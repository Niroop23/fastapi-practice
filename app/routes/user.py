from fastapi import FastAPI, Response, Depends,status,HTTPException,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    
    hashed_pwd=utils.hash(user.password)
    user.password=hashed_pwd
    new_user=models.User(**user.model_dump())
    existing_user=db.query(models.User).filter(models.User.email==new_user.email).first()
    if(existing_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the requested id: {id} not found ")
    return user


    