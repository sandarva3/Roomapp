from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Text, Lanfiles
import time

def del_things():
    epoch = time.time()
    current_time = int(epoch)
    texts = Text.objects.all()
    latest_text = Text.objects.latest('created_at')
    files = Lanfiles.objects.all()

    try:
        for text in texts:
            if((current_time > (text.Tunix_time + 1800)) and text != latest_text):
                print(f"The deleted text: {text}")
                text.delete()

        for file in files:
            if(current_time > (file.Funix_time + 1800)):
                print(f"The deleted file: {file}")
                file.delete()
    except Exception as e:
        print(f"The Exception is: {e}")

    # print(f"The latest text: {latest_text}")
    

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(del_things, 'interval', minutes=1.4)
    scheduler.start()
