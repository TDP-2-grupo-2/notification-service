import requests
from notification_service.model.notification_manager import notify_users

def send_notifications_previous_day(): 
    # get evenntos que son mañana ( los que haya que notificar junto con los usuarios)
    users_to_notify = requests.get("https://event-service-solfonte.cloud.okteto.net/events/notify")

    #chequeos de codigos retornados

    # envio de notificaciones a usuarios
    notify_users(users_to_notify)


    #send notification a los que asisten