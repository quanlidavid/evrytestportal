import paramiko
import time
import shutil
import logging
import logging.config
import re
import os


class linux():
    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.rundeckServers = ['146.213.160.182', '146.213.160.183', '146.213.160.184']

        self.logger = logging.getLogger("evrylog")
        self.logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        if os.path.exists('logs/') == False:
            os.mkdir('logs/')
        self.logfilepath = 'logs/' + 'kvm123' + '-' + time.strftime("%Y%m%d_%H-%M-%S", time.gmtime()) + '.log'
        if os.path.exists(self.logfilepath):
            os.remove(self.logfilepath)

        filehandler = logging.FileHandler(filename=self.logfilepath, encoding="utf-8")
        filehandler.setLevel(logging.INFO)
        fmter = logging.Formatter(fmt="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        filehandler.setFormatter(fmter)
        self.logger.addHandler(filehandler)

    def getlogfilepath(self):
        return self.logfilepath

    def connect(self):
        paramiko.util.log_to_file('syslogin.log')
        self.ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)

    def runCommand(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        self.logger.info(stdout.read().decode())

    def closeConnection(self):
        self.ssh.close()

    def download(self):
        try:
            t = paramiko.Transport((self.hostname, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            remotepath = '/var/log/boot.log'
            localpath = 'download/'
            sftp.get(remotepath, localpath)
            t.close()
        except Exception as e:
            self.logger.error(e)

    def upload(self):
        try:
            t = paramiko.Transport((self.hostname, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.mkdir('/home/upload5')
            sftp.put('download/filetoupload.txt', '/home/upload5/filetoupload.txt')
            t.close()
        except Exception as e:
            self.logger.error(e)

    def createChannelToRundeckServer(self, rounddeckServername):
        self.channel = self.ssh.invoke_shell()
        self.channel.settimeout(60)
        resp = ''
        resp = self.channel.recv(65535).decode()
        # print(resp)
        self.channel.send('ssh ' + rounddeckServername + '\n')
        time.sleep(5)
        resp = ''
        resp = self.channel.recv(65535).decode()
        resp = resp.strip()
        # print('result= \n'+resp)
        self.logger.info(resp)
        if resp.find('RHN kickstart on 2016-12-09') == -1:
            return False
        else:
            return True

    def createChannelToRundeckServers(self):
        for i in range(0, 3):
            if self.createChannelToRundeckServer(self.rundeckServers[i]):
                self.logger.info('Created channel to rundeck server: ' + self.rundeckServers[i])
                return True
        self.logger.error('Created channel to rundeck server failed.')
        return False

    def closeChannel(self):
        self.channel.close()

    def runCommandInChannel(self, command):
        self.channel.send(command)
        time.sleep(5)
        resp = ''
        recv = self.channel.recv(65535)
        resp = recv.decode()
        resp = resp.strip()
        return resp

    def changeUserInRundeckServer(self):
        resp = ''
        resp = self.runCommandInChannel('sudo su - rundeck\n')
        self.logger.info(resp)
        if resp.find('[rundeck@rundeckprod') == -1:
            return False
        else:
            return True

    def SSHInstance(self, instanceIP):
        self.instanceIP = instanceIP
        # print('result= \n' + self.runCommandInChannel('ssh ' + instanceIP + '\n'))
        self.logger.info(self.runCommandInChannel('ssh ' + instanceIP + '\n'))

    def getHOSTNAMEofTestServer(self):
        result = self.runCommandInChannel('hostname\n')
        self.logger.info(result)
        hostname = ''.join(re.findall('hostname\s+(.*)\s+', result))
        return hostname

    def getIPconfigofTestServer(self):
        result = self.runCommandInChannel('ifconfig\n')
        self.logger.info(result)
        ip = ''.join(re.findall(r'inet\s+(.*)\s+netmask', result)[0])
        return ip

    def getCPUofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' cat /proc/cpuinfo\n'))
        # cmd = '''cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l\n'''
        result = self.runCommandInChannel('cat /proc/cpuinfo\n')
        self.logger.info(result)
        cupnumber = len(re.findall(r'physical id', result))
        return cupnumber

    def getMEMofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' cat /proc/meminfo\n'))
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' free -h\n'))
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+'  free -h|grep Mem|cut -d : -f 2|cut -d G -f 1\n'))
        # cmd = ''' free -h|grep Mem|awk '{printf$2"\\n"}'\n'''
        result = self.runCommandInChannel('free -h\n')
        self.logger.info(result)
        mem = ''.join(re.findall(r'Mem:\s+(.*?)\s+', result))
        return mem

    def getDISKofTestServer(self):
        # print('result= \n' + self.runCommandInChannel('ssh '+testServerIP+' lsblk\n'))
        result = self.runCommandInChannel('lsblk\n')
        self.logger.info(result)
        disk = ''.join(re.findall(r'sda.*\s+(.*?G).*disk', result))
        return disk

    def getDNSofTestServer(self):
        result = self.runCommandInChannel('ping www.google.com -c 5\n')
        self.logger.info(result)
        linenumber = len(re.findall(r'\d+ bytes from .* ms', result))
        if linenumber == 5:
            return 'pass'
        else:
            return 'fail'

    def getNTPofTestServer(self):
        result = self.runCommandInChannel('timedatectl\n')
        self.logger.info(result)
        timezone = ''.join(re.findall(r'Time zone:\s+(.*)\s+\(', result))
        return timezone

    def getITMINFOofTestServer(self):
        result1 = self.runCommandInChannel('ps -ef|grep ITM --color=never\n')
        self.logger.info(result1)
        runningProcessNumber = len(re.findall(r'IBM/ITM', result1))
        result2 = self.runCommandInChannel('/opt/IBM/ITM/bin/cinfo -r\n')
        self.logger.info(result2)
        runningProdNumber = len(re.findall(r'running', result2))
        result3 = self.runCommandInChannel('/opt/IBM/ITM/bin/cinfo -o\n')
        self.logger.info(result3)
        runningInstanceNumber = len(re.findall(r'Instance', result3))
        if runningProcessNumber == 3 and runningProdNumber == 2 and runningInstanceNumber == 2:
            return 'pass'
        else:
            return 'fail'

    def getBigfixINFOofTestServer(self):
        result1 = self.runCommandInChannel('ps -ef|grep BESClient --color=never\n')
        self.logger.info(result1)
        runningProcessNumber = len(re.findall(r'/BESClient/bin/BESClient', result1))
        result2 = self.runCommandInChannel('/etc/init.d/besclient status\n')
        self.logger.info(result2)
        runningProdNumber = len(re.findall(r'running', result2))
        result3 = self.runCommandInChannel('cat /var/opt/BESClient/besclient.config\n')
        self.logger.info(result3)
        if runningProcessNumber == 1 and runningProcessNumber == 1:
            return 'pass'
        else:
            return 'fail'


