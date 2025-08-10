from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def to_float_or_none(val: str | None) -> float | None:
    if not val or val.strip() == "":
        return None
    try:
        return float(val)
    except ValueError:
        return None

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, "formula": "", "message": ""
    })

@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request,
    a_str: str = Form(""),
    b_str: str = Form(""),
    c_str: str = Form(""),
    f_str: str = Form(""),
):
    a, b, c, f = map(to_float_or_none, (a_str, b_str, c_str, f_str))
    provided = {k: v for k, v in {"a": a, "b": b, "c": c, "f": f}.items() if v is not None}
    formula = ""
    if len(provided) <= 2:
        message = "Có vô số công thức"
    elif len(provided) == 4:
        message = "Đó là công thức thu nhập của bạn" if abs(a * b * c - f) < 1e-9 else "Công thức thu nhập của bạn đã bị sai rồi!!!"
    else:
        try:
            if a is None:
                a = f / (b * c)
                formula = f"f = a • b • c ⇒ a = {a:.2f}"
            elif b is None:
                b = f / (a * c)
                formula = f"f = a • b • c ⇒ b = {b:.2f}"
            elif c is None:
                c = f / (a * b)
                formula = f"f = a • b • c ⇒ c = {c:.2f}"
            else:
                f = a * b * c
                formula = f"f = {a:.2f} • {b:.2f} • {c:.2f} = {f:.2f}"
            message = "Đây là công thức thu nhập của bạn"
        except Exception as e:
            message = "Có lỗi xảy ra: " + str(e)

    return templates.TemplateResponse("index.html", {
        "request": request, "formula": formula, "message": message
    })
