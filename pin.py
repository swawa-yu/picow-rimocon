from machine import *


pin_debug_led = Pin(15, Pin.OUT)
pin_sw = Pin(14, Pin.IN, Pin.PULL_DOWN)
pin_led_ir = Pin(15, Pin.OUT)
pin_sensor = Pin(16, Pin.IN)
pin_led_r = Pin(17, Pin.OUT)

pin_debug_led.off()

# 38kHzのキャリア周波数を生成するためのPWM設定
pwm_led_ir = PWM(pin_led_ir)
pwm_led_ir.freq(38000)
