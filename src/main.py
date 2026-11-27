from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from workers import asgi

from users import router as users_router
from confessions import router as confessions_router
from comments import router as comments_router
from reactions import router as reactions_router
from chat import router as chat_router
from notifications import router as notifications_router


# =====================================
# APPLICATION
# =====================================

app = FastAPI(
    title="PLEASURE CITY API",
    description="Backend system for Pleasure City",
    version="1.0.0"
)


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================
# ROUTERS
# =====================================

app.include_router(users_router)
app.include_router(confessions_router)
app.include_router(comments_router)
app.include_router(reactions_router)
app.include_router(chat_router)
app.include_router(notifications_router)


# =====================================
# ROOT
# =====================================

@app.get("/")
async def root():
    return {
        "name": "PLEASURE CITY",
        "status": "online",
        "version": "1.0.0"
    }


# =====================================
# HEALTH
# =====================================

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "database": "not_connected"
    }


# =====================================
# API INFO
# =====================================

@app.get("/api")
async def api_info():
    return {
        "name": "PLEASURE CITY API",
        "version": "1.0.0",
        "modules": [
            "users",
            "confessions",
            "comments",
            "reactions",
            "chat",
            "notifications"
        ],
        "docs": "/docs"
    }


# =====================================
# CLOUDFLARE ENTRYPOINT
# =====================================

Default = asgi.entrypoint(app)
