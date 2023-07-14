from app import db


# DataBase 
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20) , nullable=False,unique=True)
    password = db.Column(db.String(80) , nullable=False)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) , nullable=False,unique=True)
    password = db.Column(db.String(80) , nullable=False)