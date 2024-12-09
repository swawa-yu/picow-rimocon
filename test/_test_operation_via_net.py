import network
import socket
from env import env
from pin import *
import time
from signals import light


def set_led_ir(val):
    if val:
        pwm_led_ir.duty_u16(21845)  # 33% Duty cycleでHIGHのパルス (65536 * 0.33 ≈ 21845)
    else:
        pwm_led_ir.duty_u16(0)


# 信号を送信する関数
def send_signal(signal):
    for duration in signal:
        if duration > 0:
            set_led_ir(1)
        else:
            set_led_ir(0)
        time.sleep_us(abs(duration))
    set_led_ir(0)  # 信号をオフにするのを忘れないこと


# Wi-Fi接続情報
SSID = env.get("SSID")
PASSWORD = env.get("PASSWORD")


# Wi-Fi接続
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # MACアドレスを取得する
    mac_address = wlan.config("mac")
    print("MAC ADDRESS:", ":".join(["%02x" % b for b in mac_address]))

    print(f"Connecting to Wi-Fi({ssid})...")
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        pass

    print("Wi-Fi connected:", wlan.ifconfig())
    pin_debug_led.on()


connect_wifi(SSID, PASSWORD)


# ソケット作成
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ソケット再利用を設定
s.bind(addr)
s.listen(1)
print("server started.")

# HTTPレスポンス
html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Rimocon</title>
</head>
<body>
    <h1>照明</h1>
    <p><a href="/onoff">on / off</a></p>
    <p><a href="/lighten">lighten</a></p>
    <p><a href="/darken">暗く</a></p>
</body>
</html>
"""


def close_and_quit():
    print("program stop.")
    s.close()
    import sys

    sys.exit()


pin_sw.irq(trigger=Pin.IRQ_RISING, handler=close_and_quit)


while True:
    cl, addr = s.accept()
    print("client connection:", addr)
    request = cl.recv(1024)
    request = str(request)
    print("request content:", request)

    if "/onoff" in request:
        send_signal(light.onoff[0])
    if "/lighten" in request:
        send_signal(light.lighten[0])
    if "/darken" in request:
        send_signal(light.darken[0])

    response = html
    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    cl.send(response)
    cl.close()
