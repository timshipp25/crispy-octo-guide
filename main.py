from datetime import datetime

# Get current date and time
current_time = datetime.now()

# Write to file
with open('current_datetime.txt', 'w') as f:
    f.write(f'Current Date and Time: {current_time}')
