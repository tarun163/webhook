from django.urls import path
from . import views

urlpatterns = [
    path('webhook',views.index,name='webhook'),
    path('send',views.send_wa_msg,name='send'),
]