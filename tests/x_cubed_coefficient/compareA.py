import sys
import os
sys.path.append(os.path.abspath('../sthm'))
import SThMprobes as sthm
import numpy as np
import matplotlib.pyplot as plt

c2=sthm.probe()
c3=sthm.probe()
c4=sthm.probe()
n1=sthm.probe()
n2=sthm.probe()
n3=sthm.probe()
n4=sthm.probe()



c2.loadJSON('..\data\C2C14.sthm')
c3.loadJSON('..\data\C3C19.sthm')
c4.loadJSON('..\data\C4A8.sthm')
n1.loadJSON('..\data\N1B9.sthm')
n2.loadJSON('..\data\N2B10.sthm')
n3.loadJSON('..\data\N3B3.sthm')
n4.loadJSON('..\data\N4B8.sthm')

probes=np.array([c2,c3,c4,n1,n2,n3,n4])

c2.cutout

plt.cla()
for p in probes:
    plt.scatter(p.type,p.Ifit[1],label=p.cutout,c=['red' if p.cutout=='C' else 'grey'])

plt.xlabel('Sensor Size (um)')
plt.ylabel('a, $x^3$ coefficient')
#plt.legend(loc='')
plt.plot(0,0,color='None')
plt.savefig('a_vs_type.png')
plt.show()
