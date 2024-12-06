from pydantic import BaseModel

#USER
class UserBase(BaseModel):
  name: str
  surname: str
  email: str
  password: str

  class Config:
    orm_mode = True

class UserRequest(UserBase):
  class Config:
    orm_mode = True

class UserResponse(UserBase):
  id: int

  class Config:
    orm_mode = True

#MISSION
class MissionBase(BaseModel):
  name: str
  description: str

  class Config:
    orm_mode = True

class MissionRequest(MissionBase):
  class Config:
    orm_mode = True

class MissionResponse(MissionBase):
  id: int

  class Config:
    orm_mode = True
 
#BUILD   
class BuildBase(BaseModel):
  name: str
  description: str
  cost: int
  previewBuild: str
  experienceRequire : int

  class Config:
    orm_mode = True

class BuildRequest(BuildBase):
  class Config:
    orm_mode = True

class BuildResponse(BuildBase):
  id: int

  class Config:
    orm_mode = True

#
