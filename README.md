# Demo FastAPI Auth App

Simple demo showing registration, login (JWT), and a protected route.

## Prerequisites

- Python 3.8+
- Git (optional)

## Quickstart (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

(Unix/macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create environment file

```powershell
copy app\config\.env.example app\.env
# or on Unix: cp app/config/.env.example app/.env
```

You can also edit `app/.env` directly if present.

4. Run the app

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If `uvicorn` is not on PATH, use `python -m uvicorn ...` as shown.

## API endpoints

- `POST /register` — body JSON: `{ "username": "alice", "password": "secret" }`
- `POST /login` — form data: `username`, `password` (returns `access_token`)
- `GET /protected` — requires header `Authorization: Bearer <ACCESS_TOKEN>`

### Example flow (curl)

Register:

```bash
curl -X POST "http://127.0.0.1:8000/register" -H "Content-Type: application/json" -d '{"username":"alice","password":"secret"}'
```

Login (get token):

```bash
curl -X POST "http://127.0.0.1:8000/login" -d "username=alice&password=secret" -H "Content-Type: application/x-www-form-urlencoded"
```

Use token:

```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/protected
```

## Docs

Interactive docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Notes

- Users are stored in-memory (demo only). Replace with a real repository for persistence.
- JWT settings are read from `app/config/settings.py` and the `.env` file — set `SECRET_KEY` before production.
- If you run into PATH issues for scripts, call `python -m <module>` to run installed entrypoints.

## Next steps (optional)

- Persist users in a database.
- Return token upon registration.
- Add unit tests for auth helpers.
