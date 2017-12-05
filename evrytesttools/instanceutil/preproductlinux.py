import paramiko
import time
import shutil
import logging
import logging.config
import re
import os


class linux():
    def __init__(self, username='e214375', password='Passw0rd2018'):
        self.rundeckServers = ['146.213.160.116', '146.213.160.117', '146.213.160.118']
        self.username = username
        self.password = password

        self.logger = logging.getLogger("evrylog")
        self.logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt="%Y-%m-%d %H:%M:%S")
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        if os.path.exists('logs/') == False:
            os.mkdir('logs/')
        self.logfilepath = 'logs/' + 'Pre-Pro-Linux' + '-' + time.strftime("%Y%m%d_%H-%M-%S", time.gmtime()) + '.log'
        if os.path.exists(self.logfilepath):
            os.remove(self.logfilepath)

        filehandler = logging.FileHandler(filename=self.logfilepath, encoding="utf-8")
        filehandler.setLevel(logging.INFO)
        fmter = logging.Formatter(fmt="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
        filehandler.setFormatter(fmter)
        self.logger.addHandler(filehandler)

    def getlogfilepath(self):
        return self.logfilepath

    def connectToRundeckServer(self):
        paramiko.util.log_to_file('syslogin.log')
        self.ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return self.createConnectionToRundeckServers()

    def createConnectionToRundeckServers(self):
        connected = False
        for i in range(0, len(self.rundeckServers)):
            try:
                self.ssh.connect(hostname=self.rundeckServers[i], username=self.username, password=self.password)
                self.logger.info('Created connection to rundeck server: ' + self.rundeckServers[i])
                connected = True
                break
            except Exception as e:
                self.logger.error('Created connection to rundeck server:' + self.rundeckServers[i] + ' failed.')
        return connected

    def runCommand(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        self.logger.info(stdout.read().decode())

    def closeConnection(self):
        self.ssh.close()
        self.logger.info('Connection to rundeck server closed.')

    def createChannel(self):
        self.channel = self.ssh.invoke_shell()
        self.channel.settimeout(60)
        resp = ''
        resp = self.channel.recv(65535).decode()
        resp = resp.strip()
        self.logger.info(resp)

    def closeChannel(self):
        self.channel.close()

    def runCommandInChannel(self, command):
        self.channel.send(command)
        time.sleep(5)
        resp = ''
        recv = self.channel.recv(65535)
        resp = recv.decode()
        resp = resp.strip()
        self.logger.info(resp)
        return resp

    def getPasswordOfInstanceByName(self, hypervisor, customer, instancehostname):
        self.createChannel()
        self.runCommandInChannel('export VAULT_ADDR=http://127.0.0.1:8200\n')
        self.runCommandInChannel('vault auth -method=ldap username=e214375\n')
        self.runCommandInChannel('Passw0rd2018\n')
        result = self.runCommandInChannel(
            'vault read secret/OS/' + hypervisor + '/' + customer + '/' + instancehostname + '\n')
        self.closeChannel()
        password = ''.join(re.findall(r'password\s+(.*?)\s+', result))
        return password

    def SSHToInstance(self, instanceIP, password):
        self.instanceIP = instanceIP
        resp = self.runCommandInChannel('ssh root@' + instanceIP + '\n')
        if resp.endswith('password:'):
            self.runCommandInChannel(password + '\n')
        else:
            self.runCommandInChannel('yes' + '\n')
            self.runCommandInChannel(password + '\n')

    def getHOSTNAMEofTestServer(self):
        result = self.runCommandInChannel('hostname\n')
        hostname = ''.join(re.findall('hostname\s+(.*)\s+', result))
        return hostname

    def getIPconfigofTestServer(self):
        result = self.runCommandInChannel('ifconfig\n')
        ip = ''.join(re.findall(r'inet\s+(.*)\s+netmask', result)[0])
        return ip

    def getCPUofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' cat /proc/cpuinfo\n'))
        # cmd = '''cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l\n'''
        result = self.runCommandInChannel('cat /proc/cpuinfo\n')
        cupnumber = len(re.findall(r'physical id', result))
        return cupnumber

    def getMEMofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' cat /proc/meminfo\n'))
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' free -h\n'))
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+'  free -h|grep Mem|cut -d : -f 2|cut -d G -f 1\n'))
        # cmd = ''' free -h|grep Mem|awk '{printf$2"\\n"}'\n'''
        result = self.runCommandInChannel('free -h\n')
        mem = ''.join(re.findall(r'Mem:\s+(.*?)\s+', result))
        return mem

    def getDISKofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' lsblk\n'))
        result = self.runCommandInChannel('lsblk\n')
        disk = ''.join(re.findall(r'sda.*\s+(.*?G).*disk', result))
        return disk

    def getDNSofTestServer(self):
        result = self.runCommandInChannel('ping www.google.com -c 5\n')
        linenumber = len(re.findall(r'\d+ bytes from .* ms', result))
        if linenumber == 5:
            return 'pass'
        else:
            return 'fail'

    def getNTPofTestServer(self):
        result = self.runCommandInChannel('timedatectl\n')
        timezone = ''.join(re.findall(r'Time zone:\s+(.*)\s+\(', result))
        return timezone

    def getITMINFOofTestServer(self):
        result1 = self.runCommandInChannel('ps -ef|grep ITM --color=never\n')
        runningProcessNumber = len(re.findall(r'IBM/ITM', result1))
        result2 = self.runCommandInChannel('/opt/IBM/ITM/bin/cinfo -r\n')
        runningProdNumber = len(re.findall(r'running', result2))
        result3 = self.runCommandInChannel('/opt/IBM/ITM/bin/cinfo -o\n')
        runningInstanceNumber = len(re.findall(r'Instance', result3))
        if runningProcessNumber == 3 and runningProdNumber == 2 and runningInstanceNumber == 2:
            return 'pass'
        else:
            return 'fail'

    def getBigfixINFOofTestServer(self):
        result1 = self.runCommandInChannel('ps -ef|grep BESClient --color=never\n')
        runningProcessNumber = len(re.findall(r'/BESClient/bin/BESClient', result1))
        result2 = self.runCommandInChannel('/etc/init.d/besclient status\n')
        runningProdNumber = len(re.findall(r'running', result2))
        result3 = self.runCommandInChannel('cat /var/opt/BESClient/besclient.config\n')
        if runningProcessNumber == 1 and runningProcessNumber == 1:
            return 'pass'
        else:
            return 'fail'

    def getInstanceInfo(self, hypervisor, customer, instancehostname, instanceip):
        if self.connectToRundeckServer():
            print('rundeck server connected.')
        else:
            print('rundeck server connect failed.')
        instancepassword = self.getPasswordOfInstanceByName(hypervisor, customer, instancehostname)
        self.createChannel()
        self.SSHToInstance(instanceip, instancepassword)
        Hostname = self.getHOSTNAMEofTestServer()
        print("Hostname = " + Hostname)
        IP = self.getIPconfigofTestServer()
        print('IP = ' + str(IP))
        CPUnumber = self.getCPUofTestServer()
        print('CPU number = ' + str(CPUnumber))
        MEM = self.getMEMofTestServer()
        print('Memory = ' + MEM)
        Disk = self.getDISKofTestServer()
        print('Disk = ' + Disk)
        NTPTimeZone = self.getNTPofTestServer()
        print('NTP Timezone = ' + NTPTimeZone)
        DNSstatus = self.getDNSofTestServer()
        print("DNS status = " + DNSstatus)
        ITMINFO = self.getITMINFOofTestServer()
        print("ITM = " + ITMINFO)
        BigfixINFO = self.getBigfixINFOofTestServer()
        print("Bigfix = " + BigfixINFO)

        self.closeChannel()
        self.closeConnection()
        return {'Hostname': Hostname, 'IP': IP, 'CPUnumber': CPUnumber, 'MEM': MEM, 'Disk': Disk,
                'NTPTimeZone': NTPTimeZone, 'DNSstatus': DNSstatus, 'ITMINFO': ITMINFO, 'BigfixINFO': BigfixINFO}

    if __name__ == '__main__':
        # linux = linux('e214375','Passw0rd2018')
        # if linux.connectToRundeckServer():
        #     print('rundeck server connected.')
        # else:
        #     print('rundeck server connect failed.')
        # password = linux.getPasswordOfInstanceByName('VMWare','EVR-NO-CCD1','evr-ccd1-l01257')
        # linux.createChannel()
        # linux.SSHToInstance('10.114.27.106',password)
        # Hostname = linux.getHOSTNAMEofTestServer()
        # print("Hostname = " + Hostname)
        # IP = linux.getIPconfigofTestServer()
        # print('IP = ' + str(IP))
        # CPUnumber = linux.getCPUofTestServer()
        # print('CPU number = ' + str(CPUnumber))
        # MEM = linux.getMEMofTestServer()
        # print('Memory = ' + MEM)
        # Disk = linux.getDISKofTestServer()
        # print('Disk = ' + Disk)
        # NTPTimeZone = linux.getNTPofTestServer()
        # print('NTP Timezone = ' + NTPTimeZone)
        # DNSstatus = linux.getDNSofTestServer()
        # print("DNS status = " + DNSstatus)
        # ITMINFO = linux.getITMINFOofTestServer()
        # print("ITM = " + ITMINFO)
        # BigfixINFO = linux.getBigfixINFOofTestServer()
        # print("Bigfix = " + BigfixINFO)
        #
        # linux.closeChannel()
        # linux.closeConnection()
        # linux = linux()
        # # linux.getInstanceInfo('VMWare','EVR-NO-CCD1','evr-ccd1-l01257','10.114.27.106')
        # linux.getInstanceInfo('VMWare','EVR-NO-CCD1','evr-ccd1-l01202','10.114.27.53')
        # # linux.getInstanceInfo('VMWare','EVR-NO-CCD1','evr-ccd1-l01178','10.114.28.45')
        pass
