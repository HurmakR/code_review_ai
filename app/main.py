import logging
from fastapi import FastAPI
from .api import routes

file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

if not root_logger.handlers:
    root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

app = FastAPI()

# Include routes
app.include_router(routes.router)

logger.info("FastAPI application started successfully.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)