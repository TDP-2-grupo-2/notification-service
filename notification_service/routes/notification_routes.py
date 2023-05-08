from fastapi import APIRouter, Depends, status
from notification_service.database.database import get_postg_db
from sqlalchemy.orm import Session
from notification_service.database.notification_schema import DeviceBase
from notification_service.database import notification_repository

notification_router = APIRouter()

@notification_router.post("/new_user", status_code=status.HTTP_201_CREATED)
def register_new_device(device: DeviceBase, db: Session = Depends(get_postg_db)):
    new_device = notification_repository.register_device(db, device)
    return {"message": new_device}


