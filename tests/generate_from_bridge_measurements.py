import SThMprobes as sthm


"""Before the software was fully developed, we had some numpy files with bridge
balance data. This file initialises a bunch of probes and adds their relevant
test data. In the future, the fitting of curves"""

#<codecell>
#----------------------------------------------------------------------------------------------------------------
#filenames
C2='../data/190207 Initial Bridge Testing\[2019-02-07 1516]C2_C14'
C4='../data/190207 Initial Bridge Testing\[2019-02-07 1452]C4_A8'
C3='../190207 Initial Bridge Testing\[2019-02-07 1507]C3_C19'
C3v2='../data/190207 Initial Bridge Testing\[2019-02-12 1612]C3C19'
N1='../data/190207 Initial Bridge Testing\[2019-02-07 1436]N1_B9'
N2='../data/190207 Initial Bridge Testing\[2019-02-07 1348]N3_B3'
N3='../data/190207 Initial Bridge Testing\[2019-02-07 1348]N3_B3'
N4='../data/190207 Initial Bridge Testing\[2019-02-06 1534]N4_B8'


N='N'
C='C'

#bridge resistances are slightly off!!!!
#make new instances for all four of the non-cutout probes
N1B9=sthm.probe(307.8, 'B9', 1, N)
N2B10=sthm.probe(247.0, 'B10', 2 , N)
N3B3=sthm.probe(195.5, 'B3', 3, N)
N4B8=sthm.probe(170.3, 'B8', 4, N)
#The bridges for these probes are correct
C4A8=sthm.probe(158.3, 'A8', 4 ,   C)
C3C19=sthm.probe(169.5, 'C19', 3 , C)
C2C14=sthm.probe(116.5, 'C14', 2 , C)

#load the previously saved bridge balance data
N1B9.load_curve(N1)
N2B10.load_curve(N2)
N3B3.load_curve(N3)
N4B8.load_curve(N4)
C4A8.load_curve(C4)
C3C19.load_curve(C3v2)
C2C14.load_curve(C2)
#C1 probe was broken


#
cutouts=[C4A8,C3C19,C2C14]
non_cutouts=[N1B9,N2B10,N3B3,N4B8]

allprobes=cutouts+non_cutouts
for n in allprobes:n.saveJSON()
