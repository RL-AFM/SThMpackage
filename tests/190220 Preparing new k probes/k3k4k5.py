import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm



k3=sthm.probe(421, 'k3','k')
k4=sthm.probe(418, 'k4','k')

#input the bridge sweep here, but can't save the JSON output here because the sthm package defines the save path.
#thankfully the .npy file was saved, so we can load it
#k3.input_bridge_test(0.5)
#k3.saveJSON()

k3.load_curve('[2019-02-21 0957]kk3')
k3.display_data()
k3.Ifit

k3.plot_fit('current', save='y')
k3.saveJSON()
k4.input_bridge_test(0.5)

k4.plot_fit('current',save='y')
k4.saveJSON()
