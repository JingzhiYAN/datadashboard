from flask import Blueprint, render_template

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

full_data_update = Blueprint('data', __name__, url_prefix='/data')

# Route for data-related actions
@full_data_update.route('/update', methods=['POST'])
def update_data():
    # Your logic to update the data
    # This can involve database operations, file handling, etc.
    # Replace this with your actual logic
    
    # For demonstration, simulating a delay (5 seconds)
    import time
    time.sleep(5)
    
    return 'Data updated successfully'

# Other routes related to data can be defined here

