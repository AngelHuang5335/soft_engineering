from django.db import models
from part3.models import my_constant


# Create your models here.
class Car(models.Model):
    car_id = models.CharField(max_length=50)
    car_capacity = models.FloatField(null=True)
    car_state = models.CharField(max_length=50, null=True)
    request_amount = models.FloatField(null=True)
    request_mode = models.CharField(max_length=50, null=True)
    queue_num = models.CharField(max_length=50, null=True)
    request_time = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.car_id

    class Meta:
        # 定义数据表名
        db_table = 'Car'
        # 表别名
        verbose_name = '车辆'
        # 表别名复数，用于英文显示
        verbose_name_plural = verbose_name


class Pile():
    def __init__(self,pile_id):
        self.pile_id=pile_id
        self.working_state=my_constant.pile_state.close
        self.charge_mode="F" if pile_id<my_constant.fast_pile else "T"
        self.broken_time=0

    def __str__(self):
        return self.pile_id
'''
    class Meta:
        # 定义数据表名
        db_table = 'Pile'
        # 表别名
        verbose_name = '充电桩'
        # 表别名复数，用于英文显示
        verbose_name_plural = verbose_name
'''


class Bill(models.Model):
    bill_id = models.CharField(max_length=50, null=True)
    bill_date = models.DateField(null=True, default=None)
    charge_amount = models.FloatField(null=True)
    charge_duration = models.FloatField(null=True)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    total_charge_fee = models.FloatField(null=True)
    total_service_fee = models.FloatField(null=True)
    total_fee = models.FloatField(null=True)
    pay_state = models.IntegerField(null=True, default=0)

    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    pile_id = models.IntegerField(null=True)

    def __str__(self):
        return self.bill_id

    class Meta:
        # 定义数据表名
        db_table = 'Bill'
        # 表别名
        verbose_name = '账单'
        # 表别名复数，用于英文显示
        verbose_name_plural = verbose_name
