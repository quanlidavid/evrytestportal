from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,subprocess

def connectslvpn():
    res = os.popen('ping 10.180.19.18')
    str = res.read()

    if 'TTL=' not in str:
        driver = webdriver.Ie()
        driver.get("https://vpn.osl01.softlayer.com/prx/000/http/localhost/welcome/welcome.html")
        time.sleep(5)
        name = driver.find_element_by_id('username')
        name.clear()
        name.send_keys("evryicd_quan")
        time.sleep(2)
        password = driver.find_element_by_id('password')
        password.clear()
        password.send_keys("Testadmin@123")
        time.sleep(2)
        elem = driver.find_element_by_id('login-button')
        elem.click()
        time.sleep(40)

if __name__ == '__main__':
    connectslvpn()





