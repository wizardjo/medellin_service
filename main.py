import os
from fastapi import FastAPI, Depends, status
from typing import List
from db import database
from db.database import engine, get_db
from missions.mission import Mission
from buildings.build import Build
from charaters.character import Character
from celebrations.celebration import Celebration
from schemas.schemas import BuildRequest, BuildResponse, MissionRequest, MissionResponse, UserRequest, UserResponse, CharacterRequest,CharacterResponse, CelebrationRequest, CelebrationResponse
from users.user import User
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, text
from datetime import datetime

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "missions",
        "description": "Operations for missions."
    },
    {
        "name": "builds",
        "description": "Operations for builds."
    },
    {
        "name": "characters",
        "description": "Operations for builds."
    },
    {
        "name": "celebrations",
        "description": "Operations for builds."
    },
]

app = FastAPI()
url = os.environ['DB_URL']
print(url)
database.Base.metadata.create_all(bind=engine)

#Root API
@app.get('/')
def index():
    return { 'message': 'Server alive!', 'time': datetime.now() }

#USER start endpoints user
# POST USER
# This method create a new user
# The parameter is post_user: UserRequest
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Users"])
def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
    new_user = User(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.__dict__

# GET USER
# This method in the users route searchs user's id
# The param is user id
@app.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    query = text('SELECT * from users WHERE id={0}'.format(user_id))
    with engine.connect() as con:
        results = con.execute(query)
        if results is None:
            return None
        return results.one()


# GET
# This method get all user
@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserResponse], tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    query = text('SELECT * from users')
    with engine.connect() as con:
        results = con.execute(query)
        if results is None:
            return None
        return results

# DELETE
# This method DELETE the user by ID
# The param is user_id
@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    results = select(User).where(User.id == user_id)
    user = db.scalars(results).one()
    db.delete(user)
    db.commit()
    return user
#end user


#MISSIONS start missions endpoint
# POST MISSIONS
# This method create a new mission
# The parameter is post_mission: MissionRequest
@app.post('/missions', status_code=status.HTTP_201_CREATED, response_model=MissionResponse, tags=["Missions"])
def create_mission(post_mission: MissionRequest, db: Session = Depends(get_db)):
    new_mission = Mission(**post_mission.model_dump())
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission.__dict__

#GET MISSIONS
# This method get all missions
@app.get('/missions', status_code=status.HTTP_200_OK, response_model=List[MissionResponse], tags=["Missions"])
def get_all_missions(db: Session = Depends(get_db)):
    all_missions = db.query(Mission).all()
    return all_missions

#GET Mission
# This method in the missions route searchs mission's id
# The param is mission id
@app.get('/missions/{mission_id}', status_code=status.HTTP_200_OK, response_model=MissionResponse, tags=["Missions"])
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    results = select(Mission).where(Mission.id == mission_id)
    mission = db.scalars(results).one()
    return mission

# DELETE
# This method DELETE the Mission by ID
# The param is mission_id
@app.delete('/missions/{mission_id}', status_code=status.HTTP_200_OK, response_model=MissionResponse, tags=["Missions"])
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    results = select(Mission).where(Mission.id == mission_id)
    mission = db.scalars(results).one()
    db.delete(mission)
    db.commit()
    return mission
#end mission


#BUILDINGS start mission endpoint
# POST buildings
# This method create a new BUILD
# The parameter is post_build: BuildRequest
@app.post('/buildings', status_code=status.HTTP_201_CREATED, response_model=BuildResponse, tags=["Builds"])
def create_build(post_build: BuildRequest, db: Session = Depends(get_db)):
    new_build= Build(**post_build.model_dump())
    db.add(new_build)
    db.commit()
    db.refresh(new_build)
    return new_build.__dict__

#GET BUILD
# This method in the users route searchs build's id
# The param is build id
@app.get('/buildings/{build_id}', status_code=status.HTTP_200_OK, response_model=BuildResponse, tags=["Builds"])
def get_build(build_id: int, db: Session = Depends(get_db)):
    results = select(Build).where(Build.id == build_id)
    build = db.scalars(results).one()
    return build

