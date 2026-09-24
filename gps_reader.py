import serial

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

gps = serial.Serial(PORT, BAUD_RATE, timeout=1)

print("GPS reader started...")

while True:
    data = gps.readline().decode(
        "ascii",
        errors="ignore"
    ).strip()

    if data:
        print("GPS:", data)
