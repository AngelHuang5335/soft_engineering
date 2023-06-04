from django.urls import path
from part1 import login
from part2 import operate
from part3 import response

urlpatterns = [
    path('login', login.admin_login),
    path('powerOn', operate.power_on),
    path('logout', login.admin_logout),
    path('powerOff', operate.power_off),
    path('setPrice', response.set_price),
    path('queryPileState', operate.query_pile_state),
    path('queryQueueState', response.get_queue_state),
    path('queryPileAmount', response.query_pile_num),
    path('queryReport', operate.query_report),
    path('create_price',response.add_price)
]