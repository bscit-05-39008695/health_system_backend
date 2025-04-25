from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

client_program = db.Table('client_program',
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), nullable=False),
    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), nullable=False)
)

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    clients = db.relationship('Client', secondary=client_program, back_populates='programs')

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(50))
    programs = db.relationship('Program', secondary=client_program, back_populates='clients')