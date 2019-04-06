import time


def cpu_background_task():
    cnt = 0
    while True:
        print(f"CPU BG task {cnt}")
        time.sleep(1)
        cnt += 1