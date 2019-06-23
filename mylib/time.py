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
        self._time = {}
        return
    
    def list(self):
        return self._time.keys()
    
    def reset(self, id):
        t = time.time()
        self._time[id] = t
        return id
    
    def get(self, id):
        t = time.time()
        dt =  t - self._time[id]
        return dt
