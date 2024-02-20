import requests
from datetime import datetime, timedelta
import csv
import pytz

def fetch_sunrise_sunset_data(lat, lng, year, month):
    sun_data = {}
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=32)  # A bit over to ensure we cover the whole month
    end_date = end_date.replace(day=1) - timedelta(days=1)  # Go to the last day of the target month
    local_timezone = pytz.timezone('America/Los_Angeles')
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        response = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date_str}&formatted=0")
        data = response.json()
        
        if data['status'] == 'OK':
            utc_sunrise = datetime.fromisoformat(data['results']['sunrise'])
            local_sunrise = utc_sunrise.astimezone(local_timezone)
            utc_sunset = datetime.fromisoformat(data['results']['sunset'])
            local_sunset = utc_sunset.astimezone(local_timezone)
            sun_data[date_str] = {
                'sunrise': local_sunrise,
                'sunset': local_sunset
            }
        else:
            print(f"Failed to fetch data for {date_str}")
        
        current_date += timedelta(days=1)
    
    return sun_data

def save_to_csv(sun_data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Sunrise', 'Sunset']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for date, times in sun_data.items():
            writer.writerow({'Date': date, 'Sunrise': times['sunrise'], 'Sunset': times['sunset']})

#Data for Mountain View California
#37.3861° N, 122.0839° W

latitude = "37.3861"
longitude = "-122.0839"
year = 2024
month = 3
sunrise_sunset_data = fetch_sunrise_sunset_data(latitude, longitude, year, month)

# Save the data to CSV
csv_filename = 'sunrise_sunset_times.csv'
save_to_csv(sunrise_sunset_data, csv_filename)

print(f"Sunrise and sunset times saved to {csv_filename}")
