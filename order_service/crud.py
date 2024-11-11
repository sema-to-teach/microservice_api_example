from sqlalchemy.orm import Session
from . import models, shemas

def create_order(db: Session, order: shemas.OrderCreate):
    db_order = models.Order(user_id=order.user_id, item=order.item, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_user_id(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()