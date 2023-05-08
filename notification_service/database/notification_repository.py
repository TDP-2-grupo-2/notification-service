from sqlalchemy.orm import Session
from notification_service.database.models import Device
from notification_service.database.notification_schema import DeviceBase

def register_device(db, device: DeviceBase):
    existing_device = db.query(Device).filter(Device.user_id == device.user_id).first()
    if existing_device is None:
        print(device)
        db_device = Device(user_id=device.user_id, token=device.token)
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    else: 
        return device
        
