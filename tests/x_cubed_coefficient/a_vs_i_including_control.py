import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm
import numpy as np
import matplotlib.pyplot as plt
import tabulate

c2=sthm.probe()
c3=sthm.probe()
c4=sthm.probe()
n1=sthm.probe()
n2=sthm.probe()
n3=sthm.probe()
n4=sthm.probe()
k1=sthm.probe()
k2=sthm.probe()
k3=sthm.probe()
k4=sthm.probe()

c2.loadJSON('..\..\data\C2C14.sthm')
c3.loadJSON('..\..\data\C3C19.sthm')
c4.loadJSON('..\..\data\C4A8.sthm')
n1.loadJSON('..\..\data\N1B9.sthm')
n2.loadJSON('..\..\data\N2B10.sthm')
n3.loadJSON('..\..\data\N3B3.sthm')
n4.loadJSON('..\..\data\N4B8.sthm')
k1.loadJSON('..\..\data\kk1.sthm')
k2.loadJSON('..\..\data\kk2.sthm')
k3.loadJSON('..\..\data\kk3.sthm')
k4.loadJSON('..\..\data\kk4.sthm')


probes=np.array([c2,c3,c4,n1,n2,n3,n4,k1,k2,k3,k4])



colordict={'C':'red', 'N':'grey','k':'blue'}
labeldict={'C':'Cut out', 'N':'Non cutout','k':'Commercial'}

plt.cla()
xax=np.linspace(0,2e-3,100)

table=[]

for p in probes:
    table.append([p.style, p.Ifit[1]])
    plt.plot(xax*1e3,xax**3*p.Ifit[1],c=colordict[p.style[0]],label=labeldict[p.style[0]] if labeldict[p.style[0]] not in plt.gca().get_legend_handles_labels()[1] else '')

mytable= tabulate.tabulate(table, tablefmt='plain', floatfmt='.2E',headers=['Style','Temerature Coefficient'])
print mytable
with open('..\..\data\\a_vs_i.txt', 'w') as outputfile:
    outputfile.write(mytable)

plt.xlabel('Current (mA)')
plt.ylabel('$V_{out}$ without bridge imbalance')
plt.legend(loc='best')


if raw_input('Are you sure you want to save?? [y]')=='y':
    outfile=raw_input('Enter filename: \n')
    plt.savefig(outfile)
plt.show()



n4.plot_fit('current')
n4.resistance
n4.maxI
