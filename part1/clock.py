import threading
import time
from datetime import datetime
from part3 import response

start_time=datetime.now()

class Timer:
    coefficient = 20
    std_time = "2023-06-07 05:40:00"
    time1 = datetime.strptime(std_time, "%Y-%m-%d %H:%M:%S")
    def get_time(self):
        time2 = datetime.now()
        time_difference = time2 - start_time
        simulated_time = self.coefficient * time_difference + self.time1
        return simulated_time.strftime("%Y-%m-%d %H:%M:%S")


def get_simulated_time():
    return Timer().get_time()


car_list = []
car_remove = {}

class Clock:
    def __init__(self, charge_time, car_id):
        self.real_time = 3600 * charge_time / Timer.coefficient  # charge_time为小时，换算为秒并除以模拟时间系数
        self.car_id = car_id

    def start_charge(self):
        car_list.append(self.car_id)
        if self.car_id not in car_remove:
            car_remove[self.car_id] = 0
        threading.Thread(target=self.run).start()

    def run(self):
        print('car_id: {} start at {}'.format(self.car_id, datetime.now()))
        # 等待持续时间
        time.sleep(self.real_time)
        # 提示用户
        if self.car_id in car_list and car_remove[self.car_id]==0:
            self.charge_complete()
            car_list.remove(self.car_id)
        else:
            car_remove[self.car_id]-=1

    def charge_complete(self):
        response.end_car_charging(self.car_id)


def user_end_charge(car_id):
    car_list.remove(car_id)
    car_remove[car_id] += 1
def user_charge(charge_time, car_id):
    Clock(charge_time, car_id).start_charge()
