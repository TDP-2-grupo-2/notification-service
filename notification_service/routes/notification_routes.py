from fastapi import APIRouter, Depends, Request, status
from notification_service.database.database import get_postg_db
from sqlalchemy.orm import Session
from notification_service.database.notification_schema import DeviceBase
from notification_service.database import notification_repository
from notification_service.utils.jwt_handler import decode_token

notification_router = APIRouter()

@notification_router.post("/new_user", status_code=status.HTTP_201_CREATED)
def register_new_device(rq: Request, device: DeviceBase, db: Session = Depends(get_postg_db)):
    token = rq.headers.get("authorization")
    if token is not None:
        user_id = decode_token(token)['id']
        print('uuser', user_id)
        new_device = notification_repository.register_device(db, user_id, device.device_token)
    return {"message": new_device}


@notification_router.get("/", status_code=status.HTTP_201_CREATED)
def register_new_device(db: Session = Depends(get_postg_db)):

    registered_devices = notification_repository.get_registered_devices(db)
    return {"message": registered_devices}



