from django.db import models

# Create your models here.
class my_constant:
    charge_area = 2
    waiting_area = 6
    fast_pile = 2
    slow_pile = 3
    pile_num = fast_pile + slow_pile
    pass

class queue:
    charge_queue = []
    waiting_queue = []
    def __init__(self):
        self.charge_queue = [[-1 for j in range(my_constant.charge_area)] for i in range(my_constant.pile_num)]
        self.waiting_queue = [-1 for i in range(my_constant.waiting_area)]
    def add_car(self, car_id, charge_mode):
        start_pile_id = 0
        end_pile_id = 2
        if charge_mode=='T':
            start_pile_id = 2
            end_pile_id = my_constant.pile_num
        for j in range(0,my_constant.charge_area):
            for i in range(start_pile_id,end_pile_id):
                if self.charge_queue[i][j] == -1:
                    self.charge_queue[i][j]=car_id
                    return 0,i
        for i in range(0,my_constant.waiting_area):
            if self.waiting_queue[i] == -1:
                self.waiting_queue[i]=car_id
                return 1,i
        return -1,-1
    pass
