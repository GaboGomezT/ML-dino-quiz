from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

lived_in_options = ["USA", "United Kingdom", "China", "Mexico"]


@app.get("/")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "result": result,
            "countries": lived_in_options,
        },
    )


@app.post("/")
def form_post(
    request: Request,
    num: float = Form(...),
    fname: str = Form(...),
    diet: str = Form(...),
    country: str = Form(...)
):
    result = [num, fname, diet, country]
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "result": result,
            "countries": lived_in_options,
        },
    )
