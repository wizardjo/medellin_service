from pydantic import BaseModel


# USER
class UserBase(BaseModel):
    name: str
    email: str
    password: str
    registerdatetime: str
    id: str

    class Config:
        orm_mode = True


class UserRequest(UserBase):
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: str

    class Config:
        orm_mode = True


# USER_EVENTS
class UserEventBase(BaseModel):
    user_id: str
    event_name: str
    timestamp: str

    class Config:
        orm_mode = True


class UserEventRequest(UserEventBase):
    class Config:
        orm_mode = True


class UserEventResponse(UserEventBase):
    id: int

    class Config:
        orm_mode = True


# USER_RESOURCES
class UserResourceBase(BaseModel):
    user_id: str
    food: int = 0
    gold: int = 0
    wood: int = 0
    stone: int = 0


class UserResourceUpdate(BaseModel):
    food: int = 0
    gold: int = 0
    wood: int = 0
    stone: int = 0


class UserResourceResponse(UserResourceBase):
    id: int

    class Config:
        orm_mode = True

# USER_RESOURCES
class DailyBonusResponse(BaseModel):
    message: str
    bonus: dict
    streak: int

# MISSION
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


# BUILD
class BuildBase(BaseModel):
    name: str
    description: str
    cost: int
    preview_build: str
    experience_require: int

    class Config:
        orm_mode = True


class BuildRequest(BuildBase):
    class Config:
        orm_mode = True


class BuildResponse(BuildBase):
    id: int

    class Config:
        orm_mode = True


# CHARACTER
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


# CELEBRATION
class CelebrationBase(BaseModel):
    name: str
    description: str
    date: str

    class Config:
        orm_mode = True


class CelebrationRequest(CelebrationBase):
    class Config:
        orm_mode = True


class CelebrationResponse(CelebrationBase):
    id: int

    class Config:
        orm_mode = True
