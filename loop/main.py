import time
from config import router
from src.api import rewrite, set_device

def main():
    time.sleep(10)
    while True:
        devices = router.connected_devices
        if devices:
            print("Devices found, calling rewrite and set_device")
            rewrite()
            set_device(devices)

        time.sleep(60)

if __name__ == "__main__":
    main()