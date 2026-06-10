"""
CONSOLA — servidor multi-usuario para escribir con markov, tracery, claude y web.

Configuracion via variables de entorno:
  CLAUDE_API_KEY     - tu API key de Anthropic (sk-ant-...)
  FLASK_SECRET_KEY   - secreto para firmar cookies de sesion
  CONSOLA_USERS_FILE - ruta al users.json (default: users.json)
  CONSOLA_DB_FILE    - ruta al SQLite (default: consola.db)
  PORT               - puerto a escuchar (default: 5000)

Para correr en local:
  pip install -r requirements.txt
  cp users.example.json users.json   # edita y agrega hashes
  export CLAUDE_API_KEY=sk-ant-...
  export FLASK_SECRET_KEY=$(python -c "import secrets;print(secrets.token_hex(32))")
  python server.py
"""

import json
import os
import sqlite3
import time
from functools import wraps
from pathlib import Path

import markovify
import requests
from flask import Flask, g, jsonify, redirect, request, send_from_directory, session
from werkzeug.security import check_password_hash

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = Path(os.environ.get("CONSOLA_USERS_FILE", BASE_DIR / "users.json"))
DB_FILE = Path(os.environ.get("CONSOLA_DB_FILE", BASE_DIR / "consola.db"))
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=4 * 1024 * 1024,
)


# ─── users ──────────────────────────────────────────────────────────────

def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {u["username"]: u["password_hash"] for u in data.get("users", [])}


# ─── db ─────────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT 'sin titulo',
            body  TEXT NOT NULL DEFAULT '',
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_documents_owner ON documents(owner);
        """
    )
    conn.commit()
    conn.close()


# ─── auth helpers ───────────────────────────────────────────────────────

def login_required(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        if not session.get("user"):
            return jsonify({"error": "no auth"}), 401
        return fn(*a, **kw)
    return wrapper


def current_user():
    return session.get("user")


# ─── routes: static + auth ──────────────────────────────────────────────

@app.route("/")
def index():
    if not session.get("user"):
        return send_from_directory(BASE_DIR, "login.html")
    return send_from_directory(BASE_DIR, "consola.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    users = load_users()
    if username in users and check_password_hash(users[username], password):
        session["user"] = username
        return jsonify({"ok": True, "user": username})
    return jsonify({"error": "credenciales invalidas"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/me")
def me():
    user = session.get("user")
    if not user:
        return jsonify({"user": None}), 401
    return jsonify({"user": user})


# ─── routes: documents ──────────────────────────────────────────────────

@app.route("/api/docs", methods=["GET"])
@login_required
def docs_list():
    rows = get_db().execute(
        "SELECT id, title, updated_at FROM documents WHERE owner = ? ORDER BY updated_at DESC",
        (current_user(),),
    ).fetchall()
    return jsonify({"docs": [dict(r) for r in rows]})


@app.route("/api/docs", methods=["POST"])
@login_required
def docs_create():
    data = request.get_json() or {}
    title = (data.get("title") or "sin titulo").strip() or "sin titulo"
    body = data.get("body") or ""
    now = time.time()
    db = get_db()
    cur = db.execute(
        "INSERT INTO documents (owner, title, body, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (current_user(), title, body, now, now),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid, "title": title, "updated_at": now})


@app.route("/api/docs/<int:doc_id>", methods=["GET"])
@login_required
def docs_get(doc_id):
    row = get_db().execute(
        "SELECT id, title, body, updated_at FROM documents WHERE id = ? AND owner = ?",
        (doc_id, current_user()),
    ).fetchone()
    if not row:
        return jsonify({"error": "no existe"}), 404
    return jsonify(dict(row))


@app.route("/api/docs/<int:doc_id>", methods=["PUT"])
@login_required
def docs_update(doc_id):
    data = request.get_json() or {}
    db = get_db()
    row = db.execute(
        "SELECT id FROM documents WHERE id = ? AND owner = ?",
        (doc_id, current_user()),
    ).fetchone()
    if not row:
        return jsonify({"error": "no existe"}), 404
    fields, values = [], []
    if "title" in data:
        fields.append("title = ?")
        values.append((data["title"] or "sin titulo").strip() or "sin titulo")
    if "body" in data:
        fields.append("body = ?")
        values.append(data["body"] or "")
    fields.append("updated_at = ?")
    now = time.time()
    values.append(now)
    values.extend([doc_id, current_user()])
    db.execute(
        f"UPDATE documents SET {', '.join(fields)} WHERE id = ? AND owner = ?",
        values,
    )
    db.commit()
    return jsonify({"ok": True, "updated_at": now})


@app.route("/api/docs/<int:doc_id>", methods=["DELETE"])
@login_required
def docs_delete(doc_id):
    db = get_db()
    db.execute(
        "DELETE FROM documents WHERE id = ? AND owner = ?",
        (doc_id, current_user()),
    )
    db.commit()
    return jsonify({"ok": True})


# ─── routes: generators ─────────────────────────────────────────────────

@app.route("/api/markov", methods=["POST"])
@login_required
def api_markov():
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()
    sentences = int(data.get("sentences") or 3)
    state_size = int(data.get("state_size") or 2)
    if not text:
        return jsonify({"error": "necesito texto de entrenamiento"}), 400
    try:
        model = markovify.Text(text, state_size=state_size)
    except Exception as e:
        return jsonify({"error": f"no se pudo entrenar el modelo: {e}"}), 400
    out = []
    for _ in range(max(1, min(sentences, 20))):
        s = model.make_sentence(tries=100)
        if s:
            out.append(s)
    if not out:
        return jsonify({"error": "no se pudo generar (mas texto o baja el state_size)"}), 400
    return jsonify({"result": " ".join(out)})


@app.route("/api/claude", methods=["POST"])
@login_required
def api_claude():
    if not CLAUDE_API_KEY:
        return jsonify({"error": "el servidor no tiene CLAUDE_API_KEY configurada"}), 500
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt vacio"}), 400
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
    except requests.RequestException as e:
        return jsonify({"error": f"red: {e}"}), 502
    if r.status_code != 200:
        try:
            msg = r.json().get("error", {}).get("message", r.text)
        except Exception:
            msg = r.text
        return jsonify({"error": f"claude: {msg}"}), r.status_code
    payload = r.json()
    parts = [b.get("text", "") for b in payload.get("content", []) if b.get("type") == "text"]
    return jsonify({"result": "".join(parts)})


# ─── main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    if not USERS_FILE.exists():
        print(f"[!] no encontre {USERS_FILE} — copia users.example.json y agrega hashes")
    if not CLAUDE_API_KEY:
        print("[!] CLAUDE_API_KEY vacia — el panel de Claude no va a funcionar")
    port = int(os.environ.get("PORT", "5000"))
    print(f"[*] consola corriendo en http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
