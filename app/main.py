import logging
from fastapi import FastAPI
from .api import routes

# Logging configuration to capture all logs
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# Root logger setup to capture all logs from all modules
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

app = FastAPI()

# Include routes
app.include_router(routes.router)

logger.info("FastAPI application started successfully.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
