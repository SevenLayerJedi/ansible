import datetime
import pytz

def get_unixtimenow():
    # Set the timezone
    timezone = pytz.timezone('UTC')  # Set your desired timezone here
    #
    # Get the current datetime in the specified timezone
    current_time = datetime.datetime.now(timezone)
    #
    # Convert the datetime to a Unix timestamp
    unix_timestamp = int(current_time.timestamp())
    #
    return unix_timestamp

