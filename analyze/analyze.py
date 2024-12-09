# from ..signals.light import *
from light import *


def ave(l):
    return sum(l) / len(l) if len(l) else 0


all_data = darken + lighten + off + off2 + on

for i, l in enumerate(all_data):
    print(i, len(l), sum(abs(x) for x in l))
for i, l in enumerate(all_data):
    print(i, end=": ")
    print([v for i, v in enumerate(l) if i % 2 == 0])
    print([v for i, v in enumerate(l) if i % 2 == 1])


ave_on_start0 = sum(l[0] for l in all_data) / len(all_data)
ave_on_start1 = sum(l[0] for l in all_data) / len(all_data)

all_high = [v for l in all_data for i, v in enumerate(l) if i % 2 == 0]
all_low = [abs(v) for l in all_data for i, v in enumerate(l) if i % 2 == 1]

print("all_high:")
print(all_high)
print("all_low:")
print(all_low)

high_near500 = [v for v in all_high if 400 <= v <= 600]
print(ave(high_near500))
# print(on_near500)
high_near1500 = [v for v in all_high if 1300 <= v <= 1700]
print(ave(high_near1500))
# print(on_near1500)
high_near2000 = [v for v in all_high if 1900 <= v <= 2200]
print(ave(high_near2000))
# print(ave(on_near2000))
high_near5600 = [v for v in all_high if 5500 <= v <= 5700]
print(ave(high_near5600))
# print(on_near5600)

low_near500 = ave([v for v in all_low if 400 <= v <= 600])
print(low_near500)

low_near950 = ave([v for v in all_low if 850 <= v <= 1050])
print(low_near950)


# 開始信号らしきはじめの2つは適当にしておいて、データ部っぽいところを0/1にする
def decoded(l):
    ret = []
    n = len(l)
    for i in range(0, n, 2):
        high = l[i]
        low = l[i + 1] if i != n - 1 else low_near500
        v = round((high + abs(low)) / 500) // 2
        if v == 1:
            v = 0
        if v == 2:
            v = 1
        ret.append(v)

    # データ部だけを取り出すことにする
    ret = ret[2:-1]

    # 整数にする
    k = int("".join([str(c) for c in ret]), 2)

    # 16進表記する
    hex_str = hex(k)[2:].upper()

    # 整形する
    s = ""
    for i in range(0, len(hex_str), 2):
        if i:
            s += " "
        s += hex_str[i : i + 2]

    return s


print("darken")
for l in darken:
    print(decoded(l))
print("lighten")
for l in lighten:
    print(decoded(l))
print("off")
for l in off:
    print(decoded(l))
print("off2")
for l in off2:
    print(decoded(l))
print("on")
for l in on:
    print(decoded(l))
