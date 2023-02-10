import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


# input_road_width = int(input("Current Road's width : "))
# input_road_density = int(input("road_density Sekarang: "))
# input_road_width_n = int(input("Lebar Selanjutnya: "))
# input_road_density_n = int(input("road_density Selanjutnya: "))

input_road_width = 0
input_road_density = 0
input_road_width_n = 0
input_road_density_n = 0

def input_from_image(input1, input2, input3, input4):
  global input_road_width, input_road_density, input_road_width_n, input_road_density_n
  input_road_width = input1
  input_road_density = input2
  input_road_width_n = input3
  input_road_density_n = input4
  return compute_all()

def compute_all():
  global input_road_width, input_road_density, input_road_width_n, input_road_density_n

  road_width = np.arange(0, 12, 1)
  road_width_n = np.arange(0, 12, 1)
  road_density = np.arange(0, 19, 1)
  road_density_n = np.arange(0, 19, 1)
  green_dur = np.arange(0, 71, 1)

  if input_road_width > np.max(road_width):
      input_road_width = np.max(road_width)
  elif input_road_width < np.min(road_width):
      input_road_width = np.min(road_width)

  if input_road_width_n > np.max(road_width_n):
      input_road_width_n = np.max(road_width_n)
  elif input_road_width_n < np.min(road_width_n):
      input_road_width_n = np.min(road_width_n)

  if input_road_density > np.max(road_density):
      input_road_density = np.max(road_density)
  elif input_road_density < np.min(road_density):
      input_road_density = np.min(road_density)

  if input_road_density_n > np.max(road_density_n):
      input_road_density_n = np.max(road_density_n)
  elif input_road_density_n < np.min(road_density_n):
      input_road_density_n = np.min(road_density_n)



  road_width_nar = fuzz.trimf(road_width, [0, 0, 8])
  road_width_wide = fuzz.trimf(road_width, [6, 11, 11])
  road_width_n_nar  = fuzz.trimf(road_width_n,[0, 0, 8])
  road_width_n_wide = fuzz.trimf(road_width_n, [6, 11, 11])

  road_density_nc = fuzz.trapmf(road_density, [0, 0, 3, 6])
  road_density_lc = fuzz.trimf(road_density, [3, 6, 9])
  road_density_pc = fuzz.trimf(road_density, [6, 9, 12])
  road_density_p= fuzz.trimf(road_density, [9, 12, 15])
  road_density_vc = fuzz.trapmf(road_density, [12, 15, 18, 18])

  road_density_n_nc = fuzz.trapmf(road_density_n, [0, 0, 3, 6])
  road_density_n_lc = fuzz.trimf(road_density_n, [3, 6, 9])
  road_density_n_pc = fuzz.trimf(road_density_n, [6, 9, 12])
  road_density_n_c= fuzz.trimf(road_density_n, [9, 12, 15])
  road_density_n_vc = fuzz.trapmf(road_density_n, [12,15, 18, 18])

  green_dur_awhile = fuzz.trimf(green_dur, [0, 0, 30])
  green_dur_avg = fuzz.trimf(green_dur, [10, 30, 50])
  green_dur_long = fuzz.trimf(green_dur, [30, 50, 70])
  green_dur_vlong = fuzz.trimf(green_dur, [50, 70, 70])

  #FUZZIFIKASI INPUT
  road_width_lvl_nar = fuzz.interp_membership(road_width, road_width_nar, input_road_width)
  road_width_lvl_wide = fuzz.interp_membership(road_width, road_width_wide, input_road_width)

  road_density_lvl_nc = fuzz.interp_membership(road_density, road_density_nc, input_road_density)
  road_density_lvl_lc = fuzz.interp_membership(road_density, road_density_lc, input_road_density)
  road_density_lvl_pc = fuzz.interp_membership(road_density, road_density_pc, input_road_density)
  road_density_lvl_c= fuzz.interp_membership(road_density, road_density_p, input_road_density)
  road_density_lvl_vc = fuzz.interp_membership(road_density, road_density_vc, input_road_density)

  road_width_n_lvl_nar = fuzz.interp_membership(road_width_n, road_width_n_nar , input_road_width_n)
  road_width_n_lvl_wide = fuzz.interp_membership(road_width_n, road_width_n_wide, input_road_width_n)


  road_density_n_lvl_nc = fuzz.interp_membership(road_density_n, road_density_n_nc, input_road_density_n)
  road_density_n_lvl_lc = fuzz.interp_membership(road_density_n, road_density_n_lc, input_road_density_n)
  road_density_n_lvl_pc = fuzz.interp_membership(road_density_n, road_density_n_pc, input_road_density_n)
  road_density_n_lvl_c = fuzz.interp_membership(road_density_n, road_density_n_c, input_road_density_n)
  road_density_n_lvl_vc = fuzz.interp_membership(road_density_n, road_density_n_vc, input_road_density_n)

  # Legends : 
  # Lebar Sekarang = ljs
  # Lebar Selanjutnya = ljn
  # road_density Sekarang = kjs
  # road_density Selanjutnya = kjn

  # Rules : 
  # Jika ljs = wide, ljn = narpit/wide, dan kjs = tidak padat/kurang padat, maka green_dur = sebentar
  r1 = np.fmin(road_width_lvl_wide, road_density_lvl_nc)
  r2 = np.fmin(road_width_lvl_wide, road_density_lvl_lc)

  r3 = np.fmin(road_width_lvl_nar, road_density_lvl_nc)
  r4 = np.fmin(road_width_lvl_nar, road_density_lvl_lc)
  # Jika ljs = narpit/wide, ljn = narpit/wide, kjs = cukup padat, maka green_dur = Sedang
  r5 = np.fmin(road_width_lvl_nar, road_density_lvl_pc)
  r6 = np.fmin(road_width_lvl_wide, road_density_lvl_pc)
  # Jika ljs = narpit, ljn = narpit, kjs = padat, kjn = tidak padat/kurang padat/cukup padat, maka green_dur = lama
  r7 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_c, road_density_n_lvl_nc)))
  r8 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_c, road_density_n_lvl_pc)))
  r9 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_c, road_density_n_lvl_lc)))
  # Jika ljs = narpit/wide, ljn = narpit, kjs = cukup padat, kjn = padat/sangat padat, maka green_dur = sedang
  r10 = np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_c, road_density_n_lvl_c))

  r11 = np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_c, road_density_n_lvl_vc))
  # Jika ljs = narpit, ljn = narpit/wide, kjs = sangat padat, kjn = tidak/kurang/cukup padat, maka green_dur = sangat lama
  r12 = np.fmin(road_width_lvl_nar, np.fmin(road_density_lvl_vc, road_density_n_lvl_nc))
  r13 = np.fmin(road_width_lvl_nar, np.fmin(road_density_lvl_vc, road_density_n_lvl_lc))
  r14 = np.fmin(road_width_lvl_nar, np.fmin(road_density_lvl_vc, road_density_n_lvl_pc))
  # Jika ljs = narpit/wide, ljn = narpit, kjs = sangat padat, kjn = sangat padat/padat, maka green_dur = lama
  r15 = np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_vc, road_density_lvl_c))
  r16 = np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_vc, road_density_n_lvl_vc))
  # Jika ljs = narpit, ljn = wide, kjs = sangat padat, kjn = sangat padat/padat, maka green_dur = sangat lama
  r17 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_vc)))
  r18 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_vc,road_density_n_lvl_c)))
  r19 = np.fmin(road_width_lvl_nar, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_c)))
  # Jika ljs = wide, ljn = narpit, kjs = sangat padat, kjn = sangat padat/padat, maka green_dur = lama 
  r20 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_vc, road_density_lvl_vc)))
  r21 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_nar, np.fmin(road_density_lvl_vc, road_density_n_lvl_c)))
  # Jika ljs = wide, ljn = wide, kjs = sangat podat/padat, kjn = sangat padat/padat, maka green_dur = lama 
  r22 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_c)))
  r23 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_vc)))
  r24 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_wide,  np.fmin(road_density_lvl_c, road_density_n_lvl_c)))
  r25 = np.fmin(road_width_lvl_wide, np.fmin(road_width_n_lvl_wide, np.fmin(road_density_lvl_c, road_density_n_lvl_vc)))

  r26 = np.fmin(road_width_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_nc))
  r27 = np.fmin(road_width_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_lc))
  r28 = np.fmin(road_width_lvl_wide, np.fmin(road_density_lvl_vc, road_density_n_lvl_pc))

  out1 = np.fmin(r1, green_dur_awhile)
  out2 = np.fmin(r2, green_dur_awhile)
  out3 = np.fmin(r3, green_dur_awhile)
  out4 = np.fmin(r4, green_dur_avg)
  out5 = np.fmin(r5, green_dur_avg)
  out6 = np.fmin(r6, green_dur_awhile)
  out7 = np.fmin(r7, green_dur_long)
  out8 = np.fmin(r8, green_dur_long)
  out9 = np.fmin(r9, green_dur_long)
  out10 = np.fmin(r10, green_dur_avg)
  out11 = np.fmin(r11, green_dur_avg)
  out12 = np.fmin(r12, green_dur_vlong)
  out13 = np.fmin(r13, green_dur_vlong)
  out14 = np.fmin(r14, green_dur_vlong)
  out15 = np.fmin(r15, green_dur_long)
  out16 = np.fmin(r16, green_dur_long)
  out17 = np.fmin(r17, green_dur_vlong)
  out18 = np.fmin(r18, green_dur_vlong)
  out19 = np.fmin(r19, green_dur_vlong)
  out20 = np.fmin(r20, green_dur_long)
  out21 = np.fmin(r21, green_dur_long)
  out22 = np.fmin(r22, green_dur_long)
  out23 = np.fmin(r23, green_dur_long)
  out24 = np.fmin(r24, green_dur_long)
  out25 = np.fmin(r25, green_dur_long)
  out26 = np.fmin(r26, green_dur_long)
  out27 = np.fmin(r27, green_dur_long)
  out28 = np.fmin(r28, green_dur_long)

  hij = np.zeros_like(green_dur)

  final1 = np.fmax(out1, np.fmax(out2, np.fmax(out3, np.fmax(out4, np.fmax(out5, np.fmax(out6, np.fmax(out5, np.fmax(out6, np.fmax(out7, np.fmax(out8, np.fmax(out9, out10)))))))))))
  final2 = np.fmax(out11, np.fmax(out12, np.fmax(out13, np.fmax(out14, np.fmax(out15, np.fmax(out16, np.fmax(out15, np.fmax(out16, np.fmax(out17, np.fmax(out18, np.fmax(out19, out20)))))))))))
  final3 = np.fmax(out21, np.fmax(out22, np.fmax(out23, np.fmax(out24, np.fmax(out25, np.fmax(out26, np.fmax(out27, out28))))))) 

  agg = np.fmax(final1, np.fmax(final2, final3))

  #DEFFUZ
  durasi_hijau = fuzz.defuzz(green_dur, agg, 'centroid')
  plot_green_dur = fuzz.interp_membership(green_dur, agg, durasi_hijau)

  fig, ax0 = plt.subplots(nrows = 1, figsize=(8,3))
  ax0.plot(green_dur, green_dur_awhile, 'b', linewidth=1.5, linestyle='--')
  ax0.plot(green_dur, green_dur_avg, 'g', linewidth=1.5, linestyle='--')
  ax0.plot(green_dur, green_dur_long, 'r', linewidth=1.5, linestyle='--')
  ax0.plot(green_dur, green_dur_vlong, 'm', linewidth=1.5, linestyle='--')
  ax0.fill_between(green_dur, hij, agg, facecolor='orange', alpha=0.7)
  ax0.plot([durasi_hijau, durasi_hijau], [0, plot_green_dur], 'k', linewidth=1.5, alpha=0.9)

  # print("Durasi Lampu Hijau : ", durasi_hijau)
  plt.savefig("Result.jpg")
  return durasi_hijau