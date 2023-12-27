from tabulate import tabulate

import numpy as np

print("SPAR SIZING PROGRAM, c. 1984 by M. Hollman")

# ----- Input Data ----
# Enter Gross Weight less Wing Weight, lbs = W

w = 829
load_factor = 4.4
wing_span = 20
root_chord = 4
tip_chord = 2

# ----- Spar Program -----

n = 10

ws = [0] * n
v = [0] * n
m = [0] * n
m1 = [0] * n
wl = [0] * n

lf = float(load_factor)
s = float(wing_span)
cr = float(root_chord)
ct = float(tip_chord)

ws[0] = 0
wl[0] = 2 * w * lf * cr / (s * (cr + ct))
v[0] = w * lf / 2
m[0] = w * lf * s / 4 - w * lf * s * (2 * cr + ct) / (12 * (cr + ct))

for c in range(0, n - 1):
    ws[c + 1] = ws[c] + s / 20
    wl[c + 1] = wl[0] + 4 * w * lf * (ct - cr) * ws[c + 1] / (s**2 * (ct + ct))
    v[c + 1] = v[0] - 2 * w * lf * (
        cr * ws[c + 1] - cr * ws[c + 1] ** 2 / s + ct * ws[c + 1] ** 2 / s
    ) / (s * (cr + ct))
    m1[c + 1] = (
        cr * ws[c + 1] ** 2 / 2
        - cr * ws[c + 1] ** 3 / (3 * s)
        + ct * ws[c + 1] ** 3 / (3 * s)
    )
    m[c + 1] = m[0] + 2 * w * lf * m1[c] / (s * (cr + ct)) - w * lf * ws[c + 1] / 2

headers = ["WING STA, ft", "AIR LOAD, lb/ft", "SHEAR, lb", "MOMENT, ftlb"]
data = [ws, wl, v, m]
tabular_data = list(map(lambda *x: list(x), *data))
print(tabulate(tabular_data=tabular_data, headers=headers))


# ----- SPAR SIZING -----

ft = float(input("Enter Tensile or Compressive Strength of Cap, psi:"))
fs = float(input("Enter Shear Strength of Shear Web, psi:"))
a = float(input("Enter Spar Width, Inches:"))
cd = float(input("Enter Chord Thickness, % Chord:"))

print()

h = [0] * n
t1 = [0] * n
t2 = [0] * n


ws[0] = 0
h[0] = 0.96 * cd * cr
t1[0] = 24 * m[0] / (h[0] * a * ft)
t2[0] = v[0] / (h[0] * fs)

for c in range(0, n - 1):
    ws[c + 1] = ws[c] + s / 20
    h[c + 1] = h[0] + 0.096 * cd * 2 * (ct - cr) * ws[c + 1] / s
    t1[c + 1] = 24 * m[c + 1] / h[c + 1] * a * ft
    t2[c + 1] = v[c + 1] / (h[c + 1] * fs)

headers = ["WING STA, ft", "SPAR HEIGHT, in", "CAP THICK, in", "WEB THICK, in"]
data = [ws, h, t1, t2]
tabular_data = list(map(lambda *x: list(x), *data))
print(tabulate(tabular_data=tabular_data, headers=headers))

input("Hit Return to Quit")
