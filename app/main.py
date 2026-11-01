from fastapi import FastAPI

from invite.router import router as invite_router
from user.router import router as user_router
from profiles.router import router as profiles_router
from employee.router import router as employee_router
from service.router import router as service_router

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Kenia Studio")

app.include_router(invite_router)
app.include_router(user_router)
app.include_router(profiles_router)
app.include_router(employee_router)
app.include_router(service_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)