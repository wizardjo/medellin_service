import os
from fastapi import FastAPI, Depends, status
from typing import List
from db import database
from db.database import engine, get_db
from missions.mission import Mission
from builds.build import Build
from users import user
from schemas.schemas import BuildRequest, BuildResponse, MissionRequest, MissionResponse, UserRequest, UserResponse
from users.user import User
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from datetime import datetime

app = FastAPI()
url = os.environ['DB_URL']
print(url)
database.Base.metadata.create_all(bind=engine)

#Root API
@app.get('/')
def index():
    return { 'Welcome': 'Server alive', 'times': datetime.now() }

#GET USER
# This method in the users route searchs user's id
# The param is user id
@app.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    results = select(User).where(User.id == user_id)
    user = db.scalars(results).one()
    return user

# GET
# This method get all user
@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# DELETE
# This method DELETE the user by ID
# The param is user_id
@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    results = select(User).where(User.id == user_id)
    user = db.scalars(results).one()
    db.delete(user)
    db.commit()
    return user

#GET MISSIONS
# This method get all missions
@app.get('/missions', status_code=status.HTTP_200_OK, response_model=List[MissionResponse])
def get_all_missions(db: Session = Depends(get_db)):
    all_missions = db.query(Mission).all()
    return all_missions


# POST MISSIONS
# This method create a new mission
# The parameter is post_mission: MissionRequest
@app.post('/missions', status_code=status.HTTP_201_CREATED, response_model=MissionResponse)
def create_mission(post_mission: MissionRequest, db: Session = Depends(get_db)):
    new_mission = Mission(**post_mission.model_dump())
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission.__dict__

# POST USER
# This method create a new user
# The parameter is post_user: UserRequest
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
    new_user = User(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.__dict__

# POST buildings
# This method create a new BUILD
# The parameter is post_build: BuildRequest
@app.post('/builds', status_code=status.HTTP_201_CREATED, response_model=BuildResponse)
def create_build(post_build: BuildRequest, db: Session = Depends(get_db)):
    new_build= Build(**post_build.model_dump())
    db.add(new_build)
    db.commit()
    db.refresh(new_build)
    return new_build.__dict__
