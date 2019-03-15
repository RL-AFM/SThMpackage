import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
from matplotlib import style
import pickle
style.use('ggplot')
rc('text', usetex=True)
rc('figure', figsize=(5.59,3.14),dpi=200)
matplotlib.rcParams['font.serif'] = 'CMU Serif'
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 11
matplotlib.rcParams['text.color'] = 'xkcd:charcoal grey'
matplotlib.rcParams['axes.labelcolor'] = 'xkcd:charcoal grey'
matplotlib.rcParams['xtick.color'] = 'xkcd:charcoal grey'
matplotlib.rcParams['ytick.color'] = 'xkcd:charcoal grey'
matplotlib.rcParams['figure.subplot.bottom'] = 0.155
matplotlib.rcParams['figure.subplot.left'] = 0.155
import json #https://docs.python.org/2/library/json.html
import os

#Scipy optimisation used for fitting curves to custom functions
from scipy.optimize import curve_fit


import datetime #date and time package for giving saved files timestamps

import standard_resistors   #library for standard resistor vaules at differnet tolerances, with some additional functions

#the tolerance sets in standard resistors.py
Tol1=standard_resistors.e96
Tol2=standard_resistors.e48
Tol5=standard_resistors.e24
Tol10=standard_resistors.e12
Tol0p5=standard_resistors.e192


#for nice display of data in the atom interactive window, can also output latex formatted tables
import tabulate
from IPython.display import HTML, display

import num2tex #simple script for getting latex formatted eng-style numbers


#<codecell>
#----------------------------------------------------------------------------------------------------------------

#function that describes the form of a probe during self heating
def xcubed(x,s,a,b):
    return (s*x) + (a*x**3) + b

