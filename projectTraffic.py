import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

road_width = ctrl.Antecedent(np.arange(0, 11, 1), "Current Road's width")
road_width_n = ctrl.Antecedent(np.arange(0, 11, 1), "Next Road's width")
road_density = ctrl.Antecedent(np.arange(0, 18, 1), "Current Road's density")
road_density_n = ctrl.Antecedent(np.arange(0, 18, 1), "Next Road's density")

dur_green = ctrl.Consequent(np.arange(0, 70, 1), "Green Light Duration :")

road_width['narrow']= fuzz.trimf(road_width_n.universe,[0, 0, 8])
road_width['wide'] = fuzz.trimf(road_width_n.universe, [6, 11, 11])
road_width_n['narrow'] = fuzz.trimf(road_width_n.universe,[0, 0, 8])
road_width_n['wide'] = fuzz.trimf(road_width_n.universe, [6, 11, 11])

road_density['not_crowded'] = fuzz.trapmf(road_density.universe, [0, 0, 3, 6])
road_density['less_crowded'] = fuzz.trimf(road_density.universe, [3, 6, 9])
road_density['pretty_crowded'] = fuzz.trimf(road_density.universe, [6, 9, 12])
road_density['crowded'] = fuzz.trimf(road_density.universe, [9, 12, 15])
road_density['very_crowded'] = fuzz.trapmf(road_density.universe, [12,15, 18, 18])

road_density_n['not_crowded'] = fuzz.trapmf(road_density.universe, [0, 0, 3, 6])
road_density_n['less_crowded'] = fuzz.trimf(road_density.universe, [3, 6, 9])
road_density_n['pretty_crowded'] = fuzz.trimf(road_density.universe, [6, 9, 12])
road_density_n['crowded'] = fuzz.trimf(road_density.universe, [9, 12, 15])
road_density_n['very_crowded'] = fuzz.trapmf(road_density.universe, [12,15, 18, 18])


dur_green['awhile'] = fuzz.trimf(dur_green.universe, [0, 0, 30])
dur_green['avg'] = fuzz.trimf(dur_green.universe, [10, 30, 50])
dur_green['long'] = fuzz.trimf(dur_green.universe, [30, 50, 70])
dur_green['very_long'] = fuzz.trimf(dur_green.universe, [50, 70, 70])

road_width.view()
road_width_n.view()
road_density.view()
road_density_n.view()

# Legends : 
# Current Road's width = rws
# Next Road's width = rwn
# Current Road's density = rds
# Next Road's density = rdn

# Rules : 
# if rws = wide, dan rds = not/less crowded,then dur_green = awhile
r1 = ctrl.Rule(road_width['wide'] & road_density['not_crowded'], dur_green['awhile'])
r2 = ctrl.Rule(road_width['wide'] & road_density['less_crowded'], dur_green['awhile'])
# if rws = wide, dan rds = not crowded,then dur_green = awhile
r3 = ctrl.Rule(road_width['narrow'] & road_density['not_crowded'], dur_green['awhile'])
# if rws = narrow, dan rds = less crowded,then dur_green = avg
r4 = ctrl.Rule(road_width['narrow'] & road_density['less_crowded'], dur_green['avg'])
# if rws = narrow, rds = pretty_crowded,then dur_green = avg
r5 = ctrl.Rule(road_width['narrow'] & road_density['pretty_crowded'], dur_green['avg'])
# if rws = ide, rds = pretty crow,then dur_green = awhile
r6 = ctrl.Rule(road_width['wide'] & road_density['pretty_crowded'], dur_green['awhile'])
# if rws = narrow, rwn = narow, rds = crowded, rdn = not/less/pretty crowded,then dur_green = long
r7 = ctrl.Rule(
    road_width['narrow'] & road_width_n['narrow'] & road_density['crowded'] & road_density_n['not_crowded'], dur_green['long'])
r8 = ctrl.Rule(
  road_width['narrow'] & road_width_n['narrow'] & road_density['crowded'] & road_density_n['pretty_crowded'], dur_green['long'])  
