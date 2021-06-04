from datetime import datetime
from . import db


class Contact(db.Model):

    __tablename__ = 'contact'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    comment = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())

    def __repr__ (self):
        return f'<Contact {self.name}>'
    
    def __str__ (self):
        return f'{self.name} <{self.email}>'