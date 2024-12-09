import network


# Wi-Fi情報を取得する
def get_wifi_info():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        ip, subnet, gateway, dns = wlan.ifconfig()
        print("IP:", ip)
        print("sub:", subnet)
        print("def:", gateway)
        print("DNS:", dns)
    else:
        print("Wi-Fi not connected")


# 実行
get_wifi_info()
