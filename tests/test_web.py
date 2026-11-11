"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- CALab-specific API tests -------------------------------------------------------------------------------------
import json  # noqa: E402

from plugins import PLUGIN_REGISTRY  # noqa: E402
from web.grid_codec import decode, encode  # noqa: E402

FIXTURES = json.loads((ROOT / "tests" / "fixtures" / "ca_engine_fixtures.json").read_text())["cases"]


def test_rules_catalogue_matches_registry():
    rules = client.get("/api/rules").json()
    assert [r["key"] for r in rules] == list(PLUGIN_REGISTRY)
    for r in rules:
        assert r["name"] == PLUGIN_REGISTRY[r["key"]].get_metadata().name
        assert len(r["colormap"]) >= r["num_states"] or r["key"] == "cyclic_ca"
        assert r["patterns"] and r["doc"]


def test_info_counts():
    info = client.get("/api/info").json()
    assert info["automata"] == len(PLUGIN_REGISTRY)
    assert info["patterns"] == sum(len(p.get_default_patterns()) for p in PLUGIN_REGISTRY.values())


@pytest.mark.parametrize("key", list(PLUGIN_REGISTRY))
def test_patterns_decode(key):
    data = client.get(f"/api/patterns/{key}").json()
    meta = next(r for r in client.get("/api/rules").json() if r["key"] == key)
    assert len(data["patterns"]) == len(meta["patterns"])
    for p in data["patterns"]:
        g = decode(p["cells"], p["width"], p["height"])
        limit = p["params"].get("num_states", meta["num_states"])
        assert g.max() < limit, (key, p["name"])


def test_unknown_pattern_rule_404():
    assert client.get("/api/patterns/nope").status_code == 404


@pytest.mark.parametrize("case", FIXTURES, ids=[f"{c['rule']}:{c['label']}" for c in FIXTURES])
def test_run_reproduces_fixture(case):
    """The fixtures the JS engine is tested against still match the Python plugins (through the real API)."""
    r = client.post("/api/run", json={k: case[k] for k in ("rule", "width", "height", "steps", "params", "row")}
                    | {"cells": case["start"]})
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["cells"] == case["end"] and out["generation"] == case["generation"] and out["row"] == case["end_row"]


def test_run_rejects_bad_input():
    ok = {"rule": "game_of_life", "width": 4, "height": 4, "cells": "0" * 16, "steps": 1}
    assert client.post("/api/run", json=ok).status_code == 200
    assert client.post("/api/run", json=ok | {"rule": "nope"}).status_code == 404
    assert client.post("/api/run", json=ok | {"cells": "0" * 15}).status_code == 400
    assert client.post("/api/run", json=ok | {"cells": "2" + "0" * 15}).status_code == 400   # state 2 in a 2-state CA
    assert client.post("/api/run", json=ok | {"width": 400, "height": 400, "cells": "0" * 160000, "steps": 100}).status_code == 400


def test_codec_round_trip():
    import numpy as np
    g = np.arange(36, dtype=np.int32).reshape(4, 9)
    assert (decode(encode(g), 9, 4) == g).all()