r9 = ctrl.Rule(
    road_width['narrow'] & road_width_n['narrow'] & road_density['crowded'] & road_density_n['less_crowded'], dur_green['long'])  
# if rwn = narrow, rds = crow, rdn = crowded/very crowded,then dur_green = avg
r10 = ctrl.Rule(road_width_n['narrow'] & road_density['crowded'] & road_density_n['crowded'], dur_green['avg'])

r11= ctrl.Rule(road_width_n['narrow'] & road_density['crowded'] & road_density_n['very_crowded'], dur_green['avg'])
# if rws = narrow, rds = very_crowded, rdn = not/less/pretty crowded,then dur_green = very long
r12 = ctrl.Rule(
    road_width['narrow'] & road_density['very_crowded'] & road_density_n['not_crowded'], 
    dur_green['very_long'])
r13 = ctrl.Rule(
    road_width['narrow'] & road_density['very_crowded'] & road_density_n['less_crowded'], 
    dur_green['very_long'])
r14 = ctrl.Rule(
    road_width['narrow'] & road_density['very_crowded'] & road_density_n['pretty_crowded'], 
    dur_green['very_long'])
# if rws = narrow, rwn = wide, rds = very crowded, rdn = very crowded/crowded,then dur_green = very long
r15 = ctrl.Rule(
    road_width['narrow'] & road_width_n['wide'] & road_density['very_crowded'] & road_density_n['very_crowded'], dur_green['very_long'])
r16 = ctrl.Rule(
    road_width['narrow'] & road_width_n['wide'] & road_density['very_crowded'] & road_density_n['crowded'], 
    dur_green['very_long'])
# if rws = wide, rwn = narrow, rds = very crowded, rdn = very crowded/crowded,then dur_green = long 
r17 = ctrl.Rule(road_width['wide'] & road_width_n['narrow'] & road_density['very_crowded'] & road_density_n['very_crowded'], 
    dur_green['long'])
r18 = ctrl.Rule(road_width['wide'] & road_width_n['narrow'] & road_density['very_crowded'] & road_density_n['crowded'], 
    dur_green['long'])
# if rws = wide, rwn = wide, rds = very crowded/crowded, rdn = very crowded/crowded,then dur_green = long 
r19 = ctrl.Rule(road_width['wide'] & road_width_n['wide'] & 
    road_density['very_crowded'] & road_density_n['crowded'], 
    dur_green['long'])
r20 = ctrl.Rule(road_width['wide'] & road_width_n['wide'] & road_density['very_crowded'] & road_density_n['very_crowded'], 
    dur_green['long'])
r21 = ctrl.Rule(road_width['wide'] & road_width_n['wide'] &  road_density['crowded'] & road_density_n['crowded'], 
    dur_green['long'])
r22 = ctrl.Rule(road_width['wide'] & road_width_n['wide'] & road_density['crowded'] & road_density_n['very_crowded'], 
    dur_green['long'])
# if rws = wide, rds = very_crowded, rdn = not/less/pretty crowded,then dur_green = long
r23 = ctrl.Rule(
    road_width['wide'] & road_density['very_crowded'] & road_density_n['not_crowded'], 
    dur_green['long'])
r24 = ctrl.Rule(
    road_width['wide'] & road_density['very_crowded'] & road_density_n['less_crowded'], 
    dur_green['long'])
r25 = ctrl.Rule(
    road_width['wide'] & road_density['very_crowded'] & road_density_n['pretty_crowded'], 
    dur_green['long'])

combine_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25])

greenlight = ctrl.ControlSystemSimulation(combine_ctrl)

greenlight.input["Current Road's width"] = int(input("Current Road's width : "))
greenlight.input["Current Road's density"] = int(input("Current Road's density : "))
greenlight.input["Next Road's width"] = int(input("Next Road's width : "))
greenlight.input["Next Road's density"] = int(input("Next Road's density : "))

greenlight.compute()

print(greenlight.output["Green Light Duration :"])
dur_green.view(sim=greenlight)
plt.savefig('Hasil.png')
plt.show()

