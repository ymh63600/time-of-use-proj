from fastapi import APIRouter, HTTPException
import pandas as pd
from config import Response

count_router = APIRouter()

@count_router.get(
    "/accumulate/",
    tags=["Data"],
    summary="accumulate data",
    description="accumulate data",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},)
def accumulate_electricity():
    try:
        start_time = '1970-01-26 09:00:00' 
        end_time = '1970-01-27 09:00:00'
        df = pd.read_csv('1970-01-26_1970-01-28.csv', parse_dates=[0], index_col=0)

        # Select a specific time range
        df = df.loc[start_time:end_time]

        df = df > 0
        usage_time = df.sum() * 1  # Multiply by 1 minute because each row represents 1 minute
        print(usage_time)
        usage_time = usage_time.to_dict()
        return {"fridge":usage_time['fridge'],
                "microwave":usage_time["microwave"],
                "light":usage_time['light'],
                "sockets":usage_time['sockets'],
                "electric_stove":usage_time['electric stove'],
                "dish_washer":usage_time['dish washer']}

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found. Please check the file path.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    start_time = '1970-01-26 09:00:00'
    end_time = '1970-01-27 09:00:00'
    #print(accumulate_electricity(start_time=start_time, end_time=end_time))
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)    