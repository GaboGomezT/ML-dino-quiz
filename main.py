from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")


@app.get("/")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )


@app.post("/")
def form_post(
    request: Request,
    num: int = Form(...),
    fname: str = Form(...),
    diet: str = Form(...),
):
    result = [num, fname, diet]
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )
