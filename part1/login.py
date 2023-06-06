from . import models
from django.http import HttpResponse
import json
from django.contrib.auth.hashers import make_password, check_password
import jwt
import time
from part2.operate import create_car, get_car_capacity

user_list = models.User_list()


def judge_user_online(token):
    return user_list.judge_user_online(token)


def judge_user_token(token):
    return user_list.judge_user_token(token)


def judge_admin_token(token):
    return user_list.judge_admin_token(token)


def get_user_id(car_id):
    return models.User.objects.get(car_id=car_id).id


def generate_token(username):
    d = {
        # 公共声明
        'exp': time.time() + 3000,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': 'Issuer',  # (Issuer) 指明此token的签发者

        # 私有声明
        'data': {
            'username': username,
            'timestamp': time.time()
        }
    }

    jwt_encode = jwt.encode(d, '123456', algorithm='HS256')
    return jwt_encode


def user_register(request):
    json_dict = json.loads(request.body)
    username = json_dict.get('user_name')
    password = json_dict.get('password')
    car_id = json_dict.get('car_id')
    car_capacity = json_dict.get('car_capacity')
    if username and password and car_id and car_capacity:
        if car_id == 0:
            return HttpResponse(json.dumps({'code': 0, 'message': '车辆编号非法'}, ensure_ascii=False))
        if models.User.objects.filter(username=username).exists():
            return HttpResponse(json.dumps({'code': 0, 'message': '用户名已存在'}, ensure_ascii=False))
        if models.User.objects.filter(car_id=car_id).exists():
            return HttpResponse(json.dumps({'code': 0, 'message': '车辆编号已存在'}, ensure_ascii=False))
        password = make_password(password)
        token = generate_token(username)
        user = models.User(username=username, password=password, car_id=car_id, is_admin=0,
                           token=token)
        user_list.user_online(user)
        user.save()
        user_id = user.id
        create_car(car_id, car_capacity)
        return_json = {'code': 1, 'message': '注册成功',
                       'data': {'user_id': user_id, 'user_name': username, 'token': token, 'car_id': car_id,
                                'car_capacity': car_capacity}}
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({'code': 0, 'message': '所有选项均不能为空'}, ensure_ascii=False))


def user_login(request):
    json_dict = json.loads(request.body)
    username = json_dict.get('user_name')
    password = json_dict.get('password')
    if username and password:
        if models.User.objects.filter(username=username).exists():
            user = models.User.objects.get(username=username)
            get_user_id(user.car_id)
            if check_password(password, user.password):
                if 0:#user_list.check_user_online(user):
                    return HttpResponse(json.dumps({'code': 0, 'message': '用户已登录'}, ensure_ascii=False))
                else:
                    user_list.user_online(user)
                    return_json = {'code': 1, 'message': '登录成功',
                                   'data': {'user_id': user.id, 'user_name': username, 'token': user.token,
                                            'car_id': user.car_id,
                                            'car_capacity': get_car_capacity(user.car_id)}}
                    return HttpResponse(json.dumps(return_json, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 0, 'message': '用户名与密码不匹配'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'message': '用户名不存在'}, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({'code': 0, 'message': '用户名与密码不能为空'}, ensure_ascii=False))


def user_logout(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if user_list.judge_user_online(token):
        flag, _ = user_list.judge_user_token(token)
        if flag:
            user_list.user_offline(token)
            return HttpResponse(json.dumps({'code': 1, 'message': '成功登出'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'message': '用户未登录'}, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({'code': 0, 'message': '用户未登录'}, ensure_ascii=False))


def admin_login(request):
    json_dict = json.loads(request.body)
    password = json_dict.get('password')
    if password is None:
        return HttpResponse(json.dumps({'code': 0, 'message': '密码不能为空'}, ensure_ascii=False))
    elif password == '123456':
        if models.User.objects.filter(is_admin=1).exists():
            token = models.User.objects.get(is_admin=1).token
            if 0:#user_list.judge_user_online(token):
                return HttpResponse(json.dumps({'code': 0, 'message': '用户已登录'}, ensure_ascii=False))
            else:
                admin = models.User.objects.get(is_admin=1)
                user_list.user_online(admin)
                return_json = {'code': 1, 'message': '登录成功', 'data': {'token': token}}
                return HttpResponse(json.dumps(return_json, ensure_ascii=False))
        else:
            token = generate_token('admin')
            admin = models.User(password='123456', is_admin=1, token=token)
            admin.save()
            user_list.user_online(admin)
            return_json = {'code': 1, 'message': '登录成功', 'data': {'token': token}}
        return HttpResponse(json.dumps(return_json, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({'code': 0, 'message': '密码错误'}, ensure_ascii=False))


def admin_logout(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if user_list.judge_user_online(token):
        if user_list.judge_admin_token(token):
            user_list.user_offline(token)
            return HttpResponse(json.dumps({'code': 1, 'message': '成功登出'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'message': '用户未登录'}, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({'code': 0, 'message': '用户未登录'}, ensure_ascii=False))


