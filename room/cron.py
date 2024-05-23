import threading
from .models import Room
import time

def check_time():
    try:
        epoch = time.time()
        now = int(epoch)
        rooms = Room.objects.all()
        for room in rooms:
            if (now >= room.total_time):
                print(f"THE ROOM CODE: {room.code}")
                room.delete()
                print("ROOM DELETED !")
    
    except Exception as e:
        print(f"ERROR OCCURED : {e}")


def run():
    thread = threading.Timer(15, run)
    thread.start()
    check_time()



# from apscheduler.schedulers.background import BackgroundScheduler
# from django.conf import settings
# from django_apscheduler.jobstores import DjangoJobStore, register_events
# import time
# from .models import Room

# def check_time():
#     rooms = Room.objects.all()
#     epoch = time.time()
#     now = int(epoch)
#     for room in rooms:
#         if now >= room.total_time:
#             print(f"ROOM CODE: {room.code}")
#             room.delete()
#             print("ROOM IS DELETED")

# @register_events
# def start_scheduler(sender):
#     scheduler = BackgroundScheduler(settings.APSCHEDULER_SETTINGS)
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     scheduler.add_job(check_time, "interval", minutes=1, id="check_time_job")
#     scheduler.start()