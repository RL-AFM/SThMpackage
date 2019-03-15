import sys
import os
sys.path.append(os.path.abspath('../sthm'))
import SThMprobes as sthm


#19/02/19 We didn't do the fits for the control probes K1 and K2
#We have the saved bridge data though, so we can do it here manually
#remember to check the correct bridge resistances


#make new instances for these previously tested probes
k1=sthm.probe(437,'k1', 'k')
k1.load_curve('../data/190207 Initial Bridge Testing/[2019-02-06 1524]K1_437')
k1.display_data()
k1.plot_fit('current')
k1.saveJSON()
k1.Rm
k1.Rl
k1.Rb
"""k1 autcalculated resistors matches what we have on the bridge PCB"""

k2=sthm.probe(429,'k2', 'k')
k2.load_curve('../data/190207 Initial Bridge Testing/[2019-02-06 1127]K2_429')
k2.display_data()
k2.plot_fit('current')
k2.saveJSON()
k2.Rm
k2.Rl
k2.Rb

"""k2 autcalculated resistors matches what we have on the bridge PCB"""

c2
c2.display_data()
c2.name='C2C14_newBridge'
c2.saveJSON()
