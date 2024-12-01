from fastapi import FastAPI, Depends, status
from typing import List
from db import database
from db.database import engine, get_db
from mission import Mission
from users import user
from users.user_schemas import MissionRequest, MissionResponse, UserRequest, UserResponse
from users.user import User
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

database.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return { 'message': 'Server alive!', 'time': datetime.now() }

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users

@app.get('/missions', status_code=status.HTTP_200_OK, response_model=List[MissionResponse])
def get_all_missions(db: Session = Depends(get_db)):
    all_missions = db.query(Mission).all()
    return all_missions

@app.post('/missions', status_code=status.HTTP_201_CREATED, response_model=MissionResponse)
def create_mission(post_mission: MissionRequest, db: Session = Depends(get_db)):
    new_mission = Mission(**post_mission.model_dump())
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission.__dict__

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
    new_user = User(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.__dict__
