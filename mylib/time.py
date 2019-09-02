import datetime
import time
import pytz


def get_datetime(timezone='Asia/Tokyo'):
    return datetime.datetime.now(tz=pytz.timezone(timezone))


def record_time(func, timezone='Asia/Tokyo'):
    def wrapper(*args, **kwargs):
        start_time = get_datetime(timezone)
        print(f'↓--start_time: {start_time}--↓\n')

        retvalue = func(*args, **kwargs)

        end_time = get_datetime(timezone)
        diff_time = end_time - start_time
        print(f'\n↑--end_time  : {end_time}--↑({diff_time})')
        return retvalue
    return wrapper


class MeasureTime():
    def __init__(self):
        self.last = time.time()

    def __call__(self):
        t = time.time()
        self.last, dt = t, t - self.last
        return dt


if __name__ == "__main__":
    measure_time = MeasureTime()
    print(get_datetime())

    measure_time()
    time.sleep(0.1)
    print(measure_time())
