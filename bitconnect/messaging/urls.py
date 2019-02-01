from django.conf.urls import url
from . import views

app_name = 'messaging'
urlpatterns = [
    url(r'^$' , views.index , name = 'index') , 
    url(r'^message/(?P<mem_id>[0-9]+)$' , views.message , name = 'message') ,
]