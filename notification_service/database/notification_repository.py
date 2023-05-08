from sqlalchemy.orm import Session
from notification_service.database.models import Device
from notification_service.database.notification_schema import DeviceBase

def register_device(db, device: DeviceBase):
    existing_device = db.query(Device).filter(Device.user_id == device.user_id).first()
    if existing_device is None:
        db_device = Device(user_id=device.user_id, token=device.token)
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    else: 
        return device
    

def get_device_token(db: Session, user_id: int):
    existing_device = db.query(Device).filter(Device.user_id == user_id).first()
    if existing_device is None:
        return None
    return existing_device.token
    
        
