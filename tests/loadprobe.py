import sys
import os
sys.path.append(os.path.abspath('../sthm'))
import SThMprobes as sthm

testprobe=sthm.probe(1, 'test',1,'N')
print testprobe.name

testprobe.loadJSON('../data/C2C14.sthm')
print testprobe.name
testprobe.plot_fit('current')
