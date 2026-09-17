from fastapi import FastAPI

from invite.router import router as invite_router

app = FastAPI(title="Kenia Studio")

app.include_router(invite_router)
