import Tkinter as tk
import numpy as np
import TCRfuncs as TC
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
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
import datetime
import numpy.polynomial.polynomial as poly


class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = rows
        self.columns = columns

        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="focusout", validatecommand=vcmd)
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
                if column == 0: e.insert(0,"{0}".format(row*0.25))
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(self._entry[index].get())
            result.append(current_row)
        return result

    def _validate(self, P):
        '''Perform input validation.

        Allow only an empty value, or a value that can be converted to a float
        '''
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self, 21, 2)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.titles = tk.Label(self, text='Input Bias (V), Circuit Output (mV)')
        self.titles.pack()
        self.table.pack(side="top", fill="both", expand=True)
        self.submit.pack(side="bottom")

    def on_submit(self):
        #print(self.table.get())
        n=[]
        global data
        data=np.array(self.table.get())
        for num,line in enumerate(data):
            #print line
            if '' in line:
                print 'found blank on line', num, line
                n.append(num)
        data=(np.delete(data, (n), axis=0))
        data=data.astype(float)

        plotdata(data)

        coefs = poly.polyfit(data[:,0], data[:,1], 2)
        print coefs
        ffit = poly.polyval(data[:,0], coefs)
        plt.plot(data[:,0], ffit,label='2nd Order Polynomial Fit')

        plt.savefig(datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + bridgename + '.png')
        #plt.show()
        np.save(datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + bridgename,data)
        print 'saving file as:', datetime.datetime.now().strftime("[%Y-%m-%d %H%M]") + bridgename
        print 'exiting'
        root.destroy()
        """
        temp=TC.pt100conv(data[:,0])
        print 'temp', temp

        #def probeR3(Vbias,Vout, Gain, r1, rm)
        ProbeR=data[:,1]
        print ProbeR


        TC.plotTCR(temp,ProbeR)
        """

def plotdata(data):
    plt.cla()
    plt.scatter(data[:,0],data[:,1])
    ax=plt.gca()
    ax.set_xlabel('Bridge Bias (V)')
    ax.set_ylabel('Bridge Output (mV)')


def run():
    bridgename=raw_input('Please enter the name of the bridge you are testing: ')
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
