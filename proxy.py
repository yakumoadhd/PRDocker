import os
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ── CORS設定（ブラウザからの直接リクエストを許可）──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 本番化時は自分のドメインに絞る
    allow_methods=["GET"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("PR_API_KEY", "PR_2026_xK9mQzL4vN8pRjW2")
SEARXNG_BASE = "http://127.0.0.1:8080"

@app.get("/healthz")
async def healthz():
    return Response(content="ok", status_code=200)

@app.get("/search")
async def search(request: Request):
    header_key = request.headers.get("x-api-key", "")
    query_key = request.query_params.get("api_key", "")
    if header_key != API_KEY and query_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    params = {k: v for k, v in request.query_params.items() if k != "api_key"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{SEARXNG_BASE}/search",
            params=params,
            headers={"Accept": "application/json"},
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "application/json"),
    )
