from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from acess.invite.router import router as invite_router
from acess.user.router import router as user_router
from team.profiles.router import router as profiles_router
from media.upload.router import router as upload_router
from catalog.category.router import router as category_router
from catalog.service.router import router as service_router
from catalog.subservice.router import router as subservice_router
from catalog.profissional_subservice.router import router as profissional_subservice_router
from catalog.package.router import router as package_router
from media.tag_gallery.router import router as tag_router
from media.gallery.router import router as gallery_router
from team.staff.router import router as staff_router
from media.carousel.router import router as carousel_router
from informative.about.router import router as about_router
from informative.hours.router import router as hours_router
from informative.home.router import router as home_router

# Upload Arquivos
from pathlib import Path
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Kenia Studio")

app.include_router(invite_router)
app.include_router(user_router)
app.include_router(profiles_router)
app.include_router(upload_router)
app.include_router(category_router)
app.include_router(service_router)
app.include_router(subservice_router)
app.include_router(profissional_subservice_router)
app.include_router(package_router)
app.include_router(tag_router)
app.include_router(gallery_router)
app.include_router(staff_router)
app.include_router(carousel_router)
app.include_router(about_router)
app.include_router(hours_router)
app.include_router(home_router)

# Config conexão entre front e back
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config área Upload com local real do dispositivo para buscar no GET
PASTA_UPLOAD = Path(__file__).resolve().parent.parent / "upload"
app.mount("/upload", StaticFiles(directory=PASTA_UPLOAD), name="upload")