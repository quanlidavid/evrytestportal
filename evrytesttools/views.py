from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from evrytesttools.instanceutil.icdutil import get_sr_icd_info_attrs


# Create your views here.

def homepage(request):
    template = get_template('index.html')
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)


def icdpage(request):
    template = get_template('icd.html')
    now = datetime.now()
    srid = request.POST.get('srid')
    j_username = request.POST.get('j_username')
    j_password = request.POST.get('j_password')
    if srid != None and j_username != None and j_password != None:
        if srid != '' and j_username != '' and j_password != '':
            sr_icd_info = get_sr_icd_info_attrs(srid, j_username, j_password)
    html = template.render(locals())
    return HttpResponse(html)
