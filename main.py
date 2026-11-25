from datetime import UTC, datetime

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from Accounts_manager.accounts import account_router as accounts
from db.database import BASE_DIR, Base, engine
from Login_manager.login import login_router as login
from models import HomeResponse

# Ensure all tables defined on Base exist in users.db
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Allsabah's backend",
    docs_url=None,   # Disable default /docs so we can customize the favicon
    redoc_url=None,  # Disable default /redoc so we can customize the favicon
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    """Serve the favicon for the browser tab across all routes."""
    return FileResponse(
        BASE_DIR / "static" / "allsabah_icon.png",
        media_type="image/x-icon",
    )

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    """Serve Swagger UI with a custom favicon."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_favicon_url="/static/allsabah_icon.png",
    )


@app.get("/redoc", include_in_schema=False)
def redoc_html() -> HTMLResponse:
    """Serve ReDoc with a custom favicon."""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_favicon_url="/static/allsabah_icon.png",
    )


@app.get(
    "/",
    response_model=HomeResponse,
    status_code=status.HTTP_200_OK,
    tags=["General"],
    summary="Root and health check endpoint",
)
async def home() -> HomeResponse:
    """Combined root endpoint and operational health check."""
    return HomeResponse(
        message="Server Running",
        status="healthy",
        version=app.version,
        timestamp=datetime.now(UTC).isoformat(),
        docs_url="/docs",
    )

app.include_router(accounts)
app.include_router(login)
