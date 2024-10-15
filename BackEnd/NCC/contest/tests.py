# from django.test import TestCase

# Create your tests here.
from datetime import datetime
import pytz

# Get the current UTC time
current_time = datetime.utcnow()
print("crnt_time",current_time)

# Convert the UTC time to a specific time zone
desired_timezone = pytz.timezone('Asia/Kolkata')
localized_time = current_time.astimezone(desired_timezone)

# Format the localized time as a string
formatted_time = localized_time.strftime('%Y-%m-%d %H:%M:%S %Z')

print(formatted_time)
