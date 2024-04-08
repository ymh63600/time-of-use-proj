from fastapi import  Depends, HTTPException, status,Body
from fastapi import FastAPI
from connection import get_db
from utility import get_access_token,verify_password
from config import Response
from sqlalchemy.orm.session import Session
from models import User
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from admin_router import admin_router
from password_router import password_router
from user_router import user_router
from limit_router import limit_router
from calculate import data_router
from electricity import electricity_router
origins=["http://localhost:3000"]
#origins=["*"]
app = FastAPI()
app.include_router(admin_router)
app.include_router(password_router)
app.include_router(user_router)
app.include_router(data_router)
app.include_router(limit_router)
app.include_router(electricity_router)
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

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
        {"username": username, "token": jwt_token,"is_Admin": admin},
        headers={"Authorization": "Bearer " + jwt_token}
    )
    return response
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)    