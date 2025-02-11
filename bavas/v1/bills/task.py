from celery import shared_task
import time

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        time.sleep(2)
        print(f"number is {i} good")
    return 'Done'