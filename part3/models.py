from django.db import models

class my_constant:
    charge_area = 2
    waiting_area = 6
    fast_pile = 2
    slow_pile = 3
    pile_num = fast_pile + slow_pile
    price_duration=[["0:00","7:00","L"],["7:00","10:00","M"],["10:00","15:00","H"],["15:00","18:00","M"],
                    ["18:00","21:00","H"],["21:00","23:00","M"],["23:00","7:00","L"]]
    class pile_state():
        idle = "空闲"
        close = "关闭"
        using = "使用中"
        broken = "损坏"
    class car_state():
        idle = "空闲"
        wating = "处于等候区"
        charging_area = "处于充电区"
        can_charging = "允许充电"
        charging = "正在充电"
        end_charging = "充电结束"
    low_price=0
    mid_price=0
    high_price=0
    service_price=0.8
    slow_charging_v=7
    fast_charging_v=30
    pass
class Price(models.Model):
    low_price = models.FloatField(default=0.4)
    mid_price = models.FloatField(default=0.7)
    high_price = models.FloatField(default=1.0)
    pass
class Queue:
    charge_queue = []
    waiting_queue = []
    mode_queue = []
    broken_list = []
    pile_state = []
    def __init__(self):
        self.charge_queue = [[-1 for j in range(my_constant.charge_area)] for i in range(my_constant.pile_num)]
        self.waiting_queue = [-1 for j in range(my_constant.waiting_area)]
        self.mode_queue = [-1 for i in range(my_constant.waiting_area)]
        self.broken_list = [[]for i in range(2)]
        self.pile_state = [my_constant.pile_state.close for i in range(my_constant.pile_num)]
        self.queue_num = 0
    def get_new_queue_num(self):
        self.queue_num+=1
        return self.queue_num
    def add_car(self, car_id, charge_mode):
        start_pile_id = 0
        end_pile_id = my_constant.fast_pile
        queue_cnt = 1
        if charge_mode=='T':
            start_pile_id = my_constant.fast_pile
            end_pile_id = my_constant.pile_num
        for j in range(my_constant.charge_area):
            for i in range(start_pile_id,end_pile_id):
                if self.pile_state[i]==my_constant.pile_state.broken or self.pile_state[i]==my_constant.pile_state.close:
                    continue
                if self.charge_queue[i][j] == -1:
                    self.charge_queue[i][j]=car_id
                    if self.pile_state[i]==my_constant.pile_state.idle:
                        return j,i,str(self.get_new_queue_num())
                    else:
                        return j, i, str(self.get_new_queue_num())
        for i in range(my_constant.waiting_area):
            if self.mode_queue[i] == charge_mode:
                queue_cnt += 1
            if self.waiting_queue[i] == -1:
                self.waiting_queue[i]=car_id
                self.mode_queue[i]=charge_mode
                return 2,queue_cnt,str(self.get_new_queue_num())
        return -1,-1,-1
    def get_pile_id(self,car_id):
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j]==car_id:
                    return i
        return None
    def del_wating(self, car_id):
        for i in range(my_constant.waiting_area):
            if self.waiting_queue[i]==car_id:
                for j in range(i, my_constant.waiting_area-1):
                    self.waiting_queue[j]=self.waiting_queue[j+1]
                    self.mode_queue[j]=self.mode_queue[j+1]
                self.waiting_queue[my_constant.waiting_area-1]=-1
                self.mode_queue[my_constant.waiting_area-1]=-1
                return

    def re_add(self, car_id, charge_mode,queue_num):
        queue_cnt = 1
        self.del_wating(car_id)
        for i in range(my_constant.waiting_area):
            if self.mode_queue[i] == charge_mode:
                queue_cnt += 1
            if self.waiting_queue[i] == -1:
                self.waiting_queue[i] = car_id
                self.mode_queue[i] = charge_mode
                return 2, queue_cnt, queue_num
    def get_car_position(self, car_id, charge_mode):
        queue_cnt = 0
        for i in range(my_constant.waiting_area):
            if self.mode_queue[i] == charge_mode:
                queue_cnt += 1
            if self.waiting_queue[i] == car_id:
                return queue_cnt
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j]==car_id:
                    return j+1
        return 0
    '''
    def get_car_list(self, car_id):
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j] == car_id:
                    car_list = []
                    self.charge_queue[i][j]=-1
                    for k in range(my_constant.charge_area):
                        if self.charge_queue[i][k]!=-1:
                            car_list.append(self.charge_queue[i][k])
                    self.charge_queue[i][j]=car_id
                    return car_list
    '''
    def check_broken_list(self,charge_mode):
        if charge_mode=='F':
            list_id=0
        else: list_id=1
        if len(self.broken_list[list_id])==0:
            return -1,-1
        new_car=self.broken_list[list_id][0]
        self.broken_list[list_id].pop(0)
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j]==new_car:
                    self.charge_queue[i][j]=-1
        return 0,new_car
    def get_new_charging_car(self, car_id):
        pile_id=0
        position = 0
        charge_mode='T'
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j] == car_id:
                    pile_id=i
                    position=j
                    break
        for i in range(position,my_constant.charge_area-1):
            self.charge_queue[pile_id][i]=self.charge_queue[pile_id][i+1]
        self.charge_queue[pile_id][my_constant.charge_area-1]=-1
        if pile_id < my_constant.fast_pile:
            charge_mode='F'
        rcode, new_car=self.check_broken_list(charge_mode)
        if rcode == -1:
            for i in range(my_constant.waiting_area):
                if self.mode_queue[i] == charge_mode:
                    new_car=self.waiting_queue[i]
                    for j in range(i, my_constant.waiting_area-1):
                        self.waiting_queue[j]=self.waiting_queue[j+1]
                        self.mode_queue[j]=self.mode_queue[j+1]
                    self.waiting_queue[my_constant.waiting_area-1]=-1
                    self.mode_queue[my_constant.waiting_area-1]=-1
                    self.charge_queue[pile_id][position]=new_car
                    return new_car
        else:
            self.charge_queue[pile_id][position]=new_car
        return new_car
    def get_all_car(self):
        return_list=[]
        for i in range(my_constant.pile_num):
            for j in range(my_constant.charge_area):
                if self.charge_queue[i][j]!=-1:
                    return_list.append([self.charge_queue[i][j],i])
        for i in range(my_constant.waiting_area):
            if self.waiting_queue[i]!=-1:
                return_list.append([self.waiting_queue[i],-1])
        return return_list
    def pile_broken(self, pile_id):
        if self.pile_state[pile_id]==my_constant.pile_state.broken:
            return
        return_list=[]
        charge_mode = 1
        if pile_id<my_constant.fast_pile:
            charge_mode = 0
        for i in self.charge_queue[pile_id]:
            if i!=-1:
                self.broken_list[charge_mode].append(i)
                return_list.append(i)
        self.pile_state[pile_id]=my_constant.pile_state.broken
        return return_list
    def pile_recover(self, pile_id):
        if self.pile_state[pile_id]==my_constant.pile_state.idle or self.pile_state[pile_id]==my_constant.pile_state.using:
            return
        return_list=[]
        for i in range(my_constant.charge_area):
            self.charge_queue[pile_id][i] = -2
            self.charge_queue[pile_id][i] = self.get_new_charging_car(-2)
            if self.charge_queue[pile_id][i]!=-1:
                return_list.append(self.charge_queue[pile_id][i])
        self.pile_state[pile_id]=my_constant.pile_state.idle
        return return_list
    def try_get_newposition(self, pile_id):
        if pile_id<my_constant.fast_pile:
            pile_start=0
            pile_end=my_constant.fast_pile
            charge_mode="F"
        else:
            pile_start=my_constant.fast_pile
            pile_end=my_constant.pile_num
            charge_mode="T"
        for j in range(my_constant.charge_area):
            for i in range(pile_start,pile_end):
                if self.pile_state[i]!=my_constant.pile_state.broken and self.pile_state[i]!=my_constant.pile_state.close:
                    if self.charge_queue[i][j]==-1:
                        rcode, new_car=self.check_broken_list(charge_mode)
                        self.charge_queue[i][j]=new_car
                        return rcode, i
        return -1,-1
    pass
