import logging
from sqlalchemy.orm import Session
from notification_service.database.models import Device
from notification_service.database.notification_schema import DeviceBase

def register_device(db, user_id, device_token):
    existing_device = db.query(Device).filter(Device.user_id == user_id).first()
    if existing_device is None:
        db_device = Device(user_id=user_id, token=device_token)
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        logging.warning(existing_device)
        return db_device
    else: 
        logging.warning(existing_device)
        return existing_device
    

def get_device_token(db: Session, user_id: int):
    existing_device = db.query(Device).filter(Device.user_id == user_id).first()
    if existing_device is None:
        return None
    return existing_device.token

def get_registered_devices(db):
    return db.query(Device).all()
    
        
