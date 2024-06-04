from fastapi import FastAPI, HTTPException
import pandas as pd
from config import Response

app = FastAPI()

@app.get(
    "/accumulate/",
    tags=["Data"],
    summary="accumulate data",
    description="accumulate data",
    responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},)
def accumulate_electricity(start_time: str = '1970-01-26 09:00:00', end_time: str = '1970-01-27 09:00:00'):
    try:
        df = pd.read_csv('1970-01-26_1970-01-28.csv', parse_dates=[0], index_col=0)

        # Select a specific time range
        df = df.loc[start_time:end_time]

        df = df > 0
        usage_time = df.sum() * 1  # Multiply by 1 minute because each row represents 1 minute
        print(usage_time)
        return {"usage_time": usage_time.to_dict()}

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found. Please check the file path.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    start_time = '1970-01-26 01:00:00'
    end_time = '1970-01-27 09:00:00'
    print(accumulate_electricity(start_time=start_time, end_time=end_time))