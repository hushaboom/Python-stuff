#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from func import *

class Top(Tk):

    def __init__(self, parent):

        Tk.__init__(self, parent)
        self.parent = parent

        self.grid_propagate(False)

        self.coreFrame = LabelFrame(self,text=u'CPU Usage')
        self.coreFrame.grid(row=0, column=0, padx=5, pady=15, sticky='N', columnspan=3)
        self.topFrame = LabelFrame(self,text=u'Memory')
        self.topFrame.grid(row=1, column=2, padx=25, pady=2, sticky='NW')
        self.bttmFrame = LabelFrame(self)
        self.bttmFrame.grid(row=8, column=2, padx=25, pady=5, sticky='E', columnspan=2)
        self.hddFrame = LabelFrame(self,text=u'HDD Status')
        self.hddFrame.grid(row=4, column=0, padx=25, pady=5, sticky='N', columnspan=3)

        self.exButt = Button(self.bttmFrame,width=6,text=u'Exit',command=lambda: self.endIt())
        self.exButt.grid(row=1, sticky='E')
        self.display()

    def display(self):

        memlabel = Label(self.topFrame,text="Used: 0%")
        memlabel.grid(column=0,row=5)
        memlabelB = Label(self.topFrame,text="MB")
        memlabelB.grid(column=2,row=5)
        membar = Progressbar(self.topFrame,length=100,maximum=100,mode='determinate')
        membar.grid(column=1,row=5)
        membar['value'] = 0

        freeLabel = Label(self.topFrame,text="Free: 0%")
        freeLabel.grid(column=0,row=6)
        freeLabelB = Label(self.topFrame,text="MB")
        freeLabelB.grid(column=2,row=6)
        freebar = Progressbar(self.topFrame,length=100,maximum=100,mode='determinate')
        freebar.grid(column=1,row=6)
        freebar['value'] = 0

        cacheLabel = Label(self.topFrame,text="Cache: 0%")
        cacheLabel.grid(column=0,row=7)
        cacheLabelB = Label(self.topFrame,text="MB")
        cacheLabelB.grid(column=2,row=7)
        cachebar = Progressbar(self.topFrame,length=100,maximum=100,mode='determinate')
        cachebar.grid(column=1,row=7)
        cachebar['value'] = 0

        if os.geteuid() == 0: # check if program is run as root
            button = Button(self.topFrame, width=6, text='Drop', command=lambda: dumpMem())
            button.grid(row=8,column=0,sticky='N')
            

        procFrame = LabelFrame(self,text=u'Top Processes',width='400')
        procFrame.grid(row=3, column=0, padx=25, pady=5, columnspan=3, sticky='N')
        procLabel = Label(procFrame,text="Top Processes")
        procLabel.grid(padx=5, pady=5)

        tempLabel = LabelFrame(self,text=u'Core Temp')
        tempLabel.grid(row=1,column=1,padx=15,pady=2,sticky='E'+'E')
        temp = Label(tempLabel,text="Temp")
        temp.grid(padx=5, pady=5)

        labelhd = Label(self.coreFrame,text="Label")
        labelhd.grid(column=0,row=14,sticky='SE',columnspan=3,padx=5)
       
        labelD = Label(self.coreFrame,text="Label")
        labelD.grid(column=0,row=0, columnspan=3, sticky='N')

        bars = []
        labels = []

        for i in range(cpuCounter()[0], cpuCounter()[1]):
            
            labelB = Label(self.coreFrame,text="CPU:%d"%i)
            labelB.grid(column=0,row=i+2,sticky='N'+'E')

            bar = Progressbar(self.coreFrame,length=200,maximum=freqMax(),mode='determinate')
            bar.grid(column=1,row=i+2,sticky='N')
            bar['value'] = 0
            bars.append(bar)

            label = Label(self.coreFrame,text="CPU%d Freq: 0 MHz"%i)
            label.grid(column=2,row=i+2,sticky='N'+'W')
            labels.append((labelB, label))

        def update():

            strn, freestr, cacstr = memGrab()[0], memGrab()[1], memGrab()[2]
            brst = '-'*80
            percent = float(strn.split()[1][:-1])
            perfree = float(freestr.split()[1][:-1])
            cacfree = float(cacstr.split()[1][:-1])
            memlabel['text'] = strn+'%'
            membar['value'] = percent
            memlabelB['text'] = ' %03.2f Gb'%(float(memGrab()[3][0])/1000000)
            freeLabel['text'] = freestr+'%'
            freebar['value'] = perfree
            freeLabelB['text'] = ' %03.2f Gb'%(float(memGrab()[3][1])/1000000)
            cacheLabel['text'] = cacstr+'%'
            cachebar['value'] = cacfree
            cacheLabelB['text'] = ' %03.2f Gb'%(float(memGrab()[3][2])/1000000)
            procLabel['text'] = brst+'\n%s'%sysInfo()+brst
            temp['text'] = coreTemp()
            labelhd['text'] = brst+'\n%s%s\nDiskIO: \n%s%s'%(driveStr()[0], brst, driveStr()[1],brst)
            labelD['text'] = brst+'\n'+utc()+'\n'+brst

            data = freqOut(cpuCounter())
            cpu = list(data.keys())
            frq = list(data.values())
            counter = 0
            freqAvg = 0

            self.coreFrame['text'] = hdd()[0]
            for b in bars:
                    
                strn = '    %.2f MHz' % float(frq[counter])
                strnB = '    CPU# %d    '%(counter+1)

                percent = float(frq[counter])
                labels[counter][1]['text'] = strn
                labels[counter][0]['text'] = strnB
                b['value'] = percent

                counter += 1
                
            self.after(100,update)
        
        update()

    def endIt(self):

        self.destroy()
        exit()

if __name__ == '__main__':

    app = Top(None)
    app.title(' - Mon Assis -')
    app.resizable(0,0)
    app.geometry('510x920')
    app.mainloop()