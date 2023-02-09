import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

lebar_jalan = ctrl.Antecedent(np.arange(0, 11, 1), "Lebar Jalan yang Diatur")
lebar_jalan_n = ctrl.Antecedent(np.arange(0, 11, 1), "Lebar Jalan Selanjutnya")
kepadatan_jalan = ctrl.Antecedent(np.arange(0, 18, 1), "Kepadatan Jalan yang Diatur")
kepadatan_jalan_n = ctrl.Antecedent(np.arange(0, 18, 1), "Kepadatan Jalan Selanjutnya")
dur_hijau = ctrl.Consequent(np.arange(0, 70, 1), "Durasi Lampu Hijau")

lebar_jalan['sempit']= fuzz.trimf(lebar_jalan_n.universe,[0, 0, 8])
lebar_jalan['luas'] = fuzz.trimf(lebar_jalan_n.universe, [6, 11, 11])
lebar_jalan_n['sempit'] = fuzz.trimf(lebar_jalan_n.universe,[0, 0, 8])
lebar_jalan_n['luas'] = fuzz.trimf(lebar_jalan_n.universe, [6, 11, 11])

kepadatan_jalan['tidak_padat'] = fuzz.trapmf(kepadatan_jalan.universe, [0, 0, 3, 6])
kepadatan_jalan['kurang_padat'] = fuzz.trimf(kepadatan_jalan.universe, [3, 6, 9])
kepadatan_jalan['cukup_padat'] = fuzz.trimf(kepadatan_jalan.universe, [6, 9, 12])
kepadatan_jalan['padat'] = fuzz.trimf(kepadatan_jalan.universe, [9, 12, 15])
kepadatan_jalan['sangat_padat'] = fuzz.trapmf(kepadatan_jalan.universe, [12,15, 18, 18])

kepadatan_jalan_n['tidak_padat'] = fuzz.trapmf(kepadatan_jalan.universe, [0, 0, 3, 6])
kepadatan_jalan_n['kurang_padat'] = fuzz.trimf(kepadatan_jalan.universe, [3, 6, 9])
kepadatan_jalan_n['cukup_padat'] = fuzz.trimf(kepadatan_jalan.universe, [6, 9, 12])
kepadatan_jalan_n['padat'] = fuzz.trimf(kepadatan_jalan.universe, [9, 12, 15])
kepadatan_jalan_n['sangat_padat'] = fuzz.trapmf(kepadatan_jalan.universe, [12,15, 18, 18])


dur_hijau['sebentar'] = fuzz.trimf(dur_hijau.universe, [0, 0, 30])
dur_hijau['sedang'] = fuzz.trimf(dur_hijau.universe, [10, 30, 50])
dur_hijau['lama'] = fuzz.trimf(dur_hijau.universe, [30, 50, 70])
dur_hijau['sangat_lama'] = fuzz.trimf(dur_hijau.universe, [50, 70, 70])

# lebar_jalan.view()
# lebar_jalan_n.view()
# kepadatan_jalan.view()
# kepadatan_jalan_n.view()

# Legends : 
# Lebar Jalan Sekarang = ljs
# Lebar Jalan Selanjutnya = ljn
# Kepadatan Jalan Sekarang = kjs
# Kepadatan Jalan Selanjutnya = kjn

# Rules : 
# Jika ljs = luas, ljn = sempit/luas, dan kjs = tidak padat/kurang padat, maka dur_hijau = sebentar
r1 = ctrl.Rule(lebar_jalan['luas'] & kepadatan_jalan['tidak_padat'], dur_hijau['sebentar'])
r2 = ctrl.Rule(lebar_jalan['luas'] & kepadatan_jalan['kurang_padat'], dur_hijau['sebentar'])

r3 = ctrl.Rule(lebar_jalan['sempit'] & kepadatan_jalan['tidak_padat'], dur_hijau['sebentar'])
r4 = ctrl.Rule(lebar_jalan['sempit'] & kepadatan_jalan['kurang_padat'], dur_hijau['sedang'])
# Jika ljs = sempit/luas, ljn = sempit/luas, kjs = cukup padat, maka dur_hijau = Sedang
r5 = ctrl.Rule(lebar_jalan['sempit'] & kepadatan_jalan['cukup_padat'], dur_hijau['sedang'])
r6 = ctrl.Rule(lebar_jalan['luas'] & kepadatan_jalan['cukup_padat'], dur_hijau['sebentar'])
# Jika ljs = sempit, ljn = sempit, kjs = padat, kjn = tidak padat/kurang padat/cukup padat, maka dur_hijau = lama
r7 = ctrl.Rule(
    lebar_jalan['sempit'] & lebar_jalan_n['sempit'] & kepadatan_jalan['padat'] & kepadatan_jalan_n['tidak_padat'], dur_hijau['lama'])
