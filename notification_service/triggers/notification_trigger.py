import logging
import requests
from notification_service.database.database import get_postg_db
from notification_service.model.notification_manager import notify_users
from fastapi import Depends, status
from sqlalchemy.orm import Session

def send_notifications_previous_day(engine): 
    with Session(engine) as db: 
        response = requests.get("https://event-service-solfonte.cloud.okteto.net/events/tomorrow")

        if response.status_code == status.HTTP_200_OK:
            users_to_notify = response.json()['message']
            logging.warning(users_to_notify)
            notify_users(users_to_notify, db)

        else:
            logging.error('received response status', response.status_code)
