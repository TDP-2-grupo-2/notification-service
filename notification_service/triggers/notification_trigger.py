import logging
import requests
from notification_service.model.notification_manager import notify_users
from fastapi import status

def send_notifications_previous_day(): 
    # get evenntos que son mañana ( los que haya que notificar junto con los usuarios)
    response = requests.get("https://event-service-solfonte.cloud.okteto.net/events/tomorrow")

    #chequeos de codigos retornados
    if response.status_code == status.HTTP_200_OK:
        users_to_notify = response.json()['message']
        logging.warning(users_to_notify)
        notify_users(users_to_notify)
        # envio de notificaciones a usuarios
    else:
        logging.error('received response status', response.status_code)



    #


    #send notification a los que asisten