from flask import Blueprint, render_template
import pymysql
# Create a blueprint object
offline_bp = Blueprint('offline', __name__, url_prefix='/offlineap')
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
cursorclass =  'pymysql.cursors.DictCursor'
# Define a route within the blueprint
@offline_bp.route('/')
def offline_page():
    # Your logic to render the table here
    # For example, rendering a template named offline.html
    # Replace this with your actual logic
    try:
        # Connect to the MySQL database
        connection = pymysql.connect(host=hostname, user=databaseusername, password=databasepassword, database=databasename)
        cursor = connection.cursor()

        with connection.cursor() as cursor:

            # offline list.
            sql_query = "SELECT * FROM apdatabase WHERE status = 'offline';"
            cursor.execute(sql_query)
            offlineAP = cursor.fetchall()

            # Count the offline APs.
            cursor.execute("SELECT COUNT(*) FROM apdatabase WHERE status = 'offline'")
            countoffline = cursor.fetchone()
            countoffline = next(iter(countoffline or []), 0)
    except pymysql.Error as e:
        # Handle any potential MySQL errors
        print(f"Error: {e}")
        offlineAP = []# Set data as empty list in case of an error
        countoffline = []
    return render_template('offline.html', offlineAP=offlineAP,countoffline=countoffline)