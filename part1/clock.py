import threading
import time
from datetime import datetime
from part3 import response
from part2.operate import get_pile_state


class Timer:
    coefficient = 10
    std_time = "2023-06-01 00:00:00"
    time1 = datetime.strptime(std_time, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.now()

    def get_time(self):
        time_difference = self.time2 - self.time1
        simulated_time = self.coefficient * time_difference + self.time1
        return simulated_time.strftime("%Y-%m-%d %H:%M:%S")


def get_simulated_time():
    return Timer().get_time()


class Clock2:
    def __init__(self, time):
        self.time = time

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        # 等待持续时间
        time.sleep(self.time)
        # 提示用户
        get_pile_state()


def start_get_pile_state(time):
    Clock2(time).start()


class Clock:
    def __init__(self, charge_time, car_id):
        self.real_time = 3600 * charge_time / Timer.coefficient  # charge_time为小时，换算为秒并除以模拟时间系数
        self.car_id = car_id

    def start_charge(self):
        car_list.append(self.car_id)
        threading.Thread(target=self.run).start()

    def run(self):
        print('car_id: {} start at {}'.format(self.car_id, datetime.now()))
        # 等待持续时间
        time.sleep(self.real_time)
        # 提示用户
        if self.car_id in car_list:
            self.charge_complete()
            car_list.remove(self.car_id)

    def charge_complete(self):
        response.end_car_charging(self.car_id)


def user_end_charge(car_id):
    car_list.remove(car_id)


def user_charge(charge_time, car_id):
    Clock(charge_time, car_id).start_charge()


car_list = []
