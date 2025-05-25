from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('request-dump/', views.request_dump, name='request-dump'),
    path('sw-deploy/', views.sw_deploy, name='sw-deploy'),
    path('svc-deploy/', views.svc_deploy, name='svc-deploy'),
    path('svc-server-up/', views.svc_server_up, name='svc-server-up'),
    path('svc-ddos/', views.svc_ddos, name='svc-ddos'),
    path('svc-get-all/<int:device_id>', views.svc_get_all, name='svc-get-all'),
    path('svc-persist/<int:device_id>', views.svc_persist, name='svc-persist'),
    path('sot-populate/', views.sot_populate, name='sot-populate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
