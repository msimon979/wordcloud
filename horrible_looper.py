import time

from clouds.tasks import add

# This is not scalable at all just not sure I have time to implement a cron based system within django


def ugly_worker_loop():
    while True:
        print("Running worker")
        add.delay()
        # give it some breathing room
        time.sleep(2)
