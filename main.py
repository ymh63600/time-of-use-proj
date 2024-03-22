from fastapi import  Depends, HTTPException, status,Request,Body,Request
from fastapi import FastAPI
from connection import get_db
from utility import get_access_token,verify_password,verify_token,verify_admin,send_email,generate_token
from config import Response
from sqlalchemy.orm.session import Session
from models.myUser import User
from datetime import datetime
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt
from config import Config

origins=["http://localhost:3000"]
#origins=["*"]
app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post(
    "/login",
    tags=["Login"],
    summary="return jwt",
    description="passing correct username and password of account will return jwt",
    responses={200: Response.OK.doc, 401: Response.UNAUTHORIZED.doc},
)
async def get_jwt(username: str = Body(),
                  password: str = Body(),
                  session: Session = Depends(get_db)):
    
    user: User = (
        session.query(User).filter(User.username == username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User: " + username + " not found.",
        )
    if user.confirm_email == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email is not verified.",
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )
    jwt_token = get_access_token(user, password)
    user.last_login = datetime.utcnow()
    session.commit()
    session.close()
    if username == "Admin":
        admin = True
    else:
        admin = False
    response = JSONResponse(
        {"username": username, "token": jwt_token,"Admin": admin},
        headers={"Authorization": "Bearer " + jwt_token}
    )
    return response
    

@app.get(
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
    

@app.post(
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

@app.get(
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
    #return JSONResponse({"message": "User email verified successfully"})

@app.delete(
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
    

@app.patch(
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
    if electricity_meter is not None:
        user.electricity_meter=electricity_meter
    db.commit()
    db.close()
    return JSONResponse({"message": "User data updated successfully"})

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

@app.patch(
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

class ForgetPassword(BaseModel):
    new_password: str
    confirm_password: str

@app.post(
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

@app.patch(
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
    
@app.get(
    "/user/resend/",
    tags=["User"],
    summary="resend email",
    description="resend email",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def resend_email(user: str = Depends(verify_token)):
    send_email(user,"create")
    return {"Resend email"}

'''@app.post(
    "/user/",
    tags=["User"],
    summary="get user",
    description="get a user",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_user(request:Request,
                   current_user: str = Depends(verify_token),
                   db: Session = Depends(get_db)):
    
    admin = verify_admin(request)
    body = await request.json()
    if admin: 
        username = body.get("username",None)
        user: User = (
            db.query(User).filter(User.username == username).first()
        )
    else:
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
    '''

'''
async def delete_user(request:Request,
                      current_user: str = Depends(verify_token),
                      db: Session = Depends(get_db)):
    
    admin = verify_admin(request)
    body = await request.json()
    if admin: 
        username = body.get("username",None)
        user: User = (
            db.query(User).filter(User.username == username).first()
        )
    else:
        user: User = (
            db.query(User).filter(User.username == current_user).first()
        )

    if user != "Admin":
        db.delete(user)
        db.commit()
        db.close()
        return JSONResponse({"message": "User deleted successfully"})
    raise HTTPException(status_code=400, detail="User isn't exist")'''