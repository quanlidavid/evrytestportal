import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

def getInstanceInfoOfVIO(domain, instances__filter__q, username='e214375', password='Passw0rd2018'):
    fake_email = username
    fake_password = password

    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'https://vioppr.cloud.cosng.net/auth/login/',
    }
    r = s.get('https://vioppr.cloud.cosng.net/auth/login/', verify=False)
    soup = BeautifulSoup(r.text, 'html5lib')
    csrfmiddlewaretoken = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
    region = soup.find('input', attrs={'id': 'id_region'})['value']  # locate the data
    # print(csrfmiddlewaretoken)
    # print(region)

    payload = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'domain': domain, 'fake_email': fake_email,
               'fake_password': fake_password, 'password': password, 'region': region, 'username': username}
    r = s.post('https://vioppr.cloud.cosng.net/auth/login/', data=payload, headers=headers)

    # print(r.text)

    r = s.get('https://vioppr.cloud.cosng.net/project/instances/')
    soup = BeautifulSoup(r.text, 'html5lib')
    csrfmiddlewaretoken = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']

    payload = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'instances__filter__q': instances__filter__q,
               'instances__filter__q_field': 'name'}
    # print(csrfmiddlewaretoken)
    r = s.post('https://vioppr.cloud.cosng.net/project/instances/', data=payload, headers=headers)
    # print(r.text)

    soup = BeautifulSoup(r.text, 'html5lib')
    tbody = soup.find('tbody')
    tr = tbody.contents[1]

    # logout
    r = s.get('https://vioppr.cloud.cosng.net/auth/logout/')

    instancename = ''.join(tr.contents[2].stripped_strings)
    imagename = ''.join(tr.contents[3].stripped_strings)
    ip = ''.join(tr.contents[4].stripped_strings)
    size = ''.join(tr.contents[5].find('a').stripped_strings)
    status = ''.join(tr.contents[7].stripped_strings)
    availabilityzone = ''.join(tr.contents[8].stripped_strings)
    powerstate = ''.join(tr.contents[10].stripped_strings)

    return {'instancename': instancename, 'imagename': imagename, 'ip': ip, 'size': size, 'status': status,
            'availabilityzone': availabilityzone, 'powerstate': powerstate}


if __name__ == '__main__':
    # print(getInstanceInfoOfVIO('EVR-NO-CCD1', 'evr-ccd1-l01262'))
    print(getInstanceInfoOfVIO('EVR-NO-CCD1', 'test-vm-12847'))
