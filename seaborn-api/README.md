# Seaborn Plot API

A FastAPI service that generates seaborn plots and returns them as PNG images.

## Endpoints

- `GET /` — health check
- `GET /plot` — sample scatter plot (tips dataset)
- `POST /plot` — generate a plot with custom parameters:
```json
  {
    "x": "total_bill",
    "y": "tip",
    "kind": "scatter",
    "hue": "time"
  }
```
  `kind` can be `scatter`, `line`, `bar`, or `box`.
- `GET /plot-json` — returns a plot as a base64-encoded PNG in JSON

## Run locally

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs, or
`http://127.0.0.1:8000/plot` to see a sample image directly.

## Run with Docker

```bash
docker build -t seaborn-api .
docker run -p 8000:8000 seaborn-api
```

## Deploying

GitHub itself only hosts static sites (GitHub Pages), so it can't run this
API directly. Instead, push this repo to GitHub, then connect it to a
platform that deploys from a GitHub repo:

- **Render** — "New Web Service" → connect repo → it auto-detects the
  Dockerfile, or set build command `pip install -r requirements.txt` and
  start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Railway** — "New Project" → "Deploy from GitHub repo" → auto-detects
  the Dockerfile.
- **Fly.io** — `fly launch` in this directory, then `fly deploy` (uses the
  Dockerfile automatically).

All three redeploy automatically on every push to your GitHub repo once
connected.
