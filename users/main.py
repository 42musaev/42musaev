import uvicorn
from core.config import settings
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return {'index': '/'}


if __name__ == '__main__':
    print(settings.DATABASE_URL)
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