#GET BUILDING
# This method get all buildings
@app.get('/buildings', status_code=status.HTTP_200_OK, response_model=List[BuildResponse], tags=["Builds"])
def get_all_buildings(db: Session = Depends(get_db)):
    get_all_buildings = db.query(Build).all()
    return get_all_buildings

# DELETE
# This method DELETE the build by ID
# The param is build_id
@app.delete('/buildings/{build_id}', status_code=status.HTTP_200_OK, response_model=BuildResponse, tags=["Builds"])
def delete_build(build_id: int, db: Session = Depends(get_db)):
    results = select(Build).where(Build.id == build_id)
    build = db.scalars(results).one()
    db.delete(build)
    db.commit()
    return build
#end build


#CHARACTERS start endpoints Characters
# POST Characters
# This method create a new Character
# The parameter is post_Characters: CharactersRequest
@app.post('/characters', status_code=status.HTTP_201_CREATED, response_model=CharacterResponse, tags=["Characters"])
def create_character(post_character: CharacterRequest, db: Session = Depends(get_db)):
    new_character= Character(**post_character.model_dump())
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character.__dict__

#GET character
# This method in the characters route searchs character's id
# The param is Character id
@app.get('/characters/{character_id}', status_code=status.HTTP_200_OK, response_model=CharacterResponse, tags=["Characters"])
def get_character(character_id: int, db: Session = Depends(get_db)):
    results = select(Character).where(Character.id == character_id)
    character = db.scalars(results).one()
    return character

#GET character
# This method get all characters
@app.get('/characters', status_code=status.HTTP_200_OK, response_model=List[CharacterResponse], tags=["Characters"])
def get_all_characters(db: Session = Depends(get_db)):
    get_all_characters = db.query(Character).all()
    return get_all_characters

# DELETE
# This method DELETE the character by ID
# The param is character_id
@app.delete('/characters/{character_id}', status_code=status.HTTP_200_OK, response_model=CharacterResponse, tags=["Characters"])
def delete_build(character_id: int, db: Session = Depends(get_db)):
    results = select(Character).where(Character.id == character_id)
    character = db.scalars(results).one()
    db.delete(character)
    db.commit()
    return character
#end character


#Celebration start endpoints Characters
# POST celebration
# This method create a new celebration
# The parameter is post_celebrationrs: CelebrationsRequest
@app.post('/celebrations', status_code=status.HTTP_201_CREATED, response_model=CelebrationResponse, tags=["Celebrations"])
def create_celebration(post_celebration: CelebrationRequest, db: Session = Depends(get_db)):
    new_celebration= Celebration(**post_celebration.model_dump())
    db.add(new_celebration)
    db.commit()
    db.refresh(new_celebration)
    return new_celebration.__dict__

#GET Celebration
# This method in the Celebration route searchs celebration's id
# The param is celebration id
@app.get('/celebrations/{celebration_id}', status_code=status.HTTP_200_OK, response_model=CelebrationResponse, tags=["Celebrations"])
def get_celebration(celebration_id: int, db: Session = Depends(get_db)):
    results = select(Celebration).where(Celebration.id == celebration_id)
    celebration = db.scalars(results).one()
    return celebration

#GET celebration
# This method get all celebration
@app.get('/celebrations', status_code=status.HTTP_200_OK, response_model=List[CelebrationResponse], tags=["Celebrations"])
def get_all_celebrations(db: Session = Depends(get_db)):
    get_all_celebrations = db.query(Celebration).all()
    return get_all_celebrations

# DELETE
# This method DELETE the celebration by ID
# The param is celebration_id
@app.delete('/characters/{celebration_id}', status_code=status.HTTP_200_OK, response_model=CelebrationResponse, tags=["Celebrations"])
def delete_build(celebration_id: int, db: Session = Depends(get_db)):
    results = select(Celebration).where(Celebration.id == celebration_id)
    celebration = db.scalars(results).one()
    db.delete(celebration)
    db.commit()
    return celebration
#end celebration