r8 = ctrl.Rule(
  lebar_jalan['sempit'] & lebar_jalan_n['sempit'] & kepadatan_jalan['padat'] & kepadatan_jalan_n['cukup_padat'], dur_hijau['lama'])  
r9 = ctrl.Rule(
    lebar_jalan['sempit'] & lebar_jalan_n['sempit'] & kepadatan_jalan['padat'] & kepadatan_jalan_n['kurang_padat'], dur_hijau['lama'])  
# Jika ljs = sempit/luas, ljn = sempit, kjs = padat, kjn = padat/sangat padat, maka dur_hijau = sedang
r10 = ctrl.Rule(lebar_jalan_n['sempit'] & kepadatan_jalan['cukup_padat'] & kepadatan_jalan_n['padat'], dur_hijau['sedang'])

r11= ctrl.Rule(lebar_jalan_n['sempit'] & kepadatan_jalan['cukup_padat'] & kepadatan_jalan_n['sangat_padat'], dur_hijau['sedang'])
# Jika ljs = sempit, ljn = sempit/luas, kjs = sangat padat, kjn = tidak/kurang/cukup padat, maka dur_hijau = sangat lama
r12 = ctrl.Rule(
    lebar_jalan['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['tidak_padat'], 
    dur_hijau['sangat_lama'])
r13 = ctrl.Rule(
    lebar_jalan['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['kurang_padat'], 
    dur_hijau['sangat_lama'])
r14 = ctrl.Rule(
    lebar_jalan['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['cukup_padat'], 
    dur_hijau['sangat_lama'])
# Jika ljs = sempit/luas, ljn = sempit, kjs = sangat padat, kjn = sangat padat/padat, maka dur_hijau = lama
r15 = ctrl.Rule(lebar_jalan_n['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan['padat'], dur_hijau['lama'])
r16 = ctrl.Rule(lebar_jalan_n['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['sangat_padat'], dur_hijau['lama'])
# Jika ljs = sempit, ljn = luas, kjs = sangat padat, kjn = sangat padat/padat, maka dur_hijau = sangat lama
r17 = ctrl.Rule(
    lebar_jalan['sempit'] & lebar_jalan_n['luas'] & kepadatan_jalan['sangat_padat'] & 
    (kepadatan_jalan_n['sangat_padat'] | kepadatan_jalan_n['padat']), 
    dur_hijau['sangat_lama'])
r18 = ctrl.Rule(
    lebar_jalan['sempit'] & lebar_jalan_n['luas'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['padat'], 
    dur_hijau['sangat_lama'])
# Jika ljs = luas, ljn = sempit, kjs = sangat padat, kjn = sangat padat/padat, maka dur_hijau = lama 
r19 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['sangat_padat'], 
    dur_hijau['lama'])
r20 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['sempit'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['padat'], 
    dur_hijau['lama'])
# R10: Jika ljs = luas, ljn = luas, kjs = sangat podat/padat, kjn = sangat padat/padat, maka dur_hijau = lama 
r21 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['luas'] & 
    kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['padat'], 
    dur_hijau['lama'])
r22 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['luas'] & kepadatan_jalan['sangat_padat'] & kepadatan_jalan_n['sangat_padat'], 
    dur_hijau['lama'])
r23 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['luas'] &  kepadatan_jalan['padat'] & kepadatan_jalan_n['padat'], 
    dur_hijau['lama'])
r24 = ctrl.Rule(lebar_jalan['luas'] & lebar_jalan_n['luas'] & kepadatan_jalan['padat'] & kepadatan_jalan_n['sangat_padat'], 
    dur_hijau['lama'])
r25 = ctrl.Rule(lebar_jalan['luas'] & kepadatan_jalan['sangat_padat'], dur_hijau['lama'])
combine_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25])

durasi_hijau = ctrl.ControlSystemSimulation(combine_ctrl)

durasi_hijau.input['Lebar Jalan yang Diatur'] = int(input("Lebar Sekarang : "))
durasi_hijau.input['Kepadatan Jalan yang Diatur'] = int(input("Kepadatan Sekarang : "))
durasi_hijau.input['Lebar Jalan Selanjutnya'] = int(input('Lebar Selanjutnya : '))
durasi_hijau.input['Kepadatan Jalan Selanjutnya'] = int(input("Kepadatan Selanjutnya : "))

durasi_hijau.compute()

print(durasi_hijau.output["Durasi Lampu Hijau"])
dur_hijau.view(sim=durasi_hijau)
plt.savefig('Hasil.png')
plt.show()

