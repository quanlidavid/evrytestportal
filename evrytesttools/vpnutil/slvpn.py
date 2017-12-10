from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,subprocess

def connectslvpn():
    res = subprocess.call('ping 10.180.19.18')
    if res==1:
        driver = webdriver.Ie()
        driver.get("https://vpn.osl01.softlayer.com/prx/000/http/localhost/welcome/welcome.html")
        time.sleep(5)
        elem = driver.find_element_by_id('login-button')
        elem.click()
        time.sleep(40)

if __name__ == '__main__':
    connectslvpn()





