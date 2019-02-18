import sys
import os
sys.path.append(os.path.abspath('../sthm'))
import SThMprobes as sthm



#make a new instance - initialises to default values
c3=sthm.probe()

#load the data from a previous instance
c3.loadJSON('..\data\C3C19.sthm')

#show the bridge sweep data
c3.display_data()

#do the curve fitting. Should be redundant as this the fit is now done upon data entry
c3.fit_self_heat_curve('current')
c3.fit_self_heat_curve()
c3.plot_fit('current',save='y')
c3.plot_fit(save='y')

"""save the file again. it will have the same name, since we have not changed the
name, type or cutout attributes that make up its name. saveJSON will ask for
confirmation if the file already exists however"""
c3.saveJSON()
