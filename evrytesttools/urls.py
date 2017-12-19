from django.urls import path
from evrytesttools import views

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^test/$',views.test,name='test'),
    # url(r'^run/$',views.run,name='run'),
    # url(r'^getVIOInfo/$',views.getVIOInfo,name='getVIOInfo'),
    # url(r'^run/logdetails.html$',views.logdetails_page,name='logdetails'),

    path('', views.homepage),
    path('icd_sr/', views.icd_sr_page),
    path('icd_cmdb/', views.icd_cmdb_page),
    path('icd_create_linux_sr/', views.icd_create_linux_sr_page),
    path('icdhistory/<str:table>/',views.icd_history),
    path('vioinfo/',views.vioinfo)
    # path('post/<slug:slug>', showpost),
]