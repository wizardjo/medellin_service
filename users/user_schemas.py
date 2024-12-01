from pydantic import BaseModel

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