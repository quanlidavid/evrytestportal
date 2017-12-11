import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings()


def get_sr_icd_info(srid, j_username, j_password):
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    r = s.get('https://10.180.19.18/maximo/webclient/login/login.jsp?appservauth=true', verify=False)
    soup = BeautifulSoup(r.text, 'html5lib')
    loginstamp = soup.find('input', attrs={'name': 'loginstamp'})['value']

    # s.headers.update({'Referer': 'https://10.180.19.18/maximo/webclient/login/login.jsp?appservauth=true'})

    payload = {'allowinsubframe': 'null', 'j_password': j_password, 'j_username': j_username,
               'localStorage': 'true', 'login': 'jsp', 'loginstamp': loginstamp, 'mobile': 'false'}

    r = s.post('https://10.180.19.18/maximo/j_security_check', data=payload, headers=headers)

    soup = BeautifulSoup(r.text, 'html5lib')
    csrftoken = soup.find('input', attrs={'name': 'csrftokenholder'})['value']
    uisessionid = soup.find('input', attrs={'name': 'uisessionid'})['value']
    r = s.get(
        'https://10.180.19.18/maximo/ui/?event=loadapp&value=viewsr&uisessionid=' + uisessionid + '&csrftoken=' + csrftoken)
    soup = BeautifulSoup(r.text, 'html5lib')
    href = soup.find('a', attrs={'id': 'm6a7dfd2f-lb4'})['href']
    url = ''.join(re.findall(r'"(.*)"', href))
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')
    firsttd = soup.find('td', text=srid)
    parent = firsttd.parent

    sr = parent.contents[1]
    summary = parent.contents[3]
    classification_description = parent.contents[5]
    status = parent.contents[7]
    configuration_item_name = parent.contents[13]

    return {'sr': sr.text, 'summary': summary.text, 'classification_description': classification_description.text,
            'status': status.text, 'configuration_item_name': configuration_item_name.text}


