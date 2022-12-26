import string
import random

from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import Settings


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def index(request: Request):
	return templates.TemplateResponse("shortURL/index.html", context={
		"request": request,
	})


@router.post("/shortener")
def shorten_url(request: Request, link: str = Form(...)):
	random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
	print(random_str)
	return templates.TemplateResponse("shortURL/shortener.html", context={
		"request": request,
		"shortened_url": random_str,
		"long_url": link,
	})


@router.get("/contact")
def contact(request: Request):
	return templates.TemplateResponse("shortURL/contact.html", context={
		"request": request,
	})


@router.post("/contact")
def contact(request: Request, fullname: str = Form(...), email: str = Form(...), message: str = Form(...)):
	data = {
		"fullname": fullname,
		"email": email,
		"message": message
	}
	return templates.TemplateResponse("shortURL/contact.html", context={
		"request": request, 
		"show_message": True
	})


@router.get("/privacy-policy")
def privacy(request: Request):
	return templates.TemplateResponse("shortURL/privacy.html", context={
		"request": request,
	})


@router.get("/report-malicious-url")
def report(request: Request):
	return templates.TemplateResponse("shortURL/report_url.html", context={
		"request": request, 
		"value1": random.randint(1, 9),
		"value2": random.randint(1, 9),
	})


@router.post("/report-malicious-url")
def report(request: Request, value1: str = Form(...), value2: str = Form(...), math_answer: str = Form(...)):
	answer = int(value1) + int(value2)
	if answer == int(math_answer):
		return templates.TemplateResponse("shortURL/report_url.html", context={
			"request": request,
			"report_response": "true", 
		})
	else:
		return templates.TemplateResponse("shortURL/report_url.html", context={
			"request": request,
			"report_response": "false",
		})


@router.get("/url-click-counter")
def counter(request: Request):
	return templates.TemplateResponse("shortURL/click_counter.html", context={
		"request": request,
	})


@router.get("/terms-of-service")
def terms_of_service(request: Request):
	return templates.TemplateResponse("shortURL/terms_of_service.html", context={
		"request": request,
	})


app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)