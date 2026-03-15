"""
Interview Prep HTML Generator — Local preview server.

Usage:
    python app.py                  # uses ./data as data dir, port 8080
    python app.py --data ./mydata  # custom data directory
    python app.py --port 3000      # custom port
    python app.py --export out.html  # export to file instead of serving

Data directory structure:
    data/
    ├── intern_ja.yaml (or .md)
    ├── intern_zh.yaml (or .md)
    ├── work_ja.yaml
    ├── work_zh.yaml
    ├── project_ja.yaml
    └── project_zh.yaml
"""

import argparse
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import yaml

from parser import parse_file, TabData
from generator import generate_html

DEFAULT_CONFIG = {
    "title": "面接準備ドキュメント / 面试准备文档",
    "tabs": [
        {"id": "intern", "icon": "🎓", "label_ja": "実習経験", "label_zh": "实习经历"},
        {"id": "work", "icon": "🏢", "label_ja": "職務経験", "label_zh": "公司经历"},
        {"id": "project", "icon": "🔬", "label_ja": "プロジェクト", "label_zh": "项目经历"},
    ],
    "data_dir": "./data",
    "port": 8080,
}


def load_config(config_path: Path) -> dict:
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        merged = {**DEFAULT_CONFIG, **user_config}
        return merged
    return DEFAULT_CONFIG.copy()


def load_data(data_dir: Path, tabs: list[dict]) -> dict[str, dict[str, TabData | None]]:
    """Scan data_dir for tab files and parse them."""
    data = {}
    for tab in tabs:
        tab_id = tab["id"]
        data[tab_id] = {"ja": None, "zh": None}

        for lang in ("ja", "zh"):
            # Try yaml first, then md
            for ext in (".yaml", ".yml", ".md"):
                filepath = data_dir / f"{tab_id}_{lang}{ext}"
                if filepath.exists():
                    try:
                        data[tab_id][lang] = parse_file(filepath)
                        print(f"  Loaded: {filepath.name}")
                    except Exception as e:
                        print(f"  Error loading {filepath.name}: {e}")
                    break

    return data


def build_html(config: dict, data_dir: Path) -> str:
    data = load_data(data_dir, config["tabs"])
    return generate_html(config["title"], config["tabs"], data)


def _get_data_fingerprint(data_dir: Path) -> float:
    """Return the latest mtime across all data files. 0 if no files."""
    latest = 0.0
    if data_dir.exists():
        for f in data_dir.iterdir():
            if f.is_file() and f.suffix in (".yaml", ".yml", ".md"):
                latest = max(latest, f.stat().st_mtime)
    return latest


class PreviewHandler(BaseHTTPRequestHandler):
    """Serve cached HTML, regenerate only when data files change."""

    config: dict = {}
    data_dir: Path = Path("./data")
    _cache_html: str = ""
    _cache_fingerprint: float = -1.0

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            print("\n[Regenerating HTML...]")
            html = build_html(self.config, self.data_dir)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/export":
            html = build_html(self.config, self.data_dir)
            export_path = self.data_dir.parent / "output.html"
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(html)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            msg = f"Exported to {export_path.resolve()}"
            self.wfile.write(msg.encode("utf-8"))
            print(f"  Exported: {export_path.resolve()}")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress default access logs


def main():
    parser = argparse.ArgumentParser(description="Interview Prep HTML Generator")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--data", default=None, help="Data directory (overrides config)")
    parser.add_argument("--port", type=int, default=None, help="Server port (overrides config)")
    parser.add_argument("--export", default=None, help="Export HTML to file and exit")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    data_dir = Path(args.data) if args.data else Path(config["data_dir"])
    port = args.port if args.port else config["port"]

    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        print(f"Creating: {data_dir}")
        data_dir.mkdir(parents=True)

    # Export mode
    if args.export:
        print(f"Loading data from: {data_dir.resolve()}")
        html = build_html(config, data_dir)
        out = Path(args.export)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Exported to: {out.resolve()}")
        return

    # Server mode
    PreviewHandler.config = config
    PreviewHandler.data_dir = data_dir

    server = HTTPServer(("127.0.0.1", port), PreviewHandler)
    print(f"Loading data from: {data_dir.resolve()}")
    # Initial load test
    build_html(config, data_dir)
    print(f"\nPreview server running at: http://127.0.0.1:{port}")
    print(f"Export endpoint:           http://127.0.0.1:{port}/export")
    print("Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
