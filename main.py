from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import json
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

lived_in_options = ["USA", "United Kingdom", "China", "Mexico"]


@app.get("/")
def form_post(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
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
    country: str = Form(...),
):
    dino = classify(age, height, diet, country)
    with open("dino.json") as file:
        dino_urls = json.load(file)
    dino = random.choice(list(dino_urls.keys()))
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "dino": dino,
            "img_url": dino_urls[dino],
            "countries": lived_in_options,
        },
    )


def classify(age: int, height: float, diet: str, country: str) -> str:
    return "barapasaurus"
