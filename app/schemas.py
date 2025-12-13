from datetime import datetime
from operator import ge, le
from typing import Optional
from pydantic import BaseModel,EmailStr, Field

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    
    model_config={
        "from_attributes":True
    }
    
class UserLogin(UserCreate):
    pass


class PostBase(BaseModel):
    title:str
    content:str
    published:bool =True
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserResponse
    
    model_config = {
    "from_attributes": True   #pydantic needs dict not sqlalchemy model 
}
    
class PostOut(BaseModel):
    post:PostResponse
    votes:int
    
    model_config={
        "from_attributes":True
    }



class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
    
    
class Vote(BaseModel):
    post_id:int
    value:int=Field(...,ge=0,le=1)
    
    
