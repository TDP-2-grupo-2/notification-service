from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from notification_service.routes.notification_routes import notification_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
##comentario prueba

app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
async def welcome(status_code = status.HTTP_200_OK):
    return "Welcome to notification service!!" 