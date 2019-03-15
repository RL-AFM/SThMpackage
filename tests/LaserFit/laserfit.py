import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm

k1=sthm.probe()
k1.loadJSON('..\..\data\kk1.sthm')

k1.input_bridge_test(0.5)
k1.display_data()
k1.fit_self_heat_curve()
k1.fit_self_heat_curve('current')
k1.fullname='k1_laser_on'
k1.plot_fit('current')


k1_no_laser=sthm.probe().
k1_no_laser.loadJSON('..\..\data\kk1.sthm')
k1_no_laser.plot_fit('current')


#is there an explaination for th 1% x3 error. the self heating power is greater when the resistance is higher ( resistance increase casued by greater R0 because of laser heat).


k4=sthm.probe()
k4.loadJSON('..\..\data\kk4.sthm')
k4.fullname='k4_no_laser'
k4.plot_fit('current',save='y')

k4.fullname='k4_laser_on'
k4.input_bridge_test(0.5)
k4.plot_fit('current',save='y')
