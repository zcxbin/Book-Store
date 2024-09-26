from fastapi import FastAPI
from routers.authentication import router as authentication_router
app = FastAPI()


app.include_router(authentication_router, prefix="/auth", tags=["Authentication"])
