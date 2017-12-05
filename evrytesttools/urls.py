from django.urls import path
from evrytesttools.views import homepage,icdpage
from . import views

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^test/$',views.test,name='test'),
    # url(r'^run/$',views.run,name='run'),
    # url(r'^getVIOInfo/$',views.getVIOInfo,name='getVIOInfo'),
    # url(r'^run/logdetails.html$',views.logdetails_page,name='logdetails'),

    path('', homepage),
    path('icd/', icdpage),
    # path('post/<slug:slug>', showpost),
]