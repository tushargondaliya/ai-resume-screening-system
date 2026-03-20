from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes import auth_routes, job_routes, resume_routes, match_routes
from config.database import connect_to_mongo, close_mongo_connection
import os

app = FastAPI(title="AI Resume Screening System")

# Ensure static and templates dirs exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(job_routes.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(resume_routes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(match_routes.router, prefix="/api/matches", tags=["matches"])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create_job")
async def create_job_page(request: Request):
    return templates.TemplateResponse("create_job.html", {"request": request})
