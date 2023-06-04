from django.urls import path
from part1 import login
from part2 import operate
from part3 import response

urlpatterns = [
    path('login', login.user_login),
    path('register', login.user_register),
    path('logout', login.user_logout),
    path('chargingRequest', response.try_charging),
    path('queryCarState', response.get_state),
    path('changeChargingMode', response.change_mode),
    path('changeChargingAmount', response.change_amount),
    path('beginCharging', response.start_charging),
    path('getChargingState', response.get_charging_state),
    path('endCharging', response.end_charging),
    path('changeCapacity', operate.change_capacity),
    path('getTotalBill', operate.get_total_bill),
    path('getDetailBill', operate.get_detail_bill),
    path('getPayBill', operate.get_pay_bill),
]