from fastapi import APIRouter
from fastapi import  Depends, HTTPException,Form,Body
from connection import get_db
from utility import verify_token
from config import Response
from sqlalchemy.orm.session import Session
from models import User, Electricity_Data
from fastapi.responses import JSONResponse
from datetime import datetime

electricity_router = APIRouter()

@electricity_router.get(
    "/electricity/today/",
    tags=["electricity"],
    summary="get today's use of elcetricity",
    description="get today's use of elcetricity",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_today(current_user:str = Depends(verify_token),
                    db: Session = Depends(get_db)):            
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user:
        now = datetime.now()  
        start_time = f'{2022}-{now.month:02d}-{now.day:02d} 00:00:00'
        start: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == start_time).first()
        )
        if start is None:
            raise HTTPException(status_code=400, detail="Date wrong!")
        time_str = now.strftime('%H:%M')
        end_time = f'{2022}-{now.month:02d}-{now.day:02d} {time_str}:00'
        end: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == end_time).first()
        )
        if end is None:
            raise HTTPException(status_code=400, detail="Date wrong!")
        
        response = JSONResponse(
        {"usage": end.normal_usage - start.normal_usage}
        )
        return response
    raise HTTPException(status_code=400, detail="User not found")



@electricity_router.get(
    "/electricity/lastmonth/",
    tags=["electricity"],
    summary="get lastmonth's use of elcetricity",
    description="get lastmonth's use of elcetricity",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_lastmonth(current_user:str = Depends(verify_token),
                    db: Session = Depends(get_db)):            
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user:
        now = datetime.now() 
        lastmonth = now.month - 1  
        start_time = f'{2022}-{lastmonth:02d}-01 00:00:00'
        start: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == start_time).first()
        )
        if start is None:
            raise HTTPException(status_code=400, detail="Date wrong!")
        end_time = f'{2022}-{now.month:02d}-01 00:00:00'
        end: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == end_time).first()
        )
        if end is None:
            raise HTTPException(status_code=400, detail="Date wrong!")
        
        response = JSONResponse(
        {"usage": end.normal_usage - start.normal_usage}
        )
        return response
    raise HTTPException(status_code=400, detail="User not found")

@electricity_router.get(
    "/electricity/compare/",
    tags=["electricity"],
    summary="compare lastmonth's use of elcetricity",
    description="compare lastmonth's use of elcetricity",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
)
async def get_compare_lastmonth(current_user:str = Depends(verify_token),
                    db: Session = Depends(get_db)):            
    user: User = (
        db.query(User).filter(User.username == current_user).first()
    )
    if user:
        now = datetime.now() 
        lastmonth = now.month - 1  
        start_time = f'{2022}-{lastmonth:02d}-01 00:00:00'
        my_start: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == start_time).first()
        )
        end_time = f'{2022}-{now.month:02d}-01 00:00:00'
        my_end: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.device_uuid == user.electricity_meter,Electricity_Data.generated_time == end_time).first()
        )
        start: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.generated_time == start_time).order_by(Electricity_Data.device_uuid.desc()).all()
        )
        end: Electricity_Data = (
        db.query(Electricity_Data).filter(Electricity_Data.generated_time == end_time).order_by(Electricity_Data.device_uuid.desc()).all()
        )
        if my_start is None or my_end is None or start is None or end is None:
            raise HTTPException(status_code=400, detail="Date wrong!")
        my_usage = my_end.normal_usage - my_start.normal_usage
        usage = []
        for i in range(len(end)):
            usage.append(end[i].normal_usage - start[i].normal_usage)
        
        usage = sorted(usage)
        rank = 0
        for i in range(len(usage)):
            if(usage[i] == my_usage):
                rank = i
        response = JSONResponse(
        {"rank":  (rank + 1)/len(usage),"total_list": usage, "my_usage":my_usage}
        )
        return response
    raise HTTPException(status_code=400, detail="User not found")