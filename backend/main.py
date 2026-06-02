# from contextlib import asynccontextmanager
# import asyncio
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import logging

# from backend.power_plant.routes import router as power_router, load_all_models as load_power_models
# from backend.steel_plant.routes import router as steel_router, load_all_models as load_steel_models

# logger = logging.getLogger("main")


# async def _load_models_background():
#     """
#     Load both sets of models after the server is already up and accepting
#     requests. This way Render sees an open port immediately and does not
#     time-out waiting for HuggingFace downloads to finish.
#     """
#     logger.info("🚀 Background: Loading Power Plant models …")
#     try:
#         await load_power_models()
#         logger.info("✅ Power Plant models ready.")
#     except Exception as e:
#         logger.error("❌ Power Plant model loading failed: %s", e)

#     logger.info("🚀 Background: Loading Steel Plant models …")
#     try:
#         await load_steel_models()
#         logger.info("✅ Steel Plant models ready.")
#     except Exception as e:
#         logger.error("❌ Steel Plant model loading failed: %s", e)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Fire model loading as a background task so the server binds its port
#     # BEFORE the HuggingFace downloads start. Render's port scanner will see
#     # the open port within a second and consider the deploy successful.
#     asyncio.create_task(_load_models_background())
#     yield
#     # Shutdown: nothing extra needed


# app = FastAPI(
#     title="iFactory AI Backend",
#     description="Power Plant + Steel Plant AI inference APIs",
#     version="1.0.0",
#     lifespan=lifespan,
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/ping", tags=["meta"])
# def ping():
#     return {"status": "ok", "message": "pong"}


# @app.get("/", tags=["meta"])
# def root():
#     return {
#         "service": "iFactory AI Backend",
#         "version": "1.0.0",
#         "routes": ["/power", "/steel", "/ping", "/docs"],
#     }


# app.include_router(power_router, prefix="/power")
# app.include_router(steel_router, prefix="/steel")


from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.steel_plant.routes import router as steel_router, load_all_models as load_steel_models

logger = logging.getLogger("main")

async def _load_models_background():
    logger.info("🚀 Loading Steel Plant models …")
    try:
        await load_steel_models()
        logger.info("✅ Steel Plant models ready.")
    except Exception as e:
        logger.error("❌ Steel Plant model loading failed: %s", e)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(_load_models_background())
    yield

app = FastAPI(
    title="Steel Plant AI Backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

app.include_router(steel_router, prefix="/steel")
