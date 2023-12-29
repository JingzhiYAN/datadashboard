import subprocess
import paramiko
import time
import pymysql

def read_credentials_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        switchusername = lines[0].strip()  # Get username from the first line
        switchpassword = lines[1].strip()  # Get password from the second line
        databaseusername = lines[2].strip()
        databasepassword = lines[3].strip()
        databasename = lines[4].strip()
        hostname = lines[5].strip(

        )
        ssh_host = lines[7].strip()
    return switchusername, switchpassword,databaseusername,databasepassword,databasename,hostname,ssh_host

# File path containing username and password
credentials_file = 'daily/credentials.txt'

# Read username and password from the file
switchusername, switchpassword,databaseusername,databasepassword, databasename,hostname,ssh_host= read_credentials_from_file(credentials_file)
# SSH connection details
ssh_port = 22  # Default SSH port
ssh_username = switchusername
ssh_password = switchpassword
enable_password = switchpassword
def read_credentials_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        switchusername = lines[0].strip()  # Get username from the first line
        switchpassword = lines[1].strip()  # Get password from the second line
        databaseusername = lines[2].strip()
        databasepassword = lines[3].strip()
        databasename = lines[4].strip()
        hostname = lines[5].strip()
    return switchusername, switchpassword,databaseusername,databasepassword,databasename,hostname

# File path containing username and password
credentials_file = 'daily/credentials.txt'

# Read username and password from the file
switchusername, switchpassword,databaseusername,databasepassword, databasename,hostname= read_credentials_from_file(credentials_file)
# SSH connection details

connection = pymysql.connect(host=hostname, user=databaseusername, password=databasepassword, database=databasename)
cursor = connection.cursor()
# aquire the ip address
list_of_device_ip = []
ip = []
try:
    # Connect to the MySQL database

    cursorclass = 'pymysql.cursors.DictCursor'
    with connection.cursor() as cursor:

        # offline list.
        sql_query = "SELECT addresses FROM obmanage;"
        cursor.execute(sql_query)
        addresses = cursor.fetchall()
except pymysql.Error as e:
    # Handle any potential MySQL errors
    print(f"Error: {e}")
    countofflineswitch = []  # Set data as empty list in case of an error
    offlineswitch = []

for ip in addresses:
    ip = next(iter(ip or []), 0)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh_client.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password, timeout=10)
    print("SSH connection established.")

    # Create interactive shell
    ssh_shell = ssh_client.invoke_shell()
    time.sleep(1)

    # Send 'enable' to enter enable mode
    ssh_shell.send('enable\n')
    time.sleep(1)
    output = ssh_shell.recv(65535).decode('utf-8')

    # Wait for 'Password:' prompt and send enable password

    if 'Password:' in output:
        ssh_shell.send(enable_password + '\n')
        time.sleep(1)

    ssh_shell.send('wr\n')
    output = ssh_shell.recv(65535).decode('utf-8')
    print(ip+output)
    time.sleep(0.5)
    ssh_shell.send('exit\n')
except paramiko.AuthenticationException as auth_exception:
    print("Authentication failed:", str(auth_exception))
except paramiko.SSHException as ssh_exception:
    print("SSH connection failed:", str(ssh_exception))



