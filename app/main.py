from fastapi import FastAPI

# requests limiter
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from contextlib import asynccontextmanager

# routers
from app.sentiments.router import router as sentiment_router
from app.summaries.router import router as summaries_router
from app.users.router import router as users_router
from app.redis import r


@asynccontextmanager
async def lifespan(app: FastAPI):
    await FastAPILimiter.init(r)

    yield

    print('shutting down...')


app = FastAPI(lifespan=lifespan)


@app.get('/', tags=['Home'])
def index():
    return {'message': 'Welcome!'}


app.include_router(sentiment_router)
app.include_router(summaries_router)
app.include_router(users_router)
