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
    srid = srid.upper()
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
    return {'sr': sr.text, 'summary': summary.text, 'classification_description': classification_description.text,
            'status': status.text, 'configuration_item_name': configuration_item_name.text, 'ip': ip,
            'hostname': hostname, 'customer': customer, 'disksize': disksize, 'memsize': memsize,
            'virtualsize': virtualsize, 'cpusize': cpusize}


if __name__ == '__main__':
    # srid = 'SR5480'
    # srid='SR5317'
    info = get_sr_icd_info_attrs('SR5317', 'feilibj@cn.ibm.com', 'QAZqaz!@#123')
    print(info['summary'])
    print(get_sr_icd_info_attrs('SR5480', 'feilibj@cn.ibm.com', 'QAZqaz!@#123'))
