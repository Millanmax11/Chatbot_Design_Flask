# Create your models here
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100000), nullable=False)
    response = db.Column(db.String(100000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"<Chat message='{self.message}'>"