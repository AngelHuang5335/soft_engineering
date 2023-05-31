from django.urls import path
from part3 import response

urlpatterns = [
    #path('login/', admin.site.urls),
    #path('register/', admin.site.urls),
    #path('logout/', admin.site.urls),
    path('chargingRequest/', response.try_charging),
    #path('queryCarState/', admin.site.urls),
    #path('changeChargingMode/', admin.site.urls),
    #path('changeChargingAmount/', admin.site.urls),
    #path('beginCharging/', admin.site.urls),
    #path('getChargingState/', admin.site.urls),
    #path('endCharging/', admin.site.urls),
    #path('changeCapacity/', admin.site.urls),
    #path('getTotalBill/', admin.site.urls),
    #path('getDetailBill/', admin.site.urls),
    #path('getPayBill/', admin.site.urls),
]