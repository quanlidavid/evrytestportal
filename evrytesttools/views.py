from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from evrytesttools.instanceutil.icdutil import loginfailedException, sridnotfoundException, get_sr_icd_info_attrs, \
    sr_create_server_linux, \
    get_cmdb_icd_info_spec
from evrytesttools import models
from evrytesttools.vpnutil import slvpn
from evrytesttools.instanceutil import vioutil, preproductlinux


# Create your views here.

def homepage(request):
    template = get_template('index.html')
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)


def icd_sr_page(request):
    template = get_template('icd_sr.html')
    now = datetime.now()
    srid = request.POST.get('srid')
    j_username = request.POST.get('j_username')
    j_password = request.POST.get('j_password')
    if srid != None and j_username != None and j_password != None:
        if srid != '' and j_username != '' and j_password != '':
            slvpn.connectslvpn()
            try:
                sr_icd_info = get_sr_icd_info_attrs(srid, j_username, j_password)
                qsr = models.QuerySRRecord.objects.create_QuerySRRecord(sr_icd_info)
                qsr.save()
            except loginfailedException as e:
                errormessage = e.mesg
            except sridnotfoundException as e:
                errormessage = e.mesg
    html = template.render(locals())
    return HttpResponse(html)


def icd_cmdb_page(request):
    template = get_template('icd_cmdb.html')
    now = datetime.now()
    hostname = request.POST.get('hostname')
    j_username = request.POST.get('j_username')
    j_password = request.POST.get('j_password')
    if hostname != None and j_username != None and j_password != None:
        if hostname != '' and j_username != '' and j_password != '':
            slvpn.connectslvpn()
            try:
                sr_cmdb_info = get_cmdb_icd_info_spec(hostname, j_username, j_password)
                qcmdb = models.QueryCMDBRecord.objects.create_QueryCMDBRecord(sr_cmdb_info)
                qcmdb.save()
            except loginfailedException as e:
                errormessage = e.mesg
    html = template.render(locals())
    return HttpResponse(html)


def icd_create_linux_sr_page(request):
    template = get_template('icd_create_linux_sr.html')
    now = datetime.now()
    j_username = request.POST.get('j_username')
    j_password = request.POST.get('j_password')
    tshirtsize_option = request.POST.get('tshirtsize_option')
    security_zone = request.POST.get('security_zone')
    hypervisor_option = request.POST.get('hypervisor_option')
    purposeofsr = request.POST.get('purposeofsr')
    if j_username != None and j_password != None:
        if j_username != '' and j_password != '':
            slvpn.connectslvpn()
            try:
                create_linux_sr_info = sr_create_server_linux(tshirtsize_option, hypervisor_option, security_zone,
                                                              purposeofsr,
                                                              j_username, j_password)
                create_linux = models.SRCreateServerLinuxRecord.objects.create_SRCreateServerLinuxRecord(
                    create_linux_sr_info)
                create_linux.save()
            except loginfailedException as e:
                errormessage = e.mesg
    html = template.render(locals())
    return HttpResponse(html)


def icd_history(request, table):
    template = get_template('icd_history.html')
    now = datetime.now()
    if table == 'QuerySRRecord':
        queryset = models.QuerySRRecord.objects.all()
    elif table == 'QueryCMDBRecord':
        queryset = models.QueryCMDBRecord.objects.all()
    elif table == 'SRCreateServerLinuxRecord':
        queryset = models.SRCreateServerLinuxRecord.objects.all()
    elif table == 'VIORecord':
        queryset = models.VIORecord.objects.all()
    elif table == 'LinuxInfoRecord':
        queryset = models.LinuxInfoRecord.objects.all()
    html = template.render(locals())
    return HttpResponse(html)


def linuxinstanceinfo(request):
    template = get_template('linuxinstanceinfo.html')
    now = datetime.now()
    hypervisor = request.POST.get('hypervisor')
    customer = request.POST.get('customer')
    instancehostname = request.POST.get('instancehostname')
    instanceip = request.POST.get('instanceip')
    if hypervisor != None and customer != None and instancehostname != None and instanceip != None:
        linuxinstance = preproductlinux.linux('e214375', 'Passw0rd2018')
        linuxinstanceinfo = linuxinstance.getInstanceInfo(hypervisor, customer, instancehostname, instanceip)
        linuxinforecord = models.LinuxInfoRecord.objects.create_LinuxInfoRecord(linuxinstanceinfo)
        linuxinforecord.save()
    html = template.render(locals())
    return HttpResponse(html)


def linuxdetailslog(request):
    template = get_template('linuxdetaillog.html')
    now = datetime.now()
    logpath = request.GET.get('logpath')
    if logpath != None:
        with open(logpath, 'r') as file:
            log = file.read()
    html = template.render(locals())
    return HttpResponse(html)


def vioinfo(request):
    template = get_template('vioinfo.html')
    now = datetime.now()
    domain = request.POST.get('domain')
    instances__filter__q = request.POST.get('instances__filter__q')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username != None and password != None and instances__filter__q != None and domain != None:
        try:
            instanceinfo = vioutil.getInstanceInfoOfVIO(domain, instances__filter__q, username, password)
            viorecord = models.VIORecord.objects.create_VIORecord(instanceinfo)
            viorecord.save()
        except vioutil.viologinfailedException as e:
            errormessage = e.mesg
    html = template.render(locals())
    return HttpResponse(html)
