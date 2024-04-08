from fastapi import APIRouter
from fastapi import  Depends, HTTPException,Form,Body
from connection import get_db
from utility import verify_token
from config import Response
from sqlalchemy.orm.session import Session
from models import User
from fastapi.responses import JSONResponse


limit_router = APIRouter()


@limit_router.get(
    "/limit/",
    tags=["limit"],
    summary="get limit",
    description="get a limit",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_limit(current_user:str = Depends(verify_token),
                    db: Session = Depends(get_db)):            
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user:
            user_data = {
            "daylimit": user.daylimit,
            "monthlimit":user.monthlimit,
            }
            return user_data
    raise HTTPException(status_code=400, detail="User not found")

@limit_router.post(
    "/limit/day/",
    tags=["limit"],
    summary="set day limit",
    description="set day limit",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def set_daylimit(current_user:str = Depends(verify_token),
                        daylimit:str=Form(),
                        db: Session = Depends(get_db)):
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    elif daylimit is None:
        raise HTTPException(status_code=400, detail="daylimit cannot be null")
    else:
        user.daylimit = int(daylimit)
    db.commit()
    db.close()
    return {"OK"}

@limit_router.patch(
    "/limit/month/",
    tags=["limit"],
    summary="set month limit",
    description="set month limit",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def set_monthlimit(current_user:str = Depends(verify_token),
                        monthlimit:str=Form(),
                        db: Session = Depends(get_db)):
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    elif monthlimit is None:
        raise HTTPException(status_code=400, detail="monthlimit cannot be null")
    else:
        user.monthlimit = int(monthlimit)
    db.commit()
    db.close()
    return {"OK"}
         
