import requests
from bs4 import BeautifulSoup
import urllib3
import re, json

urllib3.disable_warnings()


class rundeckloginfailedException(BaseException):
    def __init__(self, mesg="Login failed. Maybe username/password was wrong."):
        self.mesg = mesg

    def __str__(self):
        return self.mesg


class sridnotfoundException(BaseException):
    def __init__(self, srid):
        self.mesg = srid + " not found. Maybe it is not created by this user, so you have not access to see it."

    def __str__(self):
        return self.mesg


def get_rundeck_info(srid, j_username, j_password, icd_max=30, privatecloud_max=100):
    srid = 'SR' + ''.join(re.findall('\d+', srid))
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    # login page
    r = s.get('https://rundeckpprha.cloud.cosng.net/user/login', verify=False)

    payload = {'j_password': j_password, 'j_username': j_username}
    # login
    r = s.post('https://rundeckpprha.cloud.cosng.net/user/j_security_check', data=payload, headers=headers)

    # open ICD
    r = s.get('https://rundeckpprha.cloud.cosng.net/project/ICD/activity?max=' + icd_max)
    soup = BeautifulSoup(r.text, 'html5lib')
    # status: FAILED,'SUCCEEDED'
    dispatchers = soup.find_all('tr', attrs={'class': 'link'})

    icdDispatcherJobID = 'NotFound'
    icdDispatcherJobStatus = 'NotFound'
    icdDispatcherJobDuration = 'NotFound'
    workorderid = 'NotFound'
    privatecloudJobID = 'NotFound'
    privatecloudJobStatus = 'NotFound'
    privatecloudJobDuration = 'NotFound'

    for item in dispatchers:
        try:
            icdDispatcherJob_icd_input = item.find('span', attrs={'class': 'optvalue'}).text
        except Exception as e:
            icdDispatcherJob_icd_input = None
        if icdDispatcherJob_icd_input != None and bool(re.search(srid, icdDispatcherJob_icd_input, re.IGNORECASE)):
            workorderid = json.loads(icdDispatcherJob_icd_input)['PublishITDWOTASK']['ITDWOTASKSet']['WORKORDER'][
                'WORKORDERID']
            icdDispatcherJobStatus = item.find('i')['data-execstate']
            icdDispatcherJobID = item.find('a')['href'].split('/')[-1]
            icdDispatcherJobDuration = item.find('span', {'class': 'ago'}).text

            # open privatecloud
            r = s.get('https://rundeckpprha.cloud.cosng.net/project/PrivateCloud/activity?max=' + privatecloud_max)
            soup = BeautifulSoup(r.text, 'html5lib')
            events = soup.find_all('tr', attrs={'class': 'link'})
            for item in events:
                privatecloudEventargs = item.find('div', attrs={'class': 'argstring-scrollable'}).text
                if bool(re.search(workorderid, privatecloudEventargs, re.IGNORECASE)):
                    privatecloudJobStatus = item.find('i')['data-execstate']
                    privatecloudJobID = item.find('a')['href'].split('/')[-1]
                    privatecloudJobDuration = item.find('span', {'class': 'ago'}).text
                    break
            break

    # logout
    r = s.get('https://rundeckpprha.cloud.cosng.net/user/logout')

    return {'srid': srid, 'icdDispatcherJobID': icdDispatcherJobID, 'icdDispatcherJobStatus': icdDispatcherJobStatus,
            'icdDispatcherJobDuration': icdDispatcherJobDuration, 'workorderid': workorderid,
            'privatecloudJobID': privatecloudJobID, 'privatecloudJobStatus': privatecloudJobStatus,
            'privatecloudJobDuration': privatecloudJobDuration}


if __name__ == '__main__':
    print(get_rundeck_info('sr6012', 'e214375', 'Passw0rd2018'))
    print(get_rundeck_info('SR6168', 'e214375', 'Passw0rd2018'))
    print(get_rundeck_info('6149', 'e214375', 'Passw0rd2018'))
    print(get_rundeck_info('6009', 'e214375', 'Passw0rd2018'))
