from django.urls import path
from part1 import login
from part3 import response

urlpatterns = [
    path('login/', login.admin_login),
    #path('powerOn/', admin.site.urls),
    path('logout/', login.admin_logout),
    #path('powerOff/', admin.site.urls),
    path('setPrice/', response.set_price),
    #path('queryPileState/', admin.site.urls),
    path('queryQueueState/', response.get_queue_state),
    #path('queryPileAmount/', admin.site.urls),
    #path('queryReport/', admin.site.urls),
    path('create_price/',response.add_price)
]