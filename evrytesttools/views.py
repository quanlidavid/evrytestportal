from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from evrytesttools.instanceutil.icdutil import get_sr_icd_info_attrs,sr_create_server


# Create your views here.

def homepage(request):
    template = get_template('index.html')
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)


def icd_page(request):
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

def icd_create_sr_page(request):
    template = get_template('icd_create_sr.html')
    now = datetime.now()
    j_username = request.POST.get('j_username')
    j_password = request.POST.get('j_password')
    tshirtsize_option = request.POST.get('tshirtsize_option')
    hypervisor_option = request.POST.get('hypervisor_option')
    purposeofsr = request.POST.get('purposeofsr')
    if j_username != None and j_password != None:
        if j_username != '' and j_password != '':
            create_sr_info = sr_create_server(tshirtsize_option,hypervisor_option,purposeofsr,j_username,j_password)
    html = template.render(locals())
    return HttpResponse(html)