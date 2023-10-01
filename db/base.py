from app import db


#create abstract base models

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())