if __name__ == '__main__':
    # connect to jump server
    linux = linux('ssh.cosng.net', 'e214375', 'Passw0rd2018', 22)
    linux.connect()
    if linux.createChannelToRundeckServers():
        print('rundeck server connected.')
    else:
        print('rundeck server connect failed.')
    if linux.changeUserInRundeckServer():
        print('User changed.')
    else:
        print('User change failed.')
    linux.SSHInstance('139.112.21.191')
    Hostname = linux.getHOSTNAMEofTestServer()
    print("Hostname = " + Hostname)
    IP = linux.getIPconfigofTestServer()
    print('IP = ' + str(IP))
    CPUnumber = linux.getCPUofTestServer()
    print('CPU number = ' + str(CPUnumber))
    MEM = linux.getMEMofTestServer()
    print('Memory = ' + MEM)
    Disk = linux.getDISKofTestServer()
    print('Disk = ' + Disk)
    NTPTimeZone = linux.getNTPofTestServer()
    print('NTP Timezone = ' + NTPTimeZone)
    DNSstatus = linux.getDNSofTestServer()
    print("DNS status = " + DNSstatus)
    ITMINFO = linux.getITMINFOofTestServer()
    print("ITM = " + ITMINFO)
    BigfixINFO = linux.getBigfixINFOofTestServer()
    print("Bigfix = " + BigfixINFO)

    linux.closeChannel()
    linux.closeConnection()
