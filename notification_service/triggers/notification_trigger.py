import logging
import requests
from notification_service.model.notification_manager import notify_users
from fastapi import status

def send_notifications_previous_day(): 
    response = requests.get("https://event-service-solfonte.cloud.okteto.net/events/tomorrow")

    if response.status_code == status.HTTP_200_OK:
        users_to_notify = response.json()['message']
        logging.warning(users_to_notify)
        notify_users(users_to_notify)

    else:
        logging.error('received response status', response.status_code)
