from fastapi import FastAPI
from routers import user 
import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()
app.include_router(user.router,  tags=["user"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080
    )