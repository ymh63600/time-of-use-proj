from fastapi import  Depends, HTTPException, status,Request,Body,Request,Form
from fastapi import APIRouter
from connection import get_db
from utility import verify_password,verify_token,send_email,pwd_context 
from config import Response
from sqlalchemy.orm.session import Session
from models import User, UpdatePassword, ForgetPassword
from fastapi.responses import JSONResponse
import jwt
from config import Config

password_router = APIRouter()

@password_router.patch(
    "/password/update/",
    tags=["Password"],
    summary="update password",
    description="update password",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def update_password(password: UpdatePassword,
                          current_user: str = Depends(verify_token),
                          db: Session = Depends(get_db)):
    
    user: User = (db.query(User).filter(User.username == current_user).first())
    if not verify_password(password.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )
    else:
        if password.new_password == password.confirm_password:
            user.password=pwd_context.hash(password.new_password)
    db.commit()
    db.close()
    return JSONResponse({"message": "User data updated successfully"})



@password_router.post(
    "/password/find/{token}",
    tags=["Password"],
    summary="find password",
    description="find password",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def find_password(password: ForgetPassword,
                          token,
                          db: Session = Depends(get_db)):
    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
    username = payload.get("sub")
    user: User = (db.query(User).filter(User.username == username).first())
    if password.new_password == password.confirm_password:
        user.password=pwd_context.hash(password.new_password)
    db.commit()
    db.close()
    return JSONResponse({"message": "Enter your new password to login!"})

@password_router.patch(
    "/password/forget/",
    tags=["Password"],
    summary="forget password",
    description="forget password",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def forget_password(request:Request,
                          db: Session = Depends(get_db)):
    body = await request.json()
    username = body.get("username",None)
    user: User = (
            db.query(User).filter(User.username == username).first()
        )
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    else:
        send_email(username,"forget")
        return {"Check your email to get new password"}
    