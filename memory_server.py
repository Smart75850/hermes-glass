#!/usr/bin/env python3
"""
Hermes Glass — Memory Bridge Server
提供记忆图谱、Cron、工作区、Kanban、Token 用量等 API
端口 8791，读取 Hermes Agent SQLite 数据库
"""

import json
import sqlite3
import os
import time
import glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERMES_DIR = os.path.expanduser("~/.hermes")
STATE_DB = os.path.join(HERMES_DIR, "state.db")
KANBAN_DB = os.path.join(HERMES_DIR, "kanban.db")
WORKSPACE_DIR = os.path.expanduser("~")
PORT = 8791


def safe_query(db_path, sql, params=()):
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cur = conn.execute(sql, params)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        return []


def safe_query_one(db_path, sql, params=()):
    rows = safe_query(db_path, sql, params)
    return rows[0] if rows else {}


# ═══ API Handlers ═══

def api_memory_graph():
    """返回 D3 记忆图谱节点 + 连线"""
    # 从 state.db 读取 sessions 作为节点
    sessions = safe_query(STATE_DB, """
        SELECT id, title, created_at, updated_at
        FROM sessions ORDER BY updated_at DESC LIMIT 50
    """)
    nodes = []
    links = []
    for s in sessions:
        title = s.get("title") or f"Session {s['id'][:8]}"
        nodes.append({
            "id": s["id"],
            "name": title[:40],
            "type": "session",
            "updated": s.get("updated_at", ""),
        })
    return {"nodes": nodes, "links": links}


def api_memory_focus():
    """当前焦点话题"""
    return {"focus": [], "stack": []}


def api_memory_search(query, limit=20):
    """FTS5 全文搜索"""
    results = safe_query(STATE_DB, """
        SELECT id, title, created_at FROM sessions
        WHERE title LIKE ? ORDER BY updated_at DESC LIMIT ?
    """, (f"%{query}%", limit))
    return list(results)


def api_cron():
    """Cron 任务状态"""
    jobs = safe_query(STATE_DB, """
        SELECT id, name, schedule, enabled, last_run, next_run
        FROM cron_jobs ORDER BY name
    """)
    return list(jobs) if jobs else []


def api_workspace(subpath=""):
    """工作区文件浏览"""
    base = os.path.join(WORKSPACE_DIR, subpath.lstrip("/"))
    if not os.path.exists(base):
        return {"path": subpath, "entries": [], "error": "path not found"}
    entries = []
    try:
        for name in sorted(os.listdir(base))[:50]:
            full = os.path.join(base, name)
            entries.append({
                "name": name,
                "type": "dir" if os.path.isdir(full) else "file",
                "size": os.path.getsize(full) if os.path.isfile(full) else 0,
                "mtime": os.path.getmtime(full),
            })
    except PermissionError:
        pass
    return {"path": subpath or "/", "entries": entries}


def api_kanban():
    """Kanban 任务"""
    tasks = safe_query(KANBAN_DB, """
        SELECT id, title, status, priority, created_at
        FROM tasks ORDER BY priority DESC, created_at DESC LIMIT 50
    """)
    columns = {"todo": [], "in_progress": [], "done": []}
    for t in tasks:
        status = t.get("status", "todo")
        if status not in columns:
            status = "todo"
        columns[status].append(t)
    return columns


def api_tokens():
    """Token 用量统计"""
    usage = safe_query(STATE_DB, """
        SELECT
            COUNT(*) as total_messages,
            COALESCE(SUM(length(content)), 0) as total_chars
        FROM messages
    """)
    return usage[0] if usage else {"total_messages": 0, "total_chars": 0}


def api_status():
    """服务状态"""
    return {
        "memory_bridge": "ok",
        "state_db": os.path.exists(STATE_DB),
        "kanban_db": os.path.exists(KANBAN_DB),
        "sessions": len(safe_query(STATE_DB, "SELECT COUNT(*) as c FROM sessions")),
    }


# ═══ HTTP Server ═══

ROUTES = {
    "/api/memory/graph": api_memory_graph,
    "/api/memory/focus": api_memory_focus,
    "/api/status": api_status,
    "/api/cron": api_cron,
    "/api/kanban": api_kanban,
    "/api/tokens": api_tokens,
}


class MemoryBridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # CORS
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

        result = {}

        if path == "/api/memory/search":
            q = params.get("q", [""])[0]
            limit = int(params.get("limit", ["20"])[0])
            result = api_memory_search(q, limit)
        elif path == "/api/workspace":
            subpath = params.get("path", [""])[0]
            result = api_workspace(subpath)
        elif path in ROUTES:
            result = ROUTES[path]()
        else:
            result = {"error": "not found", "path": path}

        self.wfile.write(json.dumps(result, ensure_ascii=False, default=str).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # quiet


def main():
    print(f"🧠 Memory Bridge → http://127.0.0.1:{PORT}")
    print(f"   State DB: {STATE_DB} ({'✅' if os.path.exists(STATE_DB) else '❌'})")
    print(f"   Kanban DB: {KANBAN_DB} ({'✅' if os.path.exists(KANBAN_DB) else '❌'})")
    server = HTTPServer(("127.0.0.1", PORT), MemoryBridgeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print("\n👋 Memory Bridge stopped")


if __name__ == "__main__":
    main()
