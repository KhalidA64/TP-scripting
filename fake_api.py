from fastapi import FastAPI, Request, HTTPException
import random
import time
import os
from dotenv import load_dotenv
load_dotenv()  
app = FastAPI()
API_TOKEN = os.getenv("API_TOKEN")  
@app.get("/api/monitor")
async def monitor(request: Request):
   token = request.headers.get("Authorization")
   if token != f"Bearer {API_TOKEN}":
       raise HTTPException(status_code=401, detail="Invalid token")
   fake_response_time = round(random.uniform(0.1, 1.5), 2)
   time.sleep(fake_response_time)
   return {
       "status": "OK",
       "response_time": fake_response_time
   }