from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

lived_in_options = ["USA", "United Kingdom", "China", "Mexico"]


@app.get("/")
def form_post(request: Request):
    result = "Fill out form"
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
    age: int = Form(...),
    height: float = Form(...),
    name: str = Form(...),
    diet: str = Form(...),
    country: str = Form(...)
):
    result = {
        "age": age,
        "height": height,
        "name": name,
        "diet": diet,
        "country": country,
    }
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "result": result,
            "countries": lived_in_options,
        },
    )
