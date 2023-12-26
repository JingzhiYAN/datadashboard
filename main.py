from flask import Flask, render_template, redirect, url_for,jsonify
from blueprints.data import full_data_update
import subprocess
import time
import pymysql
app = Flask(__name__)

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
# Function to get data from the database

@app.route('/update_database', methods=['POST'])
def update_database():
    # Run the Python script using subprocess
    subprocess.run(['python', 'daily/update_database.py'])
    time.sleep(5)  # Simulate a delay of 5 seconds

    # Return a completion status as JSON
    return 'complete'

@app.route('/')
def index():
    try:
        # Connect to the MySQL database
        connection = pymysql.connect(host=hostname, user=databaseusername, password=databasepassword, database=databasename)
        cursor = connection.cursor()

        with connection.cursor() as cursor:
            # Execute the SQL query to fetch data from the table
            sql_query = "SELECT * FROM apdatabase WHERE status = 'offline';"
            cursor.execute(sql_query)

            # Fetch all rows from the result set
            offlineAP = cursor.fetchall()

    except pymysql.Error as e:
        # Handle any potential MySQL errors
        print(f"Error: {e}")
        offlineAP = []  # Set data as empty list in case of an error
        # Close the database connection

    # Render the HTML template with the fetched data
    return render_template('index.html', data=offlineAP)

if __name__ == '__main__':
    app.run(debug=True)
