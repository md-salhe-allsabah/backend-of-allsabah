from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from Login_manager.login import login_router as login

from Accounts_manager.accounts import account_router as accounts
from db.database import BASE_DIR, Base, engine

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


@app.get("/")
def home() -> dict[str, str]:
    """Health check / root endpoint."""
    return {"message": "Server Running"}


app.include_router(accounts)
app.include_router(login)
