from fastapi import FastAPI

from curso_fastapi.routers.auth import auth_router
from curso_fastapi.routers.users import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
