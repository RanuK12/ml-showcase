from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import auth_router, users_router, billing_router, health_router
from app.middleware.cors import add_cors
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="SaaS API", version="1.0.0", lifespan=lifespan)

# Middleware
add_cors(app)
app.add_middleware(RateLimitMiddleware)

# Routes
app.include_router(health_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(billing_router, prefix="/api/v1")
