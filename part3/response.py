from django.http import HttpResponse
from part3.models import Queue,my_constant,Price
from part1 import login
from part2 import operate
import json

#def __init__():
queue = Queue()
new_price = Price.objects.all()
my_constant.low_price=new_price[0].low_price
my_constant.mid_price=new_price[0].mid_price
my_constant.high_price=new_price[0].high_price
print(new_price)
print(my_constant.low_price,my_constant.mid_price,my_constant.high_price)
def try_charging(request):
    json_dict = json.loads(request.body)
    car_id = json_dict.get("car_id","")
    request_amount = json_dict.get("request_amount","")
    request_mode = json_dict.get("request_mode","")
    return_json = {"code" : 1, "message" : "请求成功", "data" : ""}
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    if car_id == "" or request_amount == "" or request_mode == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car_state = operate.get_car_state(car_id)
    request_amount=float(request_amount)
    if car_state==my_constant.car_state.end_charging:
        return_json["code"] = 0
        return_json["message"] = "请先支付之前的订单"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    if request_amount<=0:
        return_json["code"] = 0
        return_json["message"] = "请求电量小于等于0"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car_capacity = operate.get_car_capacity(car_id)
    if request_amount>car_capacity:
        return_json["code"] = 0
        return_json["message"] = "请求电量超过车辆总电量"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    state, pile_id, queue_num= queue.add_car(car_id, request_mode)
    if state == -1:
        return_json["code"] = 0
        return_json["message"] = "充电等候区已满"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    operate.change_request_mode(car_id, request_mode)
    operate.change_request_amount(car_id, request_amount)
    operate.change_queue_num(car_id, queue_num)
    operate.change_request_time(car_id)
    request_time = operate.get_request_time(car_id)
    if state == 1:
        operate.change_car_state(car_id, my_constant.car_state.charging_area)
        return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.charging_area,
                           "queue_num" : queue_num, "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S')}#get_current_time
    elif state == 0:
        operate.change_car_state(car_id, my_constant.car_state.can_charging)
        return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.charging_area,
                           "queue_num" : queue_num, "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S')}#get_current_time
    else:
        operate.change_car_state(car_id, my_constant.car_state.wating)
        return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.wating,
                           "queue_num" : queue_num, "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S')}#get_current_time
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def get_state(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "请求成功", "data" : ""}
    car_id = json_dict.get("car_id","")
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile_id = queue.get_pile_id(car_id)
    request_mode = operate.get_request_mode(car_id)
    car_position = queue.get_car_position(car_id, request_mode)
    car_state = operate.get_car_state(car_id)
    queue_num = operate.get_queue_num(car_id)
    request_time = operate.get_request_time(car_id)
    request_amount = operate.get_request_amount(car_id)
    return_json["data"]={"car_position": car_position, "car_state": car_state, "queue_num": queue_num,
                         "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S'), "pile_id": pile_id,
                         "request_mode": request_mode, "request_amount":request_amount}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
