from app.controller.tayara_controller import router as tayara_router
from fastapi import FastAPI

app =  FastAPI(title="TuniHunt",debug=True)

app.include_router(tayara_router)