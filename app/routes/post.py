from fastapi import FastAPI, Response, Depends,status,HTTPException,APIRouter
from typing import List,Optional
from sqlalchemy import desc,func
from app.Auth import oauth2
from .. import models
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/",response_model=List[schemas.PostResponse])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()
    # print(search)
    
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("vote_count")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [{"post": post, "votes": votes} for post, votes in posts]



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title , content, published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # new_post=models.Post(title=post.title,content=post.content,published=post.published) u can just do **modeldump
    post_Data=post.model_dump()
    post_Data["owner_id"]=current_user.id
    new_post=models.Post(**post_Data)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db)):
    
    # cursor.execute(""" SELECT * FROM posts WHERE id =(%s) """,(id,))
    # # post=cursor.fetchone()
    # post=db.query(models.Post).get(id)
    
    Post=db.query(models.Post,func.count(models.Vote.post_id).label("vote_count")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the requested id: {id} not found ")
    post,votes=Post
    return {"post": post, "votes": votes}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id=(%s) RETURNING *""",(id,))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    delete_post_query=db.query(models.Post).filter(models.Post.id==id)
    
    if delete_post_query.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    
    
    if delete_post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the requested id: {id} doesn't exist")
    
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=(%s), content=(%s), published=(%s) WHERE id=(%s) RETURNING * """,(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    existing=post_query.first()
    
    if existing==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the requested id: {id} doesn't exist")
    
    if existing.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()     
            
    return post_query.first()