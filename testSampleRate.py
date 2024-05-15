import pyaudio

def list_devices():
    p = pyaudio.PyAudio()
    print("List of devices:")
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info["maxInputChannels"] > 0:  # Muestra solo dispositivos de entrada
            print(f"Device {i}: {dev_info['name']} - Channels: {dev_info['maxInputChannels']}")

    p.terminate()

if __name__ == "__main__":
    list_devices()