def change_amount(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "请求成功", "data" : ""}
    car_id = json_dict.get("car_id", "")
    request_amount = json_dict.get("request_amount", "")
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    if car_id == "" or request_amount == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    request_amount=float(request_amount)
    if request_amount<=0:
        return_json["code"] = 0
        return_json["message"] = "请求电量小于等于0"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car_state = operate.get_car_state(car_id)
    car_capacity = operate.get_car_capacity(car_id)
    if request_amount>car_capacity:
        return_json["code"] = 0
        return_json["message"] = "请求电量超过车辆总电量"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    if car_state==my_constant.car_state.wating:
        operate.change_request_amount(car_id,request_amount)
        return_json["code"] = 1
        return_json["message"] = "修改成功"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return_json["code"] = 0
    return_json["message"] = "在充电区或正在充电"
    return_json["data"] = ""
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
def change_mode(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "请求成功", "data" : ""}
    car_id = json_dict.get("car_id", "")
    request_mode = json_dict.get("request_mode", "")
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    if car_id == "" or request_mode == "":
        return_json["code"] = 0
        return_json["message"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car_state = operate.get_car_state(car_id)
    if car_state!=my_constant.car_state.wating:
        return_json["code"] = 0
        return_json["message"] = "在充电区或正在充电"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    queue_num=operate.get_queue_num(car_id)
    state, pile_id, queue_num = queue.re_add(car_id, request_mode, queue_num)

    operate.change_request_mode(car_id, request_mode)
    #operate.change_queue_num(car_id, queue_num)
    #operate.change_request_time(car_id)
    request_time=operate.get_request_time(car_id)
    operate.change_car_state(car_id, my_constant.car_state.wating)
    return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.wating,
                           "queue_num" : queue_num, "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S')}
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def start_charging(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "开始充电", "data" : ""}
    car_id = json_dict.get("car_id", "")
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    pile_id = queue.get_pile_id(car_id)
    car_state = operate.get_car_state(car_id)
    if car_state == my_constant.car_state.can_charging:
        operate.change_car_state(car_id,my_constant.car_state.charging)
        operate.create_bill(car_id, pile_id)
        car_list = queue.get_car_list(car_id)
        for i in car_list:
            operate.change_car_state(i, my_constant.car_state.charging_area)
        operate.change_pile_state(pile_id,my_constant.pile_state.using)
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return_json["code"]=0
    return_json["message"]="充电桩正在使用中"
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
def get_charging_state(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "查询成功", "data" : ""}
    car_id = json_dict.get("car_id", "")
    state,token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return_json["data"]=operate.get_charging_bill(car_id)
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
def end_car_charging(car_id):
    return_json = {"code" : 1, "message" : "充电结束", "data" : ""}
    car_state = operate.get_car_state(car_id)
    if car_state == my_constant.car_state.idle or car_state == my_constant.car_state.end_charging:
        return_json["code"]=0
        return_json["message"]="充电已结束"
        return return_json
    if car_state == my_constant.car_state.wating:
        queue.del_wating(car_id)
        operate.change_car_state(car_id, my_constant.car_state.idle)
    elif car_state == my_constant.car_state.charging_area:
        operate.change_car_state(car_id, my_constant.car_state.idle)
        tmp_car=queue.get_new_charging_car(car_id)
        if tmp_car!=-1:
            operate.change_car_state(tmp_car, my_constant.car_state.charging_area)
    elif car_state == my_constant.car_state.can_charging:
        operate.change_car_state(car_id, my_constant.car_state.idle)
        tmp_car=queue.get_new_charging_car(car_id)
        if tmp_car!=-1:
            operate.change_car_state(tmp_car, my_constant.car_state.can_charging)
    elif car_state ==my_constant.car_state.charging:
        operate.change_car_state(car_id, my_constant.car_state.end_charging)
        operate.update_bill(car_id,0)
        operate.change_pile_state(queue.get_pile_id(car_id),my_constant.pile_state.idle)
        car_list = queue.get_car_list(car_id)
        for i in car_list:
            operate.change_car_state(i, my_constant.car_state.can_charging)
        tmp_car=queue.get_new_charging_car(car_id)
        if tmp_car!=-1:
            operate.change_car_state(tmp_car, my_constant.car_state.can_charging)
    return return_json
def end_charging(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "充电结束", "data" : ""}
    car_id = json_dict.get("car_id", "")
    state, token_car_id=login.judge_user_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0 or token_car_id!=car_id:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return_json = end_car_charging(car_id)
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def get_queue_state(request):
    return_json = {"code" : 1, "message" : "查询成功", "data" : ""}
    state=login.judge_admin_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    car_list=queue.get_all_car()
    return_json["data"]=[]
    for i,j in car_list:
        tmp_dict = {}
        tmp_dict["user_id"]=login.get_user_id(i)
        tmp_dict["car_capacity"]=operate.get_car_capacity(i)
        tmp_dict["request_amount"]=operate.get_request_amount(i)
        tmp_dict["wait_time"]=str(operate.get_waiting_time(i))
        tmp_dict["pile_id"]=j
        tmp_dict["car_state"]=operate.get_car_state(i)
        tmp_dict["request_mode"]=operate.get_request_mode(i)
        return_json["data"].append(tmp_dict)
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def add_price(request):
    return_json = {"code" : 1, "message" : "修改成功", "data" : ""}
    price=Price()
    price.save()
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def set_price(request):
    json_dict = json.loads(request.body)
    return_json = {"code" : 1, "message" : "修改成功", "data" : ""}
    state=login.judge_admin_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    low_price = json_dict.get("low_price", "")
    mid_price = json_dict.get("mid_price", "")
    high_price = json_dict.get("high_price", "")
    new_price = Price.objects.all()
    new_price.update(low_price=low_price, mid_price=mid_price, high_price=high_price)
    my_constant.low_price=low_price
    my_constant.mid_price=mid_price
    my_constant.high_price=high_price
    print(my_constant.low_price,my_constant.mid_price,my_constant.high_price)
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

def pile_broken(pile_id):
    car_list=queue.pile_broken(pile_id)
    for i in car_list:
        car_state=operate.get_car_state(i)
        if car_state==my_constant.car_state.charging:
            operate.update_bill(i,1)
            operate.change_car_state(i,my_constant.car_state.charging_area)
        elif car_state==my_constant.car_state.charging_area or car_state==my_constant.car_state.can_charging:
            operate.change_car_state(i,my_constant.car_state.charging_area)

def pile_recover(pile_id):
    car_list=queue.pile_recover(pile_id)
    for i in car_list:
        operate.change_car_state(i,my_constant.car_state.can_charging)
def query_pile_num(request):
    return_json = {"code" : 1, "message" : "查询成功", "data" : ""}
    state=login.judge_admin_token(request.META.get("HTTP_AUTHORIZATION"))
    if state==0:
        return_json["code"] = 0
        return_json["message"] = "token验证错误"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    data_dict={"amount":my_constant.pile_num,"fast_pile_id":"","slow_pile_id":""}
    fast_pile_id=[]
    slow_pile_id=[]
    for i in range(my_constant.fast_pile):
        fast_pile_id.append({"pile_id":i})
    for i in range(my_constant.fast_pile,my_constant.pile_num):
        slow_pile_id.append({"pile_id":i})
    data_dict["fast_pile_id"]=fast_pile_id
    data_dict["slow_pile_id"]=slow_pile_id
    return_json["data"]=data_dict
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
