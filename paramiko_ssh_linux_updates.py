# This script creates ssh connections and updates the systems.
# It can be modified to run any commands.

# Author Harald Trohne

import paramiko
from getpass import getpass

class SSHClient:
    def __init__(self, l_username, l_password, l_port):
        self.l_username = l_username
        self.l_password = l_password
        self.l_port = l_port
        self.hostnames = ['192.168.0.32', '172.16.2.30']
        self.client = paramiko.client.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname=self.hostnames[0], port=self.l_port,
                            username=self.l_username, password=self.l_password)

    def __del__(self):
        self.client.close()
    
    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
        stdin.write(self.l_password +'\n')
        stdin.flush()
        for line in iter(stdout.readline, ""):
            print(line, end="")

    def exec_command_on_all(self, command):
        for host in self.hostnames:
            self.client.connect(hostname=host, port=self.l_port,
                                username=self.l_username, password=self.l_password)
            stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
            stdin.write(self.l_password +'\n')
            stdin.flush()
            for line in iter(stdout.readline, ""):
                print(host, line, end="")
            self.client.close()
    
    def exec_command_on_all_parallel(self, command):
        # TODO
        pass

def main():
    l_username = input('\nEnter username:\n')
    l_password = getpass('Enter password:\n')
    l_port = input('Enter portnumber:\n')
    ssh = SSHClient(l_username, l_password, l_port)
    ssh.exec_command('sudo apt update && sudo apt upgrade -y')
    ssh.exec_command_on_all('sudo apt update && sudo apt upgrade -y')
    ssh.__del__()

if __name__ == '__main__':
    main()
