from fastapi import  Depends, HTTPException, Request,Body,Request,APIRouter
from connection import get_db
from utility import verify_token,send_email,generate_token,pwd_context
from config import Response
from sqlalchemy.orm.session import Session
from models import User,Electricity_Data
from fastapi.responses import JSONResponse
from jose import jwt
from config import Config

user_router = APIRouter()

@user_router.get(
    "/user/",
    tags=["User"],
    summary="get user",
    description="get a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_user(
                   current_user: str = Depends(verify_token),
                   db: Session = Depends(get_db)):
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user:
            user_data = {
            "username": user.username,
            "electricity_meter":user.electricity_meter,
            }
            return user_data
    raise HTTPException(status_code=400, detail="User not found")
    

@user_router.post(
    "/user/",
    tags=["User"],
    summary="add user",
    description="add a new user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def create_user(username: str = Body(),
                      password: str = Body(),
                      confirm_password: str = Body(),
                      electricity_meter: str = Body(),
                      db: Session = Depends(get_db)):
    
    user: User = (db.query(User).filter(User.username == username).first())
    
    if user:
        raise HTTPException(status_code=400, detail="User already existed")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Password isn't matched")
    try: 
        check:Electricity_Data = (db.query(Electricity_Data).filter(Electricity_Data.device_uuid == electricity_meter).first())
    except:
        raise HTTPException(status_code=400, detail="Incorrect electric meter number")
        
    user = User(username=username,password =pwd_context.hash(password),electricity_meter=electricity_meter)
    db.add(user)
    db.commit()
    db.close()
    send_email(username,"create")
    jwt_token = generate_token(username)
    response = JSONResponse(
        {"username": username, "token": jwt_token},
        headers={"Authorization": "Bearer " + jwt_token}
    )
    return response

@user_router.get(
    "/user/verification/{token}",
    tags=["User"],
    summary="verifiy email",
    description="verifiy email",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def verifiy_email(token,
                        db: Session = Depends(get_db)):
    
    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
    username = payload.get("sub")
    user: User = (db.query(User).filter(User.username == username).first())
    user.confirm_email = True
    db.commit()
    db.close()
    return {"Email": "verified"}
    

@user_router.delete(
    "/user/",
    tags=["User"],
    summary="delete user",
    description="delete a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def delete_user(
                      current_user: str = Depends(verify_token),
                      db: Session = Depends(get_db)):
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    db.delete(user)
    db.commit()
    db.close()
    return JSONResponse({"message": "User deleted successfully"})
    

@user_router.patch(
    "/user/",
    tags=["User"],
    summary="update user",
    description="update a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def update_user(request:Request,
                      current_user: str = Depends(verify_token),
                      db: Session = Depends(get_db)):
    content_type=request.headers.get("Content-Type","")
    
    if "application/json" in content_type:
        data = await request.json()
        electricity_meter = data.get("electricity_meter",None)
        
    user: User = (db.query(User).filter(User.username == current_user).first())
    try: 
        check: Electricity_Data = (db.query(Electricity_Data).filter(Electricity_Data.device_uuid == electricity_meter).first())
    except:
        raise HTTPException(status_code=400, detail="Incorrect electric meter number")
        
    if electricity_meter is not None:
        user.electricity_meter=electricity_meter
    db.commit()
    db.close()
    return JSONResponse({"message": "User data updated successfully"})



@user_router.get(
    "/user/resend/",
    tags=["User"],
    summary="resend email",
    description="resend email",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def resend_email(user: str = Depends(verify_token)):
    send_email(user,"create")
    return {"Resend email"}

# uuid 0bd0c50a-7847-4456-ba61-8e62a8af6f3b