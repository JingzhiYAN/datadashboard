import paramiko
import time
import csv
from datetime import datetime
import pymysql
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
ssh_host = '162.254.1.32'
ssh_port = 22  # Default SSH port
ssh_username = switchusername
ssh_password = switchpassword
enable_password = switchpassword

# Establish SSH connection
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

    # Wait for 'Password:' prompt and send enable password
    output = ssh_shell.recv(65535).decode('utf-8')
    if 'Password:' in output:
        ssh_shell.send(enable_password + '\n')
        time.sleep(1)

    # Send 'show ip arp' command
    ssh_shell.send('terminal length 0\n')
    ssh_shell.send('show ip arp\n')
    time.sleep(2)  # Adjust as needed based on command execution time

    output = ''

    # Receive data in chunks
    data = ssh_shell.recv(65535).decode('utf-8')
    output += data
    data = ssh_shell.recv(65535).decode('utf-8')
    output += data


    # Print the complete output
    print(output)
    ssh_shell.send('terminal no length\n')
    # Send 'exit' command to terminate the session
    ssh_shell.send('exit\n')

    # Write accumulated lines to a new file
    with open('output.txt', 'w') as file:
            file.write(output)
    file.close()
    with open('output.txt','r', encoding = "utf-8") as newfile:
        with open('output.csv', 'w', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in newfile:
                if "I" in row:
                    elements = row.replace('\n','')
                    elements = elements.split()

                    csv_writer.writerow(elements)
except paramiko.AuthenticationException as auth_exception:
    print("Authentication failed:", str(auth_exception))
except paramiko.SSHException as ssh_exception:
    print("SSH connection failed:", str(ssh_exception))

ssh_client.close()

# Assuming 'data' contains the lines from the text file
#update the database.

connection = pymysql.connect(host=hostname, user=databaseusername, password=databasepassword, database=databasename)
cursor = connection.cursor()
# pre-process
sql_offline = "UPDATE apdatabase SET status = 'offline' WHERE status = 'online'"

# Execute the SQL command to update online APs to offline
try:
    cursor.execute(sql_offline)
    connection.commit()
    print("Online APs set to offline")
except pymysql.Error as e:
    connection.rollback()
    print(f"Error setting online APs to offline: {e}")


#it's better we do this in the same file.
with open('output.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        if not any(row):  # Check if the row is empty
            continue
        search_data = row[3]

        sql = f"UPDATE apdatabase SET status = 'online', update_time = CURRENT_TIMESTAMP WHERE program_mac = '{search_data}'"
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print(f"Successfully modified data for MAC address: {search_data}")
        else:
            print(f"Error: MAC address '{search_data}' unchange")
            # If this appear, doesn't mean it didn't found, it means there are no updates.
    csvfile.close()
cursor.close()
connection.close()



