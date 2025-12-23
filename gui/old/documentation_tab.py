"""
CALab - Documentation Viewer Tab
Displays documentation and user guides within the GUI
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextBrowser, QTreeWidget, QTreeWidgetItem, 
                             QSplitter, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
import os
import markdown


class DocumentationTab(QWidget):
    """
    Documentation viewer tab with navigation and search
    """
    
    def __init__(self):
        super().__init__()
        self.docs_dir = self._find_docs_dir()
        self.current_file = None
        self._setup_ui()
        self._load_index()
        
    def _find_docs_dir(self):
        """Find documentation directory"""
        # Try relative to current working directory
        possible_paths = [
            'docs',
            '../docs',
            '../../docs',
            os.path.join(os.path.dirname(__file__), '..', '..', 'docs')
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                return os.path.abspath(path)
        
        # Default fallback
        return 'docs'
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header with search
        header = self._create_header()
        layout.addLayout(header)
        
        # Main splitter: navigation tree + content viewer
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Navigation tree
        self.nav_tree = self._create_navigation_tree()
        splitter.addWidget(self.nav_tree)
        
        # Right: Content viewer
        self.content_viewer = self._create_content_viewer()
        splitter.addWidget(self.content_viewer)
        
        # Set initial sizes (30% nav, 70% content)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Footer with navigation buttons
        footer = self._create_footer()
        layout.addLayout(footer)
        
    def _create_header(self):
        """Create header with search"""
        layout = QHBoxLayout()
        
        title = QLabel("📚 Documentation")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Search box
        search_label = QLabel("🔍")
        layout.addWidget(search_label)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search documentation...")
        self.search_box.setMaximumWidth(200)
        self.search_box.returnPressed.connect(self._search)
        layout.addWidget(self.search_box)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search)
        layout.addWidget(search_btn)
        
        return layout
        
    def _create_navigation_tree(self):
        """Create navigation tree widget"""
        tree = QTreeWidget()
        tree.setHeaderLabel("Contents")
        tree.setMaximumWidth(350)
        tree.itemClicked.connect(self._on_tree_item_clicked)
        
        return tree
        
    def _create_content_viewer(self):
        """Create content viewing widget"""
        viewer = QTextBrowser()
        viewer.setOpenExternalLinks(False)
        viewer.setOpenLinks(False)
        viewer.anchorClicked.connect(self._on_link_clicked)
        
        # Set readable font
        font = QFont()
        font.setPointSize(11)
        viewer.setFont(font)
        
        return viewer
        
    def _create_footer(self):
        """Create footer with navigation buttons"""
        layout = QHBoxLayout()
        
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self._go_back)
        self.back_btn.setEnabled(False)
        layout.addWidget(self.back_btn)
        
        self.home_btn = QPushButton("🏠 Home")
        self.home_btn.clicked.connect(self._go_home)
        layout.addWidget(self.home_btn)
        
        layout.addStretch()
        
        return layout
        
    def _load_index(self):
        """Load documentation index into navigation tree"""
        self.nav_tree.clear()
        
        # Main sections
        sections = {
            'Getting Started': [
                ('📖 Introduction', 'introduction.md'),
                ('🔬 Theory', 'theory.md'),
                ('🚀 Quick Start', '../QUICKSTART.md')
            ],
            'Models': [
                ('📋 Overview', 'models/overview.md'),
                ('🎮 Game of Life', 'models/game_of_life.md'),
                ('🔌 Von Neumann', 'models/von_neumann.md'),
                ('⚡ Wire World', 'models/wire_world.md'),
                ('🌊 Elementary CA', 'models/elementary_ca.md')
            ],
            'GUI Guide': [
                ('📺 Overview', 'gui_guide/overview.md'),
                ('▶️ Simulation Tab', 'gui_guide/simulation_tab.md'),
                ('📝 Rule Editor', 'gui_guide/rule_editor.md'),
                ('🎨 Pattern Editor', 'gui_guide/pattern_editor.md'),
                ('📊 Diagnostics', 'gui_guide/diagnostics.md')
            ],
            'Tutorials': [
                ('✏️ Creating Rules', 'tutorials/creating_rules.md'),
                ('🎨 Creating Patterns', 'tutorials/creating_patterns.md'),
                ('🔌 Creating Plugins', 'tutorials/creating_plugins.md'),
                ('🎓 Advanced Techniques', 'tutorials/advanced.md')
            ],
            'Reference': [
                ('📚 API Documentation', 'reference/api.md'),
                ('💾 File Formats', 'reference/file_formats.md'),
                ('🔌 Plugin System', 'reference/plugin_system.md')
            ]
        }
        
        for section_name, items in sections.items():
            section_item = QTreeWidgetItem([section_name])
            section_item.setExpanded(True)
            
            for display_name, file_path in items:
                item = QTreeWidgetItem([display_name])
                item.setData(0, Qt.UserRole, file_path)
                section_item.addChild(item)
            
            self.nav_tree.addTopLevelItem(section_item)
        
        # Auto-load index page
        self._load_doc('index.md')
        
    def _on_tree_item_clicked(self, item, column):
        """Handle tree item click"""
        file_path = item.data(0, Qt.UserRole)
        if file_path:
            self._load_doc(file_path)
            
    def _on_link_clicked(self, url):
        """Handle link clicks in content"""
        # Convert QUrl to string
        link = url.toString()
        
        # Handle different link types
        if link.startswith('http://') or link.startswith('https://'):
            # External link - ignore for now
            pass
        else:
            # Internal link - load document
            self._load_doc(link)
            
    def _load_doc(self, rel_path):
        """Load and display a documentation file"""
        # Construct full path
        if rel_path.startswith('..'):
            # Go up from docs directory
            full_path = os.path.normpath(os.path.join(self.docs_dir, rel_path))
        else:
            full_path = os.path.join(self.docs_dir, rel_path)
        
        # Check if file exists
        if not os.path.exists(full_path):
            self._show_error(f"Documentation file not found: {rel_path}")
            return
        
        try:
            # Read markdown file
            with open(full_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert markdown to HTML
            html_content = markdown.markdown(
                md_content,
                extensions=['extra', 'codehilite', 'toc']
            )
            
            # Add CSS styling
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        line-height: 1.6;
                        padding: 20px;
                        max-width: 900px;
                        margin: 0 auto;
                    }}
                    h1 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    h2 {{
                        color: #34495e;
                        margin-top: 30px;
                    }}
                    h3 {{
                        color: #7f8c8d;
                    }}
                    code {{
                        background-color: #f7f7f7;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: 'Courier New', monospace;
                    }}
                    pre {{
                        background-color: #f7f7f7;
                        padding: 15px;
                        border-radius: 5px;
                        border-left: 4px solid #3498db;
                        overflow-x: auto;
                    }}
                    pre code {{
                        background-color: transparent;
                        padding: 0;
                    }}
                    a {{
                        color: #3498db;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 12px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #3498db;
                        color: white;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                    blockquote {{
                        border-left: 4px solid #3498db;
                        padding-left: 15px;
                        color: #7f8c8d;
                        font-style: italic;
                    }}
                    hr {{
                        border: none;
                        border-top: 2px solid #ecf0f1;
                        margin: 30px 0;
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Display in viewer
            self.content_viewer.setHtml(styled_html)
            
            # Update state
            self.current_file = rel_path
            self.back_btn.setEnabled(True)
            
        except Exception as e:
            self._show_error(f"Error loading documentation: {e}")
            
    def _show_error(self, message):
        """Show error message in viewer"""
        html = f"""
        <html>
        <body style="padding: 20px; font-family: sans-serif;">
            <h2 style="color: #e74c3c;">⚠️ Error</h2>
            <p>{message}</p>
            <p><a href="index.md">Return to Index</a></p>
        </body>
        </html>
        """
        self.content_viewer.setHtml(html)
        
    def _go_back(self):
        """Go back to previous page"""
        # Simple implementation - reload index
        self._go_home()
        
    def _go_home(self):
        """Go to documentation home"""
        self._load_doc('index.md')
        
    def _search(self):
        """Search documentation"""
        query = self.search_box.text().strip()
        
        if not query:
            return
        
        # Simple search implementation
        results = []
        
        # Search through documentation files
        for root, dirs, files in os.walk(self.docs_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            if query.lower() in content:
                                rel_path = os.path.relpath(file_path, self.docs_dir)
                                results.append(rel_path)
                    except:
                        pass
        
        # Display results
        if results:
            html = f"""
            <html>
            <body style="padding: 20px; font-family: sans-serif;">
                <h2>Search Results for "{query}"</h2>
                <p>Found {len(results)} document(s):</p>
                <ul>
            """
            for rel_path in results:
                html += f'<li><a href="{rel_path}">{rel_path}</a></li>'
            html += """
                </ul>
            </body>
            </html>
            """
            self.content_viewer.setHtml(html)
        else:
            html = f"""
            <html>
            <body style="padding: 20px; font-family: sans-serif;">
                <h2>Search Results</h2>
                <p>No results found for "{query}"</p>
                <p><a href="index.md">Return to Index</a></p>
            </body>
            </html>
            """
            self.content_viewer.setHtml(html)
