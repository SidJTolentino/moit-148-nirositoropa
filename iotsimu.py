import pandas as pd
import numpy as np

from datetime import datetime, timedelta


num_records = 100  # Adjust this number as needed


# Example for Smart Healthcare Monitoring
data = []


for _ in range(num_records):
    record = {
        "timestamp": datetime.now() - timedelta(minutes=np.random.randint(0, 1440)),  # Random timestamp in the last 24 hours
        "rfid": f"TRK{np.random.randint(100, 999)}",  # Random RFID
        "gps_sensor": np.random.randint(60, 100),  # Normal heart rate range
        "temperature_sensor": round(np.random.uniform(20.0, 25.0), 1)  # Goods temperature in Celsius
    }
    data.append(record)

# Convert to DataFrame
df = pd.DataFrame(data)


# Save dataset
df.to_csv("logistics_tracking_data.csv", index=False)
df.to_json("logistics_tracking_dat", orient="records")


# Display first few rows
df.head()
