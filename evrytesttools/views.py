from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from evrytesttools.instanceutil.icdutil import loginfailedException, sridnotfoundException, get_sr_icd_info_attrs, \
    sr_create_server_linux, \
    get_cmdb_icd_info_spec
from evrytesttools import models
from evrytesttools.vpnutil import slvpn
from evrytesttools.instanceutil import vioutil, preproductlinux,rundeckutil


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
    elif table == 'RundeckEecord':
        queryset = models.RundeckRecord.objects.all()
    elif table == 'EndtoendRecord':
        queryset = models.EndtoendRecord.objects.all()
    html = template.render(locals())
    return HttpResponse(html)


def linuxinstanceinfo(request):
    template = get_template('linuxinstanceinfo.html')
    now = datetime.now()
    endtoendID = request.POST.get('endtoendID')
    hypervisor = request.POST.get('hypervisor')
    customer = request.POST.get('customer')
    instancehostname = request.POST.get('instancehostname')
    instanceip = request.POST.get('instanceip')
    username = request.POST.get('username')
    password = request.POST.get('password')
    id = ''
    if hypervisor != None and customer != None and instancehostname != None and instanceip != None:
        linuxinstance = preproductlinux.linux(username, password)
        linuxinstanceinfo = linuxinstance.getInstanceInfo(hypervisor, customer, instancehostname, instanceip)
        linuxinforecord = models.LinuxInfoRecord.objects.create_LinuxInfoRecord(linuxinstanceinfo)
        linuxinforecord.save()
        id = linuxinforecord.id
        try:
            endtoend_entry = models.EndtoendRecord.objects.get(endtoendID=endtoendID)
            endtoend_entry.linuxinstanceID = id
            endtoend_entry.save()
        except:
            pass
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
    endtoendID = request.POST.get('endtoendID')
    domain = request.POST.get('domain')
    instances__filter__q = request.POST.get('instances__filter__q')
    username = request.POST.get('username')
    password = request.POST.get('password')
    id = ''
    if username != None and password != None and instances__filter__q != None and domain != None:
        try:
            instanceinfo = vioutil.getInstanceInfoOfVIO(domain, instances__filter__q, username, password)
            viorecord = models.VIORecord.objects.create_VIORecord(instanceinfo)
            viorecord.save()
            id = viorecord.id
        except vioutil.viologinfailedException as e:
            errormessage = e.mesg
        try:
            endtoend_entry = models.EndtoendRecord.objects.get(endtoendID=endtoendID)
            endtoend_entry.vioID = id
            endtoend_entry.save()
        except:
            pass

    html = template.render(locals())
    return HttpResponse(html)

def rundeckinfo(request):
    template = get_template('rundeckinfo.html')
    now = datetime.now()
    endtoendID = request.POST.get('endtoendID')
    srid = request.POST.get('srid')
    username = request.POST.get('username')
    password = request.POST.get('password')
    icd_max = request.POST.get('icd_max')
    private_max = request.POST.get('private_max')
    id = ''
    if username != None and password != None and srid != None:
        try:
            rundeckJobInfo = rundeckutil.get_rundeck_info(srid, username, password,icd_max,private_max)
            rundeckrecord = models.RundeckRecord.objects.create_RundeckRecord(rundeckJobInfo)
            rundeckrecord.save()
            id = rundeckrecord.id
        except rundeckutil.rundeckloginfailedException as e:
            errormessage = e.mesg
        try:
            endtoend_entry = models.EndtoendRecord.objects.get(endtoendID=endtoendID)
            endtoend_entry.rundeckID = id
            endtoend_entry.save()
        except:
            pass
    html = template.render(locals())
    return HttpResponse(html)

def generatetestlog(request,endtoendID):
    template = get_template('linuxdetaillog.html')
    now = datetime.now()
    log = ''
    try:
        one_entry = models.EndtoendRecord.objects.get(endtoendID=endtoendID)
        log = '================================================End to End Test Log: '+endtoendID+' ===================================================\n\n'
        if (one_entry.createSRID != '0'):
            createsr_entry = models.SRCreateServerLinuxRecord.objects.get(id=one_entry.createSRID)
            log = log + "================================================Created SR Log===================================================\n\n"
            for f in models.SRCreateServerLinuxRecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(createsr_entry, f.name)) + "\n"
        if (one_entry.querySRID != '0'):
            querysr_entry = models.QuerySRRecord.objects.get(id=one_entry.querySRID)
            log = log + "\n\n\n\n\n================================================Query SR Log===================================================\n\n"
            for f in models.QuerySRRecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(querysr_entry, f.name)) + "\n"
        if (one_entry.cmdbID != '0'):
            cmdb_entry = models.QueryCMDBRecord.objects.get(id=one_entry.cmdbID)
            log = log + "\n\n\n\n\n================================================Query CMDB Log===================================================\n\n"
            for f in models.QueryCMDBRecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(cmdb_entry, f.name)) + "\n"
        if (one_entry.vioID != '0'):
            vio_entry = models.VIORecord.objects.get(id=one_entry.vioID)
            log = log + "\n\n\n\n\n================================================Query VIO Log===================================================\n\n"
            for f in models.VIORecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(vio_entry, f.name)) + "\n"
        if (one_entry.rundeckID != '0'):
            rundeck_entry = models.RundeckRecord.objects.get(id=one_entry.rundeckID)
            log = log + "\n\n\n\n\n================================================Query Rundeck Log===================================================\n\n"
            for f in models.RundeckRecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(rundeck_entry, f.name)) + "\n"
        if (one_entry.linuxinstanceID != '0'):
            instance_entry = models.LinuxInfoRecord.objects.get(id=one_entry.linuxinstanceID)
            log = log + "\n\n\n\n\n================================================Linux instance Log===================================================\n\n"
            for f in models.LinuxInfoRecord._meta.get_fields():
                log = log + f.name + " : " + str(getattr(instance_entry, f.name)) + "\n"
    except:
        log = log + 'This end to end test do not exist. '

    html = template.render(locals())
    return HttpResponse(html)

