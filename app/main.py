import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return {'/': 'index page'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
