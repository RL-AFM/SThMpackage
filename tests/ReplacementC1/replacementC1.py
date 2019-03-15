import sys
import os
sys.path.append(os.path.abspath('../../sthm'))
import SThMprobes as sthm

##190302 This probe died upon trying to do the bridge sweep.

c1c9=sthm.probe(314.8, 'c9','C1')


c1c9.maxI
c1c9.input_bridge_test(0.25)


#fin
