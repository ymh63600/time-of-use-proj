from fastapi import APIRouter
from fastapi import  Depends, HTTPException,Request,Request,Form
from connection import get_db
from utility import verify_admin
from config import Response
from sqlalchemy.orm.session import Session
from models import User
from fastapi.responses import JSONResponse


admin_router = APIRouter()


@admin_router.post(
    "/admin/",
    tags=["User"],
    summary="get user",
    description="get a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_user_admin(request:Request,
                         username:str=Form(),
                         db: Session = Depends(get_db)):            
    if verify_admin(request):
        user: User = (
            db.query(User).filter(User.username == username).first()
        )
        if user:
            user_data = {
            "username": user.username,
            "electricity_meter":user.electricity_meter,
            "last_login": user.last_login
            }
            return user_data
        raise HTTPException(status_code=400, detail="User not found")
    raise HTTPException(status_code=400, detail="You aren't admin.")

@admin_router.delete(
    "/admin/",
    tags=["User"],
    summary="get user",
    description="get a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def delete_user_admin(request:Request,
                            username:str=Form(),
                            db: Session = Depends(get_db)):
    
    if verify_admin(request): 
        user: User = (
            db.query(User).filter(User.username == username).first()
        )
        db.delete(user)
        db.commit()
        db.close()
        return JSONResponse({"message": "User deleted successfully"})
    raise HTTPException(status_code=400, detail="You aren't admin.")