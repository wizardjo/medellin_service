from pydantic import BaseModel

#USER
class UserBase(BaseModel):
  name: str
  email: str
  password: str
  registerdatetime: str
  disabled: bool

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

#CHARACTER
class CharacterBase(BaseModel):
  name: str
  description: str

  class Config:
    orm_mode = True

class CharacterRequest(CharacterBase):
  class Config:
    orm_mode = True

class CharacterResponse(CharacterBase):
  id: int

  class Config:
    orm_mode = True
    
    
#CELEBRATION
class CelebrationBase(BaseModel):
  name: str
  description: str
  date : str

  class Config:
    orm_mode = True

class CelebrationRequest(CelebrationBase):
  class Config:
    orm_mode = True

class CelebrationResponse(CelebrationBase):
  id: int

  class Config:
    orm_mode = True