class probe(object):

    def __init__(self,resistance=300,name='UN-INITIALISED',style='k',gain=101.):
        self.resistance=resistance
        self.name=name
        self.style=style
        self.fullname= self.style + self.name
        self.data=None
        self.maxI=self.choose_I_from_type()
        self.calculate_bridge_resistors()
        self.Vfit=None
        self.gain=gain
        self.Isweep=None
        self.Vsweep=None


    #selects the max current based upon the sensor size (1,2,3 or 4).
    #Look up table contains the maxcurrent based on current density, divided by two for safety while testing
    def choose_I_from_type(self):

        #make sure the style is somewhat reasonable
        if not any(n in self.style for n in ['1','2','3','4','k']): raise ValueError('Invalid probe type')

        #if it's a regular probe, set the max current as 2mA
        if 'k' in self.style:
            return 2e-3
        else:
            sensor_width=int(self.style[1])
            if not any(n == sensor_width for n in range(1,5)): raise ValueError('type can only be between 1 and 4')

            currentlims=np.array([0.23,0.465,0.695,0.925])*1e-3
            #print 'Maximum Current = {0:.2f}mA'.format(currentlims[n-2]*1e3)
            return currentlims[sensor_width-1]

    #load a saved .npy file containing the bridge V-V sweep info
    def load_curve(self, filename):
        self.data=np.load(filename+'.npy')
        self.scale_input()
        print 'loaded bridge V-mV data from file {0}'.format(filename)

        print 'processing plots for current and voltage'
        self.fit_self_heat_curve('voltage')
        self.fit_self_heat_curve('current')
        #self.resistance_from_bridge_output()


    #transform between circuit output in mV and the bridge output voltage in V
    def scale_input(self):
        print 'Note: Input data has been scaled by the gain of the circuit, {0}x'.format(self.gain)
        self.data[:,1]=1e-3*self.data[:,1] #convert from mV input to V
        self.data[:,1]=self.data[:,1]/self.gain      #divide through by gain to get to the real signal


    #directly enter probe bridge sweep results. Increment is the voltge increment on the x axis
    def input_bridge_test(self,increment):
        Vin=np.arange(0,5+increment,increment)
        Vout=np.zeros(len(Vin))

        for n,v in enumerate(Vin):
            Vout[n]=raw_input('Enter output (mV) for input of {0}V'.format(v))

        self.data=np.column_stack((Vin.transpose(),Vout.transpose()))
        np.save(datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + self.fullname,self.data)
        self.scale_input()
        print 'Writing probe data:'
        self.display_data()
        print 'Fitting voltage and current curves'
        self.fit_self_heat_curve('voltage')
        self.fit_self_heat_curve('current')
        #self.display_data()



    #nicely display V-V sweep data in a table
    def display_data(self):
        if self.data is None:
            print 'No data to display'
            pass
        else:
            try:
                datacopy=np.copy(self.data)
                datacopy[:,1]=datacopy[:,1]*1e3 * self.gain    #make readable; convert to mV and include the circuit's gain
                display(HTML(tabulate.tabulate(datacopy,tablefmt="html",floatfmt=".3f",headers=('Bias(V)','Output (mV)'))))
            except AttributeError:
                print 'No data to display'


    #calculate the appropriate bridge resistors based on the probe resistance and max current
    def calculate_bridge_resistors(self):

        #probe resistance
        r1 = self.resistance
        #find the matching resistor lower than the probe resistance

        #matching resistor

        if r1>200:
            print 'Calculating bridge resistors using 5% tolerance'
            Rm=standard_resistors.floorCorrection(r1,Tol5)

        else:
            print 'Calculating bridge resistors using 0.5% tolerance'
            Rm=standard_resistors.floorCorrection(r1,Tol0p5)
        #Rm=standard_resistors.floorCorrection(r1,[Tol5 if r1>300 else Tol0p5])
        print 'Probe resistance = {0}'.format(r1)
        print 'Matching resistor chosen as {0}'.format(Rm)
        #find the resistor required for balancing the probe to the match
        try:
            Rb=(r1**-1 - Rm**-1)**-1
            Rb=standard_resistors.findNearestResistor(abs(Rb), Tol5)
            print 'Parallel resistance = {:.0f}'.format(Rb)
        except ZeroDivisionError:
            print 'perfect match, no parallel needed'
            Rb=0


        #use that current to define the value of the limiting resistors
        Rl=(5./self.maxI) - Rm
        #get the nearest standard value
        Rl=standard_resistors.findNearestResistor(abs(Rl), Tol5)
        print 'Limiting resistors = {:.0f}'.format(Rl)

        self.Rm=Rm
        self.Rb=Rb
        self.Rl=Rl

    #fit the self-heating/bridge testing curve using our custom fit routine
    def fit_self_heat_curve(self,sweeptype='voltage'):


        if self.data is None:
            print 'No data to fit'
            pass


        if sweeptype=='voltage':
            x=self.data[:,0]
            self.Vsweep=x

        elif sweeptype=='current':
            x=self.data[:,0]/(self.Rm + self.Rl)
            self.Isweep=x

        else: raise ValueError('Enter only current or voltage')

        y=self.data[:,1]


        print 'Calculating fit using {} as the x axis'.format(sweeptype)


        fit,fitcov=curve_fit(xcubed, x,y)


        if sweeptype=='voltage':self.Vfit=fit
        elif sweeptype=='current':self.Ifit=fit


    def scatterdata(self,xscale=1,yscale=1):
        plt.scatter(self.data[:,0]*xscale,self.data[:,1]*yscale)

    def plot_fit(self,kw='voltage',save=None,yprefix=''):

        y_multiplier={'k':1e-3,'':1,'m': 1e3, 'u':1e6 , 'n':1e9}

        if kw=='voltage':
            coeffs=self.Vfit
            maxbias=self.Vsweep[-1]
        elif kw=='current':
            coeffs=self.Ifit
            maxbias=self.Isweep[-1]
        else: raise ValueError('voltage and current are the only valid strings')
        xax=np.linspace(0,maxbias,50)

        plt.cla()
        condition = xax*1e3 if kw=='current' else xax
        plt.plot(condition, y_multiplier[yprefix]*xcubed(xax,*coeffs),label='$V_{{out}} = {0:.2f}x + {1:.2e}x^3 + {2:.2e}$'.format(coeffs[0],num2tex.num2tex(coeffs[1]),num2tex.num2tex(coeffs[2])))
        plt.plot(condition, y_multiplier[yprefix]*xax*coeffs[0],label='Bridge Imbalance')
        plt.plot(condition, y_multiplier[yprefix]*xax**3*coeffs[1],label='Only self-heating')
        if kw == 'voltage':
            plt.xlabel('Input Voltage (V)')
            self.scatterdata(yscale=y_multiplier[yprefix])

        if kw == 'current':
            plt.xlabel('Input current (mA)')
            plt.scatter(self.Isweep*1e3, y_multiplier[yprefix]*self.data[:,1])


        plt.ylabel('Output Voltage (before gain)({0}V)'.format(yprefix))

        plt.legend(loc='best')

        if save is not None:
            plt.savefig(datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + self.fullname + kw + 'sweep')
        plt.show()

    #return the resistance of the probe at each measurement point, given that the bridge resistors are all known
    #should have accounted for the circuits gain term already
    def resistance_from_bridge_output(self):
        Vin=self.data[:,0][1:]
        Vout=self.data[:,1][1:]
        res=(self.Rl/((Vout/Vin)+(self.Rl/(self.Rl+self.Rm))))-self.Rl
    	if self.Rb!=0:
    		res = ((res**-1)-(self.Rb**-1))**-1
        self.resistanceSweep= res
        return res

    def plot_resistance_curve(self, xtype,save=None):
        self.resistance_from_bridge_output()
        if xtype=='voltage':
            plt.scatter(self.Vsweep[1:],self.resistanceSweep)
            plt.xlabel('Bias Voltage (V)')
        elif xtype=='current':
            plt.scatter(self.Isweep[1:]*1e3, self.resistanceSweep)
            plt.xlabel('Bias Current* (mA)')
            plt.xlim(xmin=0, xmax=self.Isweep[1:][-1]*1e3)
        else: raise AttributeError('Only current and voltage are allowed')

        plt.ylabel('Resistance (Ohms)')
        if save is not None:
            plt.savefig(datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + self.fullname  + xtype + ' _vs_resistance')
        plt.show()




    #while JSON offers more readable output, it can't serialise numpy ndarrays, so we had to fix that
    #https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable

    def saveJSON(self):
        print 'Converting np arrays to lists for serialisation'
        output=self.__dict__        #make a copy so we dont change the one stored in memory
        for n,v in output.iteritems():
            if type(v)==np.ndarray:
                print n,'is a numpy array'
                output[n]=v.tolist()
                print 'should have converted'
        path=os.path.abspath('./'+self.fullname+'.sthm')
        if os.path.exists(path):
            response = raw_input('File already exists! Overwrite [y]?\n')
            if response != 'y': return 'Exited without saving'
        with open(path,'w') as file:
            json.dump(self.__dict__, file)

    #opposite of above, now we need to put the lists back into an array
    def loadJSON(self,fname):
        with open(fname, 'r') as f:
            foo=json.load(f)
        for n,v in foo.iteritems():
            if type(v)==list:
                print n,'is a list'
                foo[n]=np.asarray(v)
                print 'should have converted back'
        self.__dict__ = foo

print 'Imported SThM probe library'
