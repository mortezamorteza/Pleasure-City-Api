from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from workers import asgi

# =====================================
# PLEASURE CITY API
# =====================================

app = FastAPI(
    title="PLEASURE CITY API",
    description="Backend API for Pleasure City",
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
    allow_headers=["*"],
)

# =====================================
# ROOT
# =====================================

@app.get("/")
async def root():
    return {
        "name": "PLEASURE CITY",
        "status": "online",
        "version": "1.0.0",
        "backend": "FastAPI",
        "message": "Welcome to Pleasure City API"
    }


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "database": "not_connected",
        "api": "operational"
    }


# =====================================
# API INFORMATION
# =====================================

@app.get("/api")
async def api_info():
    return {
        "name": "Pleasure City API",
        "version": "1.0.0",
        "endpoints": {
            "root": "/",
            "health": "/api/health",
            "documentation": "/docs"
        }
    }


# =====================================
# CLOUDFLARE ASGI ENTRYPOINT
# =====================================

Default = asgi.entrypoint(app)