def get_sr_icd_info_attrs(srid, j_username, j_password):
    srid = 'SR' + ''.join(re.findall('\d+', srid))

    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    # login page
    r = s.get('https://10.180.19.18/maximo/webclient/login/login.jsp?appservauth=true', verify=False)
    soup = BeautifulSoup(r.text, 'html5lib')
    loginstamp = soup.find('input', attrs={'name': 'loginstamp'})['value']

    payload = {'allowinsubframe': 'null', 'j_password': j_password, 'j_username': j_username,
               'localStorage': 'true', 'login': 'jsp', 'loginstamp': loginstamp, 'mobile': 'false'}
    # login
    r = s.post('https://10.180.19.18/maximo/j_security_check', data=payload, headers=headers)

    soup = BeautifulSoup(r.text, 'html5lib')
    csrftoken = soup.find('input', attrs={'name': 'csrftokenholder'})['value']
    uisessionid = soup.find('input', attrs={'name': 'uisessionid'})['value']

    # view requests
    r = s.get(
        'https://10.180.19.18/maximo/ui/?event=loadapp&value=viewsr&uisessionid=' + uisessionid + '&csrftoken=' + csrftoken)
    soup = BeautifulSoup(r.text, 'html5lib')
    href = soup.find('a', attrs={'id': 'm6a7dfd2f-lb4'})['href']
    url = ''.join(re.findall(r'"(.*)"', href))
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')
    firsttd = soup.find('td', text=srid)
    parent = firsttd.parent

    sr = parent.contents[1]
    summary = parent.contents[3]
    classification_description = parent.contents[5]
    status = parent.contents[7]
    configuration_item_name = parent.contents[13]

    print(sr.text, summary.text, classification_description.text, status.text, configuration_item_name.text)
    events = [{"type": "setvalue", "targetId": "mb68266fb-tb", "value": srid, "requestType": "ASYNC", "csrftokenholder"
    : csrftoken, "priority": 1}, {"type": "click", "targetId": "mb7327214-pb", "value": "", "requestType"
    : "SYNC", "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'mb68266fb-tb', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    events = [{"type": "click", "targetId": "m6a7dfd2f_tdrow_[C:0]_ttxt-lb[R:0]", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]
    payload = {'csrftoken': csrftoken, 'currentfocus': 'm6a7dfd2f_tdrow_[C:0]_ttxt-lb[R:0]', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    soup = BeautifulSoup(r.text, 'html5lib')
    href = soup.find('a', attrs={'id': 'm3b660ada-lb4'})['href']
    url = ''.join(re.findall(r'"(.*)"', href))
    # get attributes
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')
    try:
        ip = soup.find('td', text='ITDIPADDRESS_EP').parent.contents[7].text
    except Exception as e:
        ip = ''
    try:
        hostname = soup.find('td', text='ITDHOSTNAME').parent.contents[7].text
    except Exception as e:
        hostname = ''
    try:
        customer = soup.find('td', text='ITDCUSTOMER').parent.contents[7].text
    except Exception as e:
        customer = ''
    try:
        disksize = soup.find('td', text='ITDDISK0SIZE').parent.contents[7].text + \
                   soup.find('td', text='ITDDISK0SIZE').parent.contents[9].text
    except Exception as e:
        disksize = ''
    try:
        memsize = soup.find('td', text='ITDMEMORY').parent.contents[7].text + \
                  soup.find('td', text='ITDMEMORY').parent.contents[9].text
    except Exception as e:
        memsize = ''
    try:
        virtualsize = soup.find('td', text='EVRVIRTUALSIZE').parent.contents[7].text
    except Exception as e:
        virtualsize = ''
    try:
        cpusize = soup.find('td', text='EVRVCPUSIZE').parent.contents[7].text
    except Exception as e:
        cpusize = ''
    try:
        hypervisor = soup.find('td', text='ITDHYPERVISOR').parent.contents[7].text
    except Exception as e:
        hypervisor = ''

    # logout
    events = [{"type": "click", "targetId": "titlebar_hyperlink_7-lbsignout", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'titlebar_hyperlink_9-lbsignout', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    return {'sr': sr.text, 'summary': summary.text, 'classification_description': classification_description.text,
            'status': status.text, 'configuration_item_name': configuration_item_name.text, 'ip': ip,
            'hostname': hostname, 'customer': customer, 'disksize': disksize, 'memsize': memsize,
            'virtualsize': virtualsize, 'cpusize': cpusize, 'hypervisor': hypervisor}


def sr_create_server(tshirtsize_option, hypervisor_option, security_zone, purposeofsr, j_username, j_password):
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    # open home
    r = s.get('https://10.180.19.18/maximo/webclient/login/login.jsp?appservauth=true', verify=False)

    # login
    soup = BeautifulSoup(r.text, 'html5lib')
    loginstamp = soup.find('input', attrs={'name': 'loginstamp'})['value']

    payload = {'allowinsubframe': 'null', 'j_password': j_password, 'j_username': j_username,
               'localStorage': 'true', 'login': 'jsp', 'loginstamp': loginstamp, 'mobile': 'false'}

    r = s.post('https://10.180.19.18/maximo/j_security_check', data=payload, headers=headers)

    # open create linux dialog
    soup = BeautifulSoup(r.text, 'html5lib')
    csrftoken = soup.find('input', attrs={'name': 'csrftokenholder'})['value']
    uisessionid = soup.find('input', attrs={'name': 'uisessionid'})['value']

    events = [
        {"type": "launchdialog", "targetId": "m87ab630e-srmnavigator_srmnavigatorctrl", "value": "EVRCCP1583,ITEMSET1",
         "requestType": "SYNC", "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm87ab630e-srmnavigator_srmnavigatorctrl', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    soup = BeautifulSoup(r.text, 'html5lib')
    item = soup.find('input', attrs={'id': 'm362ae120-tb'})['value']
    customer = soup.find('input', attrs={'id': 'mcff97de2-sctextbox_textbox'})['value']
    customername = soup.find('input', attrs={'id': 'mb8fe4d74-sctextbox_textbox'})['value']
    disasterlevelclass = soup.find('input', attrs={'id': 'm269ad8d7-sccombobox_textbox'})['value']
    hostname = soup.find('input', attrs={'id': 'madd01c7b-sctextbox_textbox'})['value']
    operationsystem = soup.find('input', attrs={'id': 'm8f4b0393-sccombobox_textbox'})['value']
    environment = soup.find('input', attrs={'id': 'm614562bf-sccombobox_textbox'})['value']
    backup = soup.find('input', attrs={'id': 'm86fd4fb8-sccombobox_textbox'})['value']
    servicelevel = soup.find('input', attrs={'id': 'm4d05f565-sccombobox_textbox'})['value']
    servicemodel = soup.find('input', attrs={'id': 'm3d6f01ea-sctextbox_textbox'})['value']
    retentionofbackup = soup.find('input', attrs={'id': 'mf1fa7f2e-sccombobox_textbox'})['value']
    storegetier = soup.find('input', attrs={'id': 'm30720120-sccombobox_textbox'})['value']
    serverbemanaged = soup.find('input', attrs={'id': 'md911a415-sccombobox_textbox'})['value']
    hypervisor = soup.find('input', attrs={'id': 'mc767514d-sccombobox_textbox'})['value']

    print(item)
    print(customer)
    print(customername)
    print(hostname)
    print(operationsystem)
    print(disasterlevelclass)
    print(environment)
    print(backup)
    print(servicelevel)
    print(servicemodel)
    print(retentionofbackup)
    print(storegetier)
    print(serverbemanaged)
    print(hypervisor)

    # open security zone dialog and select zone
    events = [
        {"type": "click", "targetId": "mdad72ced-sctextbox_detailbutton", "value": "ciname", "requestType": "SYNC",
         "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'mdad72ced-sctextbox_textbox', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    events = [{"type": "click", "targetId": security_zone, "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': security_zone, 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    soup = BeautifulSoup(r.text, "lxml-xml")
    securityzone = BeautifulSoup(soup.text, 'html5lib').find('input', attrs={'id': 'mdad72ced-sctextbox_textbox'})[
        'value']
    print(securityzone)

    # Select T-Shirt Size
    events = [
        {"type": "setvalue", "targetId": "m112f9630-sctextbox_textbox", "value": purposeofsr, "requestType": "ASYNC",
         "csrftokenholder": csrftoken, "priority": 1},
        {"type": "click", "targetId": "m785e53fe-sccombobox_dropimage", "value": "combobox",
         "requestType": "SYNC",
         "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm785e53fe-sccombobox_textbox', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    events = [{"type": "click", "targetId": "defaultDialogCR_menus", "value": tshirtsize_option, "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm785e53fe-sccombobox_textbox', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    soup = BeautifulSoup(r.text, "lxml-xml")
    tshirtsize = BeautifulSoup(soup.text, 'html5lib').find('input', attrs={'id': 'm785e53fe-sccombobox_textbox'})[
        'value']
    vcpusize = BeautifulSoup(soup.text, 'html5lib').find('input', attrs={'id': 'mf596368-sccombobox_textbox'})['value']
    memsize = BeautifulSoup(soup.text, 'html5lib').find('input', attrs={'id': 'me8e14e6f-sccombobox_textbox'})['value']
    print(tshirtsize)
    print(vcpusize)
    print(memsize)

    # select hypervior
    if hypervisor_option != 'VMWare_OPTION':
        events = [
            {"type": "click", "targetId": "mc767514d-sccombobox_dropimage", "value": "combobox", "requestType": "SYNC",
             "csrftokenholder": csrftoken}]
        payload = {'csrftoken': csrftoken, 'currentfocus': 'mc767514d - sccombobox_textbox', 'requesttype': 'SYNC',
                   'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
                   'uisessionid': uisessionid, 'events': str(events)}
        r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

        events = [
            {"type": "click", "targetId": "defaultDialogCR_menus", "value": hypervisor_option, "requestType": "SYNC",
             "csrftokenholder": csrftoken}]
        payload = {'csrftoken': csrftoken, 'currentfocus': 'mc767514d - sccombobox_textbox', 'requesttype': 'SYNC',
                   'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
                   'uisessionid': uisessionid, 'events': str(events)}
        r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

        soup = BeautifulSoup(r.text, "lxml-xml")
        hypervisor = BeautifulSoup(soup.text, 'html5lib').find('input', attrs={'id': 'mc767514d-sccombobox_textbox'})[
            'value']
        print(hypervisor)

    # Order now
    events = [{"type": "click", "targetId": "m92ee8002-srmpushbutton_pushbutton", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm92ee8002-srmpushbutton_pushbutton', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    soup = BeautifulSoup(r.text, 'html5lib')
    srsubmitedinfo = soup.find('label', attrs={'id': 'm3373ba3e-lb'}).text
    print(srsubmitedinfo)

    # logout
    events = [{"type": "click", "targetId": "titlebar_hyperlink_7-lbsignout", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm92ee8002-srmpushbutton_pushbutton', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    return {'item': item, 'customer': customer, 'customername': customername, 'disasterlevelclass ': disasterlevelclass,
            'hostname': hostname, 'operationsystem': operationsystem, 'environment': environment, 'backup'
            : backup, 'servicelevel': servicelevel, 'servicemodel': servicemodel,
            'retentionofbackup': retentionofbackup, 'storegetier': storegetier, 'serverbemanaged': serverbemanaged,
            'hypervisor': hypervisor, 'securityzone': securityzone, 'tshirtsize': tshirtsize, 'vcpusize': vcpusize,
            'memsize': memsize, 'srsubmitedinfo': srsubmitedinfo}


def get_cmdb_icd_info_spec(hostname, j_username, j_password):
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    # login page
    r = s.get('https://10.180.19.18/maximo/webclient/login/login.jsp?appservauth=true', verify=False)
    soup = BeautifulSoup(r.text, 'html5lib')
    loginstamp = soup.find('input', attrs={'name': 'loginstamp'})['value']

    payload = {'allowinsubframe': 'null', 'j_password': j_password, 'j_username': j_username,
               'localStorage': 'true', 'login': 'jsp', 'loginstamp': loginstamp, 'mobile': 'false'}
    # login
    r = s.post('https://10.180.19.18/maximo/j_security_check', data=payload, headers=headers)

    soup = BeautifulSoup(r.text, 'html5lib')
    csrftoken = soup.find('input', attrs={'name': 'csrftokenholder'})['value']
    uisessionid = soup.find('input', attrs={'name': 'uisessionid'})['value']

    # configuration items
    events = [{"type": "changeapp", "targetId": "titlebar-tb_gotoButton", "value": "CI", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'm87ab630e - srmnavigator_srmnavigatorctrl',
               'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    r = s.get(
        'https://10.180.19.18/maximo/ui/?event=loadapp&value=ci&uisessionid=' + uisessionid + '&csrftoken=' + csrftoken)

    # filter
    events = [{"type": "setvalue", "targetId": "m6a7dfd2f_tfrow_[C:1]_txt-tb", "value": hostname,
               "requestType": "ASYNC", "csrftokenholder": csrftoken, "priority": 1},
              {"type": "setvalue", "targetId": "m6a7dfd2f_tfrow_[C:7]_txt-tb", "value": "y", "requestType": "ASYNC",
               "csrftokenholder": csrftoken, "priority": 1},
              {"type": "filterrows", "targetId": "m6a7dfd2f_tbod_tfrow-tr", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]
    payload = {'csrftoken': csrftoken, 'currentfocus': 'm6a7dfd2f_tfrow_[C:7]_txt-tb', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    # configuration item
    events = [{"type": "click", "targetId": "m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:0]", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]
    payload = {'csrftoken': csrftoken, 'currentfocus': 'm6a7dfd2f_tdrow_[C:1]_ttxt - lb[R:0]', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    # ci details
    events = [{"type": "click", "targetId": "mbf28cd64-tab", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]
    payload = {'csrftoken': csrftoken, 'currentfocus': 'm98d76e99 - tb', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)
    soup = BeautifulSoup(r.text, 'html5lib')
    href = soup.find('a', attrs={'id': 'mb47137f1-lb4'})['href']
    url = ''.join(re.findall(r'"(.*)"', href))

    # get attributes
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')

    try:
        name = soup.find('td', text='COMPUTERSYSTEM_NAME').parent.contents[3].text
    except Exception as e:
        name = ''
    try:
        memorysize = soup.find('td', text='COMPUTERSYSTEM_MEMORYSIZE').parent.contents[3].text + \
                     soup.find('td', text='COMPUTERSYSTEM_MEMORYSIZE').parent.contents[5].text
    except Exception as e:
        memorysize = ''
    try:
        tshirtsize = soup.find('td', text='COMPUTERSYSTEM_TSHIRTSIZE').parent.contents[3].text
    except Exception as e:
        tshirtsize = ''
    try:
        numcpus = soup.find('td', text='COMPUTERSYSTEM_NUMCPUS').parent.contents[3].text
    except Exception as e:
        numcpus = ''

    # logout
    events = [{"type": "click", "targetId": "titlebar_hyperlink_7-lbsignout", "value": "", "requestType": "SYNC",
               "csrftokenholder": csrftoken}]

    payload = {'csrftoken': csrftoken, 'currentfocus': 'titlebar_hyperlink_9-lbsignout', 'requesttype': 'SYNC',
               'localStorage': 'true', 'responsetype': 'text/xml', 'scrollleftpos': 0, 'scrolltoppos': 0,
               'uisessionid': uisessionid, 'events': str(events)}
    r = s.post('https://10.180.19.18/maximo/ui/maximo.jsp', data=payload)

    return {'hostname': hostname, 'name': name, 'memorysize': memorysize, 'tshirtsize': tshirtsize,
            'numcpus': numcpus}


if __name__ == '__main__':
    # print(sr_create_server("small.1_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test1','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("small.2_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test2','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("small.3_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test3','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("medium.1_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test4','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("medium.2_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test5','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("medium.3_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test6','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("large.1_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test7','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("large.2_OPTION",'VMWare_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test8','feilibj@cn.ibm.com','QAZqaz!@#123'))
    # print(sr_create_server("small.1_OPTION", 'HyperV_OPTION', 'lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test1', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("small.2_OPTION", 'HyperV_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]', 'Automation test9', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("small.3_OPTION", 'HyperV_OPTION', 'lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test10', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("medium.1_OPTION", 'HyperV_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]', 'Automation test11', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("medium.2_OPTION", 'HyperV_OPTION','lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]', 'Automation test12', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("medium.3_OPTION", 'HyperV_OPTION', 'lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test13', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("large.1_OPTION", 'HyperV_OPTION', 'lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test14', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    # print(sr_create_server("large.2_OPTION", 'HyperV_OPTION', 'lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]','Automation test15', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
    print(get_cmdb_icd_info_spec('EVR-CCD1-L01322', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
'''
large.1_OPTION
large.2_OPTION
medium.1_OPTION
medium.2_OPTION
medium.3_OPTION
small.1_OPTION
small.2_OPTION
small.3_OPTION
'''
'''HyperV_OPTION
VMWare_OPTION

HyperV
VMWare
'''
'''
lookup_page2_tdrow_[C:1]_ttxt-lb[R:0]
lookup_page2_tdrow_[C:1]_ttxt-lb[R:1]
lookup_page2_tdrow_[C:1]_ttxt-lb[R:2]
lookup_page2_tdrow_[C:1]_ttxt-lb[R:3]
lookup_page2_tdrow_[C:1]_ttxt-lb[R:4]

LS-EVR-NO-CCD1-CONF-SECU1
LS-EVR-NO-CCD1-CONF-FRON1
LS-EVR-NO-CCD1-PUBL-FRON1
LS-EVR-NO-CCD1-PUBL-PROT1
LS-EVR-NO-CCD1-CONF-PROT1
'''
#     # srid = 'SR5480'
#     # srid='SR5317'
#     info = get_sr_icd_info_attrs('SR5317', 'feilibj@cn.ibm.com', 'QAZqaz!@#123')
#     print(info['summary'])
#     print(get_sr_icd_info_attrs('SR5480', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
