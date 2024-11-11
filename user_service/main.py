from fastapi import FastAPI, Depends, HTTPException, Request, Form 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.types import NULLTYPE
from . import crud, models, shemas, database

app = FastAPI()
database.init_db()

templates = Jinja2Templates(directory="user_service/templates")

#Создание сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Depends - возвращает то, что возвращает функция
@app.get("/", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/users/", response_class=RedirectResponse)
def create_user(name: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    user = shemas.UserCreate(name=name, email=email)
    crud.create_user(db=db, user=user)
    return RedirectResponse(url="/", status_code=303)

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user