from part1.clock import get_simulated_time, user_end_charge, user_charge
from part2.models import Car, Bill, Pile
from part3 import response
from part3.models import my_constant
from django.http import HttpResponse
from datetime import datetime
import json
import random

pile_list=[]
for i in range(my_constant.pile_num):
    pile_list.append(Pile(i))

def create_car(carid, carcapacity):
    Car.objects.create(car_id=carid, car_capacity=carcapacity, car_state=my_constant.car_state.idle)


def create_bill(carid, pileid):
    simulated_time = get_simulated_time()
    car = Car.objects.filter(car_id=carid)[0]
    Bill.objects.create(bill_id=simulated_time + str(carid),
                        bill_date=datetime.strptime(simulated_time,"%Y-%m-%d %H:%M:%S").date(),
                        start_time=datetime.strptime(simulated_time,"%Y-%m-%d %H:%M:%S"),
                        car_id=car, pile_id=pileid)
    if car.request_mode == "F":
        charge_time = car.request_amount / my_constant.slow_charging_v
    elif car.request_mode == "T":
        charge_time = car.request_amount / my_constant.fast_charging_v
    user_charge(charge_time, carid)


def calculate_charge_fee(hou, minu, sec):
    mid_time=0
    high_time=0
    if hou < 7:
        low_time = hou + minu / 60 + sec / 3600
    elif hou < 10:
        low_time = 7.0
        mid_time = hou - 7.0 + minu / 60 + sec / 3600
    elif hou < 15:
        low_time = 7.0
        mid_time = 3.0
        high_time = hou - 10.0 + minu / 60 + sec / 3600
    elif hou < 18:
        low_time = 7.0
        mid_time = 3.0 + hou - 15.0 + minu / 60 + sec / 3600
        high_time = 5.0
    elif hou < 21:
        low_time = 7.0
        mid_time = 6.0
        high_time = 5.0 + hou - 18.0 + minu / 60 + sec / 3600
    elif hou < 23:
        low_time = 7.0
        mid_time = 6.0 + hou - 21.0 + minu / 60 + sec / 3600
        high_time = 8.0
    else:
        low_time = 7.0 + hou - 23.0 + minu / 60 + sec / 3600
        mid_time = 8.0
        high_time = 8.0
    return (my_constant.low_price * low_time + my_constant.mid_price * mid_time + my_constant.high_price * high_time)


def update_bill(carid, sign):
    car = Car.objects.filter(car_id=carid)[0]
    bill = Bill.objects.filter(car_id=car).last()
    starttime = bill.start_time
    starttime=starttime.replace(tzinfo=None)
    endtime=datetime.strptime(get_simulated_time(), "%Y-%m-%d %H:%M:%S")
    endtime=endtime.replace(tzinfo=None)
    duration = (endtime - starttime).seconds / 3600
    if car.request_mode == "F":
        amount = duration * my_constant.slow_charging_v
    elif car.request_mode == "T":
        amount = duration * my_constant.fast_charging_v
    if sign == 1:
        car.request_amount = car.request_amount - amount
        car.save()
    service_fee = amount * my_constant.service_price
    if endtime.date() == starttime.date():
        charge_fee = calculate_charge_fee(endtime.hour, endtime.minute, endtime.second) - \
                     calculate_charge_fee(starttime.hour, starttime.minute, starttime.second)
    else:
        charge_fee = (endtime.date() - starttime.date()).days * calculate_charge_fee(24, 0, 0) + \
                     calculate_charge_fee(endtime.hour, endtime.minute, endtime.second) - \
                     calculate_charge_fee(starttime.hour, starttime.minute, starttime.second)
    bill.charge_amount = amount
    bill.charge_duration = duration
    bill.end_time = endtime
    bill.total_charge_fee = charge_fee
    bill.total_service_fee = service_fee
    bill.total_fee = charge_fee + service_fee
    bill.save()
    user_end_charge(carid)


def get_car_state(carid):
    return Car.objects.filter(car_id=carid)[0].car_state


def get_car_capacity(carid):
    return Car.objects.filter(car_id=carid)[0].car_capacity


