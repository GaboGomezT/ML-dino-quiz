from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import json
import random
import pickle
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

lived_in_options = [
    "India",
    "Uruguay",
    "Kazakhstan",
    "Spain",
    "Australia",
    "Madagascar",
    "United Kingdom",
    "Zimbabwe",
    "USA",
    "France",
    "Mongolia",
    "Switzerland",
    "South Africa",
    "Malawi",
    "Wales",
    "Tunisia",
    "Niger",
    "Germany",
    "Romania",
    "North Africa",
    "China",
    "Japan",
    "Brazil",
    "Uzbekistan",
    "Egypt",
    "Tanzania",
    "Russia",
    "Canada",
    "Morocco",
    "Argentina",
]


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


def map_age_to_era(age: int) -> str:
    """Late Cretaceous   10 - 15 (2012 - 2007)
    Early Cretaceous  16 - 20 (2006 - 2001)
    Late Jurassic     21 - 26 (2000 - 1995)
    Mid Jurassic      27 - 32 (1994 - 1989)
    Early Jurassic    33 - 38 (1988 - 1983)
    Late Triassic     39 - 44 (1982 - 1977)"""

    if age <= 15:
        return "Late Cretaceous"
    elif age <= 20:
        return "Early Cretaceous"
    elif age <= 26:
        return "Late Jurassic"
    elif age <= 32:
        return "Mid Jurassic"
    elif age <= 38:
        return "Early Jurassic"
    else:
        return "Late Triassic "


def min_max_human_height(height: float) -> float:
    return (height - 0.5464) / (2.72 - 0.5464)


def classify(age: int, height: float, diet: str, country: str) -> str:
    period = map_age_to_era(age)
    length = min_max_human_height(height)
    features = [diet, period, country, length]

    input_df = pd.DataFrame(
        [features], columns=["diet", "period", "lived_in", "length"]
    )

    random_forest = pickle.load(open("dino_model.mo", "rb"))
    encoder = pickle.load(open("encoder.mo", "rb"))

    x_input = encoder.transform(input_df)
    return random_forest.predict(x_input)[0]
