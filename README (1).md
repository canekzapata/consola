# consola

consola de escritura multi-usuaria con cuatro paneles para escribir mas chingón:

- **EDITOR** central rich-text (bold, italic, tipografias, listas, colores, headers, export .txt/.html)
- **TRACERY** — gramaticas generativas estilo Kate Compton, editable en vivo
- **MARKOV** — cadenas de markov via `markovify` en el server
- **CLAUDE** — llamada a la API de Anthropic (la key vive en el server)
- **WEB** — iframe que carga DDG html / wikipedia / archive / cualquier URL
- **DOCS** sidebar con persistencia SQLite por usuarie + autosave c/8s

Estética: net-art noventero, Windows-95-ish, fondo teal, tipografía system + monospace.

## correr en local

```bash
pip install -r requirements.txt

# crear users.json con tus 5 amix
cp users.example.json users.json
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('mi-password'))"
# pega el hash en users.json para cada usuarie

# variables de entorno
export CLAUDE_API_KEY=sk-ant-...
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

python server.py
# abre http://localhost:5000
```

## deployar en un server

Cualquier VPS con python sirve. Recomendación mínima con gunicorn detrás de nginx:

```bash
pip install gunicorn
gunicorn -w 2 -b 127.0.0.1:5000 server:app
```

Pon nginx delante con HTTPS (necesario para cookies seguras en produccion). Las cookies de sesion ya estan en `HttpOnly` + `SameSite=Lax`; si vas a HTTPS, agrega tambien `SESSION_COOKIE_SECURE=True` en el `app.config`.

## variables de entorno

| variable | qué hace | default |
|---|---|---|
| `CLAUDE_API_KEY` | tu key de Anthropic | (vacía) |
| `CLAUDE_MODEL` | modelo a usar | `claude-sonnet-4-6` |
| `FLASK_SECRET_KEY` | secreto para cookies | `dev-insecure-change-me` (cámbiala!) |
| `CONSOLA_USERS_FILE` | ruta del users.json | `./users.json` |
| `CONSOLA_DB_FILE` | ruta del SQLite | `./consola.db` |
| `PORT` | puerto a escuchar | `5000` |

## archivos

```
server.py            backend Flask (auth + docs + markov + claude)
consola.html         frontend principal (post-login)
login.html           pantalla de login
users.example.json   ejemplo de usuarios — cópialo a users.json
requirements.txt     dependencias python
```

## sobre web search

El panel WEB usa un `<iframe>` para que escribas mientras navegas. Algunos sitios bloquean el embed con `X-Frame-Options` o `frame-ancestors`. DDG html, Wikipedia y archive.org sí funcionan. Si quieres mover a Claude `web_search` o a Brave Search en el futuro, el endpoint en `server.py` es facil de extender.
