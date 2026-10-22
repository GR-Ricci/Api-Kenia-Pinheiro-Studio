from fastapi import FastAPI

from invite.router import router as invite_router
from user.router import router as user_router

app = FastAPI(title="Kenia Studio")

app.include_router(invite_router)
app.include_router(user_router)
