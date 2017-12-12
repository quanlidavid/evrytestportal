from django.urls import path
from evrytesttools.views import homepage,icd_sr_page,icd_create_linux_sr_page,icd_cmdb_page,icd_history
from . import views

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^test/$',views.test,name='test'),
    # url(r'^run/$',views.run,name='run'),
    # url(r'^getVIOInfo/$',views.getVIOInfo,name='getVIOInfo'),
    # url(r'^run/logdetails.html$',views.logdetails_page,name='logdetails'),

    path('', homepage),
    path('icd_sr/', icd_sr_page),
    path('icd_cmdb/', icd_cmdb_page),
    path('icd_create_linux_sr/', icd_create_linux_sr_page),
    path('icdhistory/<str:table>/',icd_history)
    # path('post/<slug:slug>', showpost),
]