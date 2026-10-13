from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(tags=["Dashboard"])

# Path ke folder templates
templates = Jinja2Templates(
    directory=str(Path(__file__).parent.parent.parent / "templates")
)


@router.get("/")
def dashboard(request: Request):
    """Serve halaman dashboard HTML."""
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"api_base": ""}
    )