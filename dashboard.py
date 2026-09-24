import tkinter as tk

root = tk.Tk()
root.title("Search & Rescue Drone Dashboard")
root.geometry("650x450")

tk.Label(
    root,
    text="SEARCH & RESCUE DRONE",
    font=("Arial", 22, "bold")
).pack(pady=25)

victim = tk.Label(
    root,
    text="Possible Victims: 0",
    font=("Arial", 16)
)
victim.pack(pady=10)

hazard = tk.Label(
    root,
    text="Hazards Detected: 0",
    font=("Arial", 16)
)
hazard.pack(pady=10)

gps = tk.Label(
    root,
    text="GPS: Waiting...",
    font=("Arial", 14)
)
gps.pack(pady=10)

status = tk.Label(
    root,
    text="Drone Status: Connected",
    font=("Arial", 14)
)
status.pack(pady=10)

root.mainloop()
