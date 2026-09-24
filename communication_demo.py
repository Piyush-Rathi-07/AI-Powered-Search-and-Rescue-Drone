import json
import time

rescue_data = {
    "object": "person",
    "confidence": 0.87,
    "latitude": 18.6298,
    "longitude": 73.7997,
    "status": "possible_victim"
}

message = json.dumps(rescue_data)

print("Sending data...")
print(message)

time.sleep(1)

print("Data received by rescue dashboard.")
