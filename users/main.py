import uvicorn
from api import router as api_v1_router
from fastapi import FastAPI

app = FastAPI(docs_url='/docs/users', openapi_url='/api/users/openapi.json')
app.include_router(api_v1_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
