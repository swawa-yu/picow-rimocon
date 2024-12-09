from env import *
import network
import socket
from data.lab_aircon import *
from send2 import send_signal
from machine import Pin
import time

# 固定IPアドレスの設定
FIXED_IP = "10.22.43.40"  # 固定IPアドレス
SUBNET_MASK = "255.255.255.0"  # サブネットマスク
GATEWAY = "10.22.43.1"  # デフォルトゲートウェイ
DNS = "133.41.4.2"  # DNSサーバー（GoogleのDNSを指定）

# 状態表現LED
led_ok = Pin(13, Pin.OUT)  # 緑色 OK
led_wifi = Pin(12, Pin.OUT)  # 黄色 Wi-Fi


# Wi-Fi接続
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # 固定IPを設定
    wlan.ifconfig((FIXED_IP, SUBNET_MASK, GATEWAY, DNS))

    # 接続できるまで繰り返し接続を試みる
    while True:
        t = time.ticks_ms()
        print(f"Connecting to Wi-Fi({ssid})...")
        wlan.connect(ssid, password)
        while time.ticks_diff(time.ticks_ms(), t) < 10000:
            if wlan.isconnected():
                print("Wi-Fi connected:", wlan.ifconfig())
                return
        print("Failed to connect Wi-Fi. Retry in 10 seconds...")



# HTMLを生成する
def generate_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Aircon Control</title>
    </head>
    <body>
        <h1>Aircon Control</h1>
        <button onclick="fetch('/danbou');">暖房</button>
        <button onclick="fetch('/off');">オフ</button>
    </body>
    </html>
    """


# HTTPサーバーを起動する
def start_server():
    while True:
        try:
            addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
            s = socket.socket()
            s.bind(addr)
            s.listen(5)

            print("Listening on", addr)
            led_ok.value(1)  # OK LEDを点灯

            while True:
                cl, addr = s.accept()
                print("Client connected from", addr)
                request = cl.recv(1024).decode()
                print("Request:", request)

                # HTTPリクエストを解析
                if "GET /danbou" in request:
                    send_signal(danbou)  # 暖房信号を送信
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n暖房に設定しました"
                elif "GET /off" in request:
                    send_signal(off)  # オフ信号を送信
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=UTF-8x`\r\n\r\nエアコンをオフにしました"
                else:
                    # HTMLページを返す
                    response = (
                        "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                        + generate_html()
                    )

                cl.send(response)
                cl.close()
        except Exception as e:
            continue



# メイン
while True:
    led_ok.value(0)
    led_wifi.value(0)

    connect_wifi(SSID, PASSWORD)
    led_wifi.value(1)  # Wi-Fi LEDを点灯
    
    start_server()
