from django.db import models
from enum import Enum
# Create your models here.

class my_constant:
    charge_area = 2
    waiting_area = 6
    fast_pile = 2
    slow_pile = 3
    pile_num = fast_pile + slow_pile
    class pile_state():
        idle = "空闲"
        close = "关闭"
        using = "使用中"
        broken = "损坏"
    class car_state():
        idle = "空闲"
        wating = "处于等待区"
        charging_area = "处于充电区"
        can_charging = "允许充电"
        charging = "正在充电"
        end_charging = "结束充电"
    pass

class Queue:
    charge_queue = []
    waiting_queue = []
    def __init__(self):
        self.charge_queue = [[-1 for j in range(my_constant.charge_area)] for i in range(my_constant.pile_num)]
        self.waiting_queue = [-1 for i in range(my_constant.waiting_area)]
        self.queue_num = 0
    def get_new_queue_num(self):
        self.queue_num+=1
        return self.queue_num
    def add_car(self, car_id, charge_mode):
        start_pile_id = 0
        end_pile_id = 2
        if charge_mode=='T':
            start_pile_id = 2
            end_pile_id = my_constant.pile_num
        for j in range(0,my_constant.charge_area):
            for i in range(start_pile_id,end_pile_id):
                #pile_state=get_pile_state(i)
                #if pile_state=="损坏" or pile_state=="关闭":
                #    continue
                if self.charge_queue[i][j] == -1:
                    self.charge_queue[i][j]=car_id
                    #if pile_state=="使用中":
                    #    return 1,i
                    #else:
                    return 0,i,self.get_new_queue_num()
        for i in range(0,my_constant.waiting_area):
            if self.waiting_queue[i] == -1:
                self.waiting_queue[i]=car_id
                return 2,i,self.get_new_queue_num()
        return -1,-1,-1
    pass
