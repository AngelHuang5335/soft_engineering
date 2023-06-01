from django.urls import path
from part1 import login
from part3 import response

urlpatterns = [
    path('login/', login.user_login),
    path('register/', login.user_register),
    path('logout/', login.user_logout),
    path('chargingRequest/', response.try_charging),
    path('queryCarState/', response.get_state),
    path('changeChargingMode/', response.change_mode),
    path('changeChargingAmount/', response.change_amount),
    path('beginCharging/', response.start_charging),
    path('getChargingState/', response.get_charging_state),
    path('endCharging/', response.end_charging),
    #path('changeCapacity/', admin.site.urls),
    #path('getTotalBill/', admin.site.urls),
    #path('getDetailBill/', admin.site.urls),
    #path('getPayBill/', admin.site.urls),
]