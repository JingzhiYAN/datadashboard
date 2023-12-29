import csv
from datetime import datetime
import subprocess
import pymysql

def senderx(ip_address):
    ping_count = 5  # Number of ping attempts
    timeout = 5  # Timeout for each ping attempt

    # Constructing the ping command within cmd.exe
    ping_cmd = f"/c ping -n {ping_count} -w {timeout * 1000} {ip_address}"  # Using milliseconds for timeout

    try:
        # Run the cmd.exe command with the ping command as an argument
        ping_output = subprocess.run(["C:\\WINDOWS\\system32\\cmd.exe", ping_cmd], capture_output=True, text=True, timeout=timeout+1)

        # Check the return code to determine if the device is reachable
        if ping_output.returncode == 0:
            # If the device replies to the ping
            return 'deviceon'
        else:
            # If the device is down or unreachable
            return 'devicedown'

    except subprocess.TimeoutExpired:
        # If the ping command times out
        return 'devicedown'



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
    result = senderx(ip)
    connection = pymysql.connect(host=hostname, user=databaseusername, password=databasepassword,
                                 database=databasename)
    cursor = connection.cursor()
    addresses = []
    print(ip)
    print(result)
    if result == 'deviceon':
        try:
            command = sql_query = f"UPDATE obmanage SET status = 'online', update_time = CURRENT_TIMESTAMP WHERE addresses = '{ip}';"
            cursor.execute(command)
            connection.commit()
            print("update successful")
        except pymysql.Error as e:
            connection.rollback()
            print(f"failed: {e}")

    if result == 'devicedown':
        try:
            command = sql_query = f"UPDATE obmanage SET status = 'offline', update_time = CURRENT_TIMESTAMP WHERE addresses = '{ip}';"
            cursor.execute(command)
            connection.commit()
            print("Update successful")
        except pymysql.Error as e:
            connection.rollback()
            print(f"Failed{e}")
cursor.close()
connection.close()



