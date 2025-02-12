from datetime import datetime, timedelta

# Generate logs with timestamps  (current day)
now = datetime.now().replace(second=0, microsecond=0)
log_start = now.replace(hour=8, minute=00)
log_end = now.replace(hour=9, minute=00)

# Create logs with timestamps in this range
logs = []
current_time = log_start
while current_time <= log_end:
    unix_timestamp = int(current_time.timestamp())
    logs.append(f"{unix_timestamp} host{unix_timestamp % 50} host{(unix_timestamp + 5) % 50}")
    current_time += timedelta(minutes=10)  # Increment by 10 minutes

logs

with open("log_test2.txt", "a") as f:
    for log in logs:
        f.write(log + "\n")
