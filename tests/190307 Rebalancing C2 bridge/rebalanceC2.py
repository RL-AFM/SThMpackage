import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm

c2=sthm.probe()
c2.loadJSON('../../data/C2C14.sthm')
c2.display_data()
c2.fit_self_heat_curve('current')
c2.plot_fit('current')

c2.name
c2.name='C14_reteset'


c2.Rm
c2.Rl
c2.Rb

c2.input_bridge_test(0.5)
c2.fit_self_heat_curve('current')
c2.plot_fit('current')
c2.Isweep*1e3

c2.display_data()
c2.data*1e3

plt.show()
c2.resistance+=3.2
c2.resistance
c2.calculate_bridge_resistors()

c2.input_bridge_test(0.5)
