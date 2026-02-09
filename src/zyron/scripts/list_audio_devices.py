import sounddevice as sd

print("🎤 Available Audio Input Devices:")
devices = sd.query_devices()
default_input = sd.default.device[0]

for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        star = "*" if i == default_input else " "
        print(f"[{i}]{star} {device['name']} (Sample Rate: {device['default_samplerate']})")

print("\n* = Default Input Device")
