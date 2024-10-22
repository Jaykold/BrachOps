import uvicorn
from fastapi import FastAPI
from src.routes.routes import router
import config

app = FastAPI(debug=config.DEBUG)

app.include_router(router)

@app.get('/')
async def health_check():
    return "OK"

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", reload=True, port=config.PORT)