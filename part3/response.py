from django.http import HttpResponse
from part3.models import Queue,my_constant
import time
import json
def create_global():
    global queue
    queue = Queue()
def try_charging(request):
    json_dict = json.loads(request.body)
    car_id = json_dict.get("car_id","")
    request_amount = json_dict.get("request_amount","")
    request_mode = json_dict.get("request_mode","")
    return_json = {"code" : 1, "msg" : "", "data" : ""}
    if car_id == "" or request_amount == "" or request_mode == "":
        return_json["code"] = 0
        return_json["msg"] = "缺少参数"
        return_json["data"] = ""
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    #car_state = get_car_state(car_id)
    #car_capacity = get_car_capacity(car_id)
    #if request_amount>car_capacity:
    #    return_json["code"] = 0
    #    return_json["msg"] = "请求电量超过车辆总电量"
    #    return_json["data"] = ""
    #    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    state, pile_id, queue_num= queue.add_car(car_id, request_mode)
    if state == -1:
        if car_id == "" or request_amount == "" or request_mode == "":
            return_json["code"] = 0
            return_json["msg"] = "充电等候区已满"
            return_json["data"] = ""
            return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    return_json["msg"] = "请求成功"
    #change_request_mode(car_id, request_mode)
    #change_request_amount(car_id, request_amount)
    #if state == 1:
    #    change_car_state(car_id, my_constant.car_state.charging_area)
    #    return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.charging_area,
    #                       "queue_num" : queue_num, "request_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}#get_current_time
    #elif state == 0:
    #    change_car_state(car_id, my_constant.car_state.can_charging)
    #    return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.charging_area,
    #                       "queue_num" : queue_num, "request_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}#get_current_time
    #else:
    #    change_car_state(car_id, my_constant.car_state.wating)
    #    return_json["data"] = {"car_position" : pile_id, "car_state": my_constant.car_state.wating,
    #                       "queue_num" : queue_num, "request_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}#get_current_time
    return_json["data"] = {"car_position" : pile_id, "car_state" : my_constant.car_state.charging_area,
                           "queue_num" : queue_num, "request_time" : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}#get_current_time
    print(return_json)
    return HttpResponse(json.dumps(return_json, ensure_ascii=False))

