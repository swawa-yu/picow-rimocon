import network
from env import env

# Wi-Fi接続情報
SSID = env.get("SSID")
PASSWORD = env.get("PASSWORD")


# Wi-Fi接続
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # MACアドレスを取得する
    mac_address = wlan.config("mac")
    print("MACアドレス:", ":".join(["%02x" % b for b in mac_address]))

    print(f"Connecting to Wi-Fi({ssid})...")
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        pass

    print("Wi-Fi connected:", wlan.ifconfig())


connect_wifi(SSID, PASSWORD)

while True:
    pass