def get_request_mode(carid):
    return Car.objects.filter(car_id=carid)[0].request_mode

def get_request_amount(carid):
    return Car.objects.filter(car_id=carid)[0].request_amount

def get_queue_num(carid):
    return Car.objects.filter(car_id=carid)[0].queue_num


def get_request_time(carid):
    return Car.objects.filter(car_id=carid)[0].request_time


def get_charging_bill(carid):
    car = Car.objects.filter(car_id=carid)[0]
    bill = Bill.objects.filter(car_id=car).last()
    if bill.end_time == None:
        end_time=None
    else:
        end_time=bill.end_time.strftime('%Y-%m-%d %H:%M:%S')
    return {"car_id": carid, "bill_date": bill.bill_date.strftime('%Y-%m-%d'), "bill_id": bill.bill_id, "pile_id": bill.pile_id,
            "charge_amount": bill.charge_amount, "charge_duration": bill.charge_duration, "start_time":
                bill.start_time.strftime('%Y-%m-%d %H:%M:%S'), "end_time": end_time, "total_charge_fee": bill.total_charge_fee,
            "total_service_fee": bill.total_service_fee, "total_fee": bill.total_fee}


def change_car_state(carid, carstate):
    car = Car.objects.filter(car_id=carid)[0]
    car.car_state = carstate
    car.save()


def change_request_mode(carid, requestmode):
    car = Car.objects.filter(car_id=carid)[0]
    car.request_mode = requestmode
    car.save()


def change_request_amount(carid, requestamount):
    car = Car.objects.filter(car_id=carid)[0]
    car.request_amount = requestamount
    car.save()


def change_queue_num(carid, queuenum):
    car = Car.objects.filter(car_id=carid)[0]
    car.queue_num = queuenum
    car.save()


def change_request_time(carid):
    car = Car.objects.filter(car_id=carid)[0]
    car.request_time = get_simulated_time()
    car.save()


def change_pile_state(pileid, pilestate):
    pile=pile_list[pileid]
    pile.working_state=pilestate


def get_total_bill(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    carid = json_dict.get("car_id", "")
    billdate = json_dict.get("bill_date", "")
    if carid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    lst = []
    car = Car.objects.filter(car_id=carid)[0]
    if billdate=="" or billdate is None:
        bills = Bill.objects.filter(car_id=car)
    else:
        bills = Bill.objects.filter(car_id=car, bill_date=billdate)
    print(bills)
    for bill in bills:
        if bill.charge_duration != None:
            lst.append({"car_id": carid, "bill_date": bill.bill_date.strftime('%Y-%m-%d'), "bill_id": bill.bill_id, "pile_id": bill.pile_id,
                    "start_time": bill.start_time.strftime('%Y-%m-%d %H:%M:%S'), "end_time": bill.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "total_fee": bill.total_fee, "pay_state": bill.pay_state})
    return_json["data"] ={"bill_list": lst}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def change_capacity(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    carid = json_dict.get("car_id", "")
    carcapacity = json_dict.get("car_capacity", "")
    if carid == "" or carcapacity is None:
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car = Car.objects.filter(car_id=carid)[0]
    car.car_capacity = carcapacity
    car.save()
    return_json["data"] = {"car_capacity": carcapacity}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def get_detail_bill(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    billid = json_dict.get("bill_id", "")
    if billid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    bill = Bill.objects.filter(bill_id=billid)[0]
    return_json["data"] = {"car_id": bill.car_id.car_id, "bill_date": bill.bill_date.strftime('%Y-%m-%d'), "bill_id": billid,
                           "pile_id": bill.pile_id, "charge_amount": bill.charge_amount, "charge_duration":
                               bill.charge_duration, "start_time": bill.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                           "end_time": bill.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                           "total_charge_fee": bill.total_charge_fee, "total_service_fee": bill.total_service_fee,
                           "total_fee": bill.total_fee, "pay_state": bill.pay_state}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def get_pay_bill(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    billid = json_dict.get("bill_id", "")
    if billid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    bill = Bill.objects.filter(bill_id=billid)[0]
    bill.pay_state = 1
    change_car_state(bill.car_id.car_id,my_constant.car_state.idle)
    bill.save()
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def power_on(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    pileid = json_dict.get("pile_id", "")
    if pileid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile = pile_list[pileid]
    if pile.working_state == my_constant.pile_state.close or pile.working_state == my_constant.pile_state.broken:
        pile.working_state = my_constant.pile_state.idle
        response.pile_recover(pileid)
    else:
        return_json["code"] = 0
        if pile.working_state == my_constant.pile_state.idle:
            return_json["message"] = "充电桩已打开"
        if pile.working_state == my_constant.pile_state.using:
            return_json["message"] = "充电桩使用中"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def power_off(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    pileid = json_dict.get("pile_id", "")
    if pileid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile = pile_list[pileid]
    if pile.working_state == my_constant.pile_state.idle:
        pile.working_state = my_constant.pile_state.close
        response.pile_broken(pileid)
    else:
        return_json["code"] = 0
        if pile.working_state == my_constant.pile_state.close:
            return_json["message"] = "充电桩已关闭"
        if pile.working_state == my_constant.pile_state.using:
            return_json["message"] = "充电桩使用中"
        if pile.working_state == my_constant.pile_state.broken:
            return_json["message"] = "充电桩已损坏"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def query_pile_state(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    pileid = json_dict.get("pile_id", "")
    if pileid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile = pile_list[pileid]
    bills = Bill.objects.filter(pile_id=pileid)
    totalChargeNum = 0
    totalChargeTime = 0.0
    totalCapacity = 0.0
    for bill in bills:
        totalChargeNum += 1
        if bill.charge_duration != None:
            totalChargeTime += bill.charge_duration
            totalCapacity += bill.charge_amount
    return_json["data"] = {"workingState": pile.working_state, "totalChargeNum": totalChargeNum,
                           "totalChargeTime": totalChargeTime, "totalCapacity": totalCapacity,
                           "charge_mode": pile.charge_mode}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def query_report(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    pileid = json_dict.get("pile_id", "")
    start_date = json_dict.get("start_date", "")
    end_date = json_dict.get("end_date", "")
    if pileid == "" or start_date == "" or end_date == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    bills = Bill.objects.filter(pile_id=pileid, bill_date__gte=start_date, bill_date__lte=end_date)
    total_charge_num = 0
    total_charge_time = total_capacity = total_charge_fee = total_service_fee = total_fee = 0.0
    for bill in bills:
        total_charge_num += 1
        total_charge_time += bill.charge_duration
        total_capacity += bill.charge_amount
        total_charge_fee += bill.total_charge_fee
        total_service_fee += bill.total_service_fee
        total_fee += bill.total_fee
    return_json["data"] = {"total_charge_num": total_charge_num, "total_charge_time": total_charge_time,
                           "total_capacity": total_capacity, "total_charge_fee": total_charge_fee,
                           "total_service_fee": total_service_fee, "total_fee": total_fee, "start_date": start_date,
                           "end_date": end_date}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))


def get_waiting_time(car_id):
    last_time=get_request_time(car_id)
    last_time=last_time.replace(tzinfo=None)
    new_time=datetime.strptime(get_simulated_time(), "%Y-%m-%d %H:%M:%S")
    new_time=new_time.replace(tzinfo=None)
    return new_time - last_time

def pile_crash(request):
    json_dict = json.loads(request.body)
    return_json = {"code": 1, "message": "请求成功", "data": ""}
    pileid = json_dict.get("pile_id", "")
    if pileid == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile = pile_list[pileid]
    if pile.working_state == my_constant.pile_state.idle or pile.working_state == my_constant.pile_state.using:
        pile.working_state = my_constant.pile_state.broken
        response.pile_broken(pileid)
    else:
        return_json["code"] = 0
        if pile.working_state == my_constant.pile_state.close:
            return_json["message"] = "充电桩已关闭"
        if pile.working_state == my_constant.pile_state.broken:
            return_json["message"] = "充电桩已损坏"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
