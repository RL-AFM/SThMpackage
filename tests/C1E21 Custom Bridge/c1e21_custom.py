import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm
import matplotlib.pyplot as plt


#!GAIN SHOULD BE CALCULATED PROPERLY FROM OPAMP DATASHEET
#set up the probe & bridge: we used a custom bridge with higher gain for this experiment
c1e21=sthm.probe(199, name='E21_custom', style='c1',gain=1000)

#immediately we should correct the limiting resistor values. because this is a different bridge,
#the automatic calculation for the other bridge does not apply.
#Rl affects the calculation of current in the sweep
c1e21.Rl=55000

#enter the bridge sweep data
c1e21.load_curve('[2019-03-14 1835]c1E21_custom')

#print it out, in mV
c1e21.display_data()




c1e21.fit_self_heat_curve()
c1e21.plot_fit(yprefix='m')



c1e21.fit_self_heat_curve('current')
c1e21.plot_fit('current',yprefix='u')
"""
c1e21.saveJSON()

"""
