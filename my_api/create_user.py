from fastapi import FastAPI, Request
from sqlmodel import Field, Session, SQLModel, create_engine
from .models import users
from auth_token import read_items
app = FastAPI()

engine = create_engine("sqlite:///database.db")



@app.post("/users/create")
async def create_user(data:dict):
    new_user=users(username=data['username'],age=data['age'])
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
    return{'message':'Utilisateur bien ajouté.'}