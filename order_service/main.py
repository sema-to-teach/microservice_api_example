import requests
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import crud, models, shemas, database

app = FastAPI()
database.init_db()

USER_SERVICE_URL = "http://127.0.0.1:8001/users/"
templates = Jinja2Templates(directory="order_service/templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_orders(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@app.post("/orders/", response_class=RedirectResponse)
def create_order(user_id: int = Form(...), item: str = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь в UserService
    user_response = requests.get(f"{USER_SERVICE_URL}{user_id}")
    
    if user_response.status_code != 200 :
        raise HTTPException(status_code=404, detail="User not found")
    order = shemas.OrderCreate(user_id=user_id, item=item, quantity=quantity)
    crud.create_order(db=db, order=order)
    return RedirectResponse(url="/", status_code=303)
