"""CALab web interface (FastAPI app + static front end for the local app and GitHub Pages).

Contents:
    app.py        -- FastAPI routes under /api, STATIC_ENDPOINTS exported by scripts/build_static.py
    catalogue.py  -- rule catalogue, preset patterns and Python stepping, read from plugins.PLUGIN_REGISTRY
    grid_codec.py -- base-36 grid text encoding shared with static/ca_engine.js
    static/       -- ES-module front end (hash router, canvas lab, JS port of every registered rule)
"""
