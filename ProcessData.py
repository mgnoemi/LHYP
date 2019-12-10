
import pickle
import os
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt


picklePath = r'C:\Repoz\LHYP'
pickle_in = open('allPatientData',"rb")
allPatientData = pickle.load(pickle_in)

rlList = []
raList = []
hdList = []
mirList = []
marList = []
plotData = dict()

for patology in allPatientData:
    if patology not in plotData:
        plotData[patology]={}
    for id in allPatientData[patology]:
        for slc in allPatientData[patology][id]:
            for frm in allPatientData[patology][id][slc]:
                rl=allPatientData[patology][id][slc][frm]['ratioLenght']
                if not math.isnan(rl):
                    rlList.append(rl)
                ra=allPatientData[patology][id][slc][frm]['ratioArea']
                if not math.isnan(ra):
                    raList.append(ra)
                hd=allPatientData[patology][id][slc][frm]['HausdorffDistance']
                if not math.isnan(hd):
                    hdList.append(hd)
                mir=allPatientData[patology][id][slc][frm]['MinorAxisRatio']
                if not math.isnan(mir):
                    mirList.append(mir)
                mar=allPatientData[patology][id][slc][frm]['MajorAxisRatio']
                if not math.isnan(mar):
                    marList.append(mar)
  
    plotData[patology]['rlList'] = rlList.copy()
    plotData[patology]['raList'] = raList.copy()
    plotData[patology]['hdList'] = hdList.copy()
    plotData[patology]['mirList'] = mirList.copy()
    plotData[patology]['marList'] = marList.copy()

    rlList.clear()
    raList.clear()
    hdList.clear()
    mirList.clear()
    marList.clear()

patologylist= []
data_to_plot_rl = []
data_to_plot_ra = []
data_to_plot_hd = []
data_to_plot_mir = []
data_to_plot_mar = []

for patology in plotData:
    patologylist.append(patology)
    data_to_plot_rl.append(plotData[patology]['rlList'])
    data_to_plot_ra.append(plotData[patology]['raList'])
    data_to_plot_hd.append(plotData[patology]['hdList'])
    data_to_plot_mir.append(plotData[patology]['mirList'])
    data_to_plot_mar.append(plotData[patology]['marList'])

# Create a figure instance
fig_rl = plt.figure(1, figsize=(9, 6))
# Create an axes instance
ax_rl = fig_rl.add_subplot(111)
# Create the boxplot
bp_rl = ax_rl.boxplot(data_to_plot_rl, showfliers=False)
# configure the boxplot
ax_rl.set_xticklabels(patologylist)
ax_rl.set_title('Circumference ratio of lp and ln for different pathologyes')
ax_rl.get_xaxis().tick_bottom()
ax_rl.get_yaxis().tick_left()
# Save the figure
fig_rl.savefig('lenghtRatio.png', bbox_inches='tight')

# Create a figure instance
fig_ra = plt.figure(2, figsize=(9, 6))
# Create an axes instance
ax_ra = fig_ra.add_subplot(111)
# Create the boxplot
bp_ra = ax_ra.boxplot(data_to_plot_ra, showfliers=False)
# configure the boxplot
ax_ra.set_xticklabels(patologylist)
ax_ra.set_title('Area ratio of lp and ln for different pathologyes')
ax_ra.get_xaxis().tick_bottom()
ax_ra.get_yaxis().tick_left()
# Save the figure
fig_ra.savefig('areaRatio.png', bbox_inches='tight')

# Create a figure instance
fig_hd = plt.figure(3, figsize=(9, 6))
# Create an axes instance
ax_hd = fig_hd.add_subplot(111)
# Create the boxplot
bp_hd = ax_hd.boxplot(data_to_plot_hd, showfliers=False)
# configure the boxplot
ax_hd.set_xticklabels(patologylist)
ax_hd.set_title('Hausdorff distance of lp and ln for different pathologyes')
ax_hd.get_xaxis().tick_bottom()
ax_hd.get_yaxis().tick_left()
# Save the figure
fig_hd.savefig('hausdorffDistance.png', bbox_inches='tight')

# Create a figure instance
fig_mir = plt.figure(4, figsize=(9, 6))
# Create an axes instance
ax_mir = fig_mir.add_subplot(111)
# Create the boxplot
bp_mir = ax_mir.boxplot(data_to_plot_mir, showfliers=False)
# configure the boxplot
ax_mir.set_xticklabels(patologylist)
ax_mir.set_title('Minor axis ratio of fitted ellipses for ln and lp for different pathologyes')
ax_mir.get_xaxis().tick_bottom()
ax_mir.get_yaxis().tick_left()
# Save the figure
fig_mir.savefig('minorAxisRatio.png', bbox_inches='tight')

# Create a figure instance
fig_mar = plt.figure(5, figsize=(9, 6))
# Create an axes instance
ax_mar = fig_mar.add_subplot(111)
# Create the boxplot
bp_mar = ax_mar.boxplot(data_to_plot_mar, showfliers=False)
# configure the boxplot
ax_mar.set_xticklabels(patologylist)
ax_mar.set_title('Major axis ratio of fitted ellipses for ln and lp for different pathologyes')
ax_mar.get_xaxis().tick_bottom()
ax_mar.get_yaxis().tick_left()
# Save the figure
fig_mar.savefig('majorAxisRatio.png', bbox_inches='tight')








