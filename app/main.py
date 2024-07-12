import uvicorn
from api import router as api_v1_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(api_v1_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
