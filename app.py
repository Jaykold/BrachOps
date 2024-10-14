import uvicorn
from fastapi import FastAPI
from src.routes import routes
import config

app = FastAPI(debug=config.DEBUG)

routes.router(app)

@app.get('/')
async def health_check():
    return "OK"

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)