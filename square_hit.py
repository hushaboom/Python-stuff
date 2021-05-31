# _*_ coding:utf-8 _*_
#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from math import sqrt
import time, random, threading



class Body(Tk):

    def __init__(self,parent):

        Tk.__init__(self,parent)

        self.dispVar = StringVar()
        self.diffVar = StringVar()
        self.gridVar = StringVar()
        self.score = StringVar()
        self.miss = StringVar()

        self.timer = 1.62
        self.rate = 0.05
        self.pad = 3
        self.grids = [3,4]
        self.tally = 0
        self.misses = 0
        self.totalmissed = 0
        self.diff = 0
        self.gridClick = 0

        self.txtList = ['Easy', 'Norm', 'Hard']
        self.bgList = ['blue', 'yellow', 'red']

        self.tallyman = [0]

        self.wm_attributes('-type','splash')

        self.mainMenu()


    def mainMenu (self):

        self.butts = list()

        self.lastNum = 0

        self.end = False
        self.start = True
        self.click = False
        self.switch = False

        self.txt = 'white'

        grid = self.grids[self.gridClick]

        self.size = pow(grid,2)

        self.gridVar.set('%sx%s' % (grid, grid))
        self.diffVar.set('')

        txt = '      Square Hit\n\nHit Red Square \n50 times to win\n\nMiss 5 times to lose\n\nSelect difficulty \nand Grid size\nPress Start when ready!'
        self.dispVar.set(txt)

        self.mFrame = LabelFrame(self, text = u'Square Hit', bg = '#c3cbc8')
        self.mFrame.grid(padx = 9, pady = 9, sticky = 'nsew')

        self.display = Label(self.mFrame, width = 22, text = self.dispVar, textvariable = self.dispVar, anchor = "n", justify = "left", font = ("Arial", 15), height = 8, bg = '#04332a', fg ='#b1ced8')
        self.display.grid(row = 0, column = 1, rowspan = 3, padx = 4, pady = 4, sticky = 'nsew')

        self.buttFrame = LabelFrame(self.mFrame, bg = '#c3cbc8')
        self.buttFrame.grid(row = 3, column = 1, padx = 4, pady = 4, sticky = 'new')

        self.infoFrame = LabelFrame(self.mFrame, text = 'Grid Size', bg = '#c3cbc8')
        self.infoFrame.grid(row = 0, column = 2, rowspan = 1, padx = 4, pady = 4, sticky = 'new')

        self.scoreFrame = LabelFrame(self.mFrame, text = 'Hits:', bg = '#c3cbc8')
        self.scoreFrame.grid(row = 0, column = 0, padx = 4, pady = 4, sticky = 'n')

        self.missFrame = LabelFrame(self.mFrame, text = 'Miss:', bg = '#c3cbc8')
        self.missFrame.grid(row = 1, column = 0, padx = 4, pady = 4, sticky = 'N')

        self.missinfo = Label(self.missFrame, textvariable = self.miss, text = self.miss, font = ("Arial", 15), justify = 'center', width = 3, height = 3, bg = '#c3cbc8')
        self.missinfo.grid(row = 0, column = 0, rowspan = 3, padx = 4, pady = 4, sticky = 'n')

        self.info = Label(self.infoFrame, textvariable = self.gridVar, text = self.gridVar, font = ("Arial", 15), justify = 'center', width = 3, height = 3, bg = '#c3cbc8')
        self.info.grid(row = 0, column = 0, rowspan = 3, padx = 4, pady = 4, sticky = 'n')

        self.tab = Label(self.scoreFrame, textvariable = self.score, text = self.score, font = ("Arial", 15), justify = 'center', width = 3, height = 3, bg = '#c3cbc8')
        self.tab.grid(row = 0, column = 0, rowspan = 3, padx = 4, pady = 4, sticky = 'n')

        self.btinfo = Button(self.infoFrame, width = 2, height = 1, text = 'Grid', fg = 'white', bg = 'navy blue', command = lambda: self.gridsel())
        self.btinfo.grid(row = 3, column = 0, padx = 3, pady = 3, sticky = 'S')

        self.btgo = Button(self.buttFrame, width = 2, height = 1, text = 'Start', fg = 'black', bg = '#00ff00', command = lambda: self.OnButtonClick('start'))
        self.btgo.grid(row = 0, column = 0, padx = 3, pady = 3)

        self.dFrame = LabelFrame(self.mFrame, text = 'Difficulty', bg = '#c3cbc8')
        self.dFrame.grid(row = 1, column = 2, padx = 4, pady = 4, sticky = 'w')

        self.infotab = Label(self.dFrame, textvariable = self.diffVar, text = self.diffVar, font = ("Arial", 12), justify = 'left', width = 9, height = 3, bg = '#c3cbc8')
        self.infotab.grid(row = 0, column = 0, columnspan = 2, padx = 4, pady = 4, sticky = 'w')

        self.btdif = Button(self.dFrame, width = 2, height = 1, text = self.txtList[self.diff], fg = self.txt, bg = self.bgList[self.diff], command = lambda: self.difficulty())
        self.btdif.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = 'n')

        self.btno = Button(self.buttFrame, width = 2, height = 1, text = 'Quit', fg = 'white', bg = '#370000', command = lambda: self.quitter())
        self.btno.grid(row = 0, column = 2, padx = 3, pady = 3)


    def passer (self, flag = 1, state = False):

        if self.click:

            return

        self.click = True

        if state:

            self.switch = True

            try:

                self.go.join()

            except:

                pass

            self.go = threading.Thread(target = self.player, args = ())

            if flag == 1:

                if self.misses > 0:

                    if self.diff == 0:

                        self.misses -= 1
                        self.tally += 1

                        if self.tally % 5 == 0 and self.tally not in self.tallyman:

                            self.timer -= (self.timer * self.rate)
                            self.tallyman.append(self.tally)

                    else:

                        self.misses -= 1

                    self.miss.set(self.misses)

                else:

                    self.tally += 1

                    if self.tally % 5 == 0 and self.tally not in self.tallyman:

                        self.timer -= (self.timer * self.rate)
                        self.tallyman.append(self.tally)

                [i.destroy() for i in self.butts]

                self.score.set(self.tally)

                if self.tally == 50:

                    self.ender(True)

                else:

                    self.go.start()

            else:

                self.switch = True
                self.misses += 1
                self.totalmissed += 1
                self.miss.set(self.misses)

                if self.diff == 2:

                    self.tally -= 1

                    if self.tally < 0:

                        self.tally = 0

                    self.score.set(self.tally)

                [i.destroy() for i in self.butts]

                if self.misses == 5:

                    self.ender(False)

                else:

                    self.go.start()

        else:

            try:

                self.go.join()

            except:

                pass

            [i.destroy() for i in self.butts]

            if self.diff > 0:

                self.misses += 1
                self.totalmissed += 1
                self.miss.set(self.misses)

                if self.diff == 2:

                    self.tally -= 1

                    if self.tally < 0:

                        self.tally = 0

                    self.score.set(self.tally)


                if self.misses == 5:

                    self.ender(False)

                else:

                    self.go = threading.Thread(target = self.player, args = ())
                    self.go.start()

            else:

                self.go = threading.Thread(target = self.player, args = ())
                self.go.start()

    def ender (self, state):

        [i.destroy for i in [self.display, self.btno]]

        self.display = Label(self.mFrame, width = 22, text = self.dispVar, textvariable = self.dispVar, anchor = "n", justify = "left", font = ("Arial", 15), height = 8, bg = '#04332a', fg ='#b1ced8')
        self.display.grid(row = 0, column = 1, rowspan = 3, padx = 4, pady = 4, sticky = 'nsew')

        self.btgo = Button(self.buttFrame, width = 2, height = 1, text = 'Menu', fg = 'black', bg = '#00ff00', command = lambda: self.OnButtonClick('menu'))
        self.btgo.grid(row = 0, column = 0, padx = 3, pady = 3)

        self.btno = Button(self.buttFrame, width = 2, height = 1, text = 'Quit', fg = 'white', bg = '#370000', command = lambda: self.quitter())
        self.btno.grid(row = 0, column = 2, padx = 3, pady = 3)

        total = self.tally - self.totalmissed

        txt = "Hit: %s\nMissed: %s\nTotal: %s" % (self.tally, self.totalmissed, total)

        if total == 50:

            txt += "\n!!  Perfect Game  !!"

        self.dispVar.set(txt)

        pass

    def OnButtonClick (self, event, switch = False):

        if event == 'start':

            [i.destroy() for i in [self.btgo, self.btdif, self.btinfo]]

            self.dispVar.set('')
            self.diffVar.set(self.txtList[self.diff])
            self.score.set(0)
            self.miss.set(0)

            self.display.destroy()

            self.display = Label(self.mFrame, width = 22, text = self.dispVar, textvariable = self.dispVar, anchor = "n", justify = "left", font = ("Arial", 15), height = 3, bg = '#04332a', fg ='#b1ced8')
            self.display.grid(row = 0, column = 1, rowspan = 3, padx = 4, pady = 4, sticky = 'nsew')

            self.display.bind("<Button-1>", self.bgclick)

            self.go = threading.Thread(target = self.player, args = ())
            self.go.start()

        elif event == 'menu':

            [i.destroy() for i in [self.btgo, self.btdif, self.btinfo, self.display, self.buttFrame, self.infoFrame, self.scoreFrame, self.missFrame, self.missinfo, self.info, self.tab, self.btinfo, self.dFrame, self.infotab, self.mFrame]]

            self.dispVar.set('')
            self.diffVar.set(self.txtList[self.diff])

            self.score.set(0)
            self.miss.set(0)

            self.tally = 0
            self.misses = 0
            self.totalmissed = 0

            st = self.grids[self.gridClick]

            txt = '%sx%s' % (st, st)

            self.gridVar.set(txt)

            self.mainMenu()

    def player (self):

        mark = time.time()

        self.switch = False

        if self.gridClick > len(self.grids) - 1:

            self.gridClick = len(self.grids) - 1

        grid = self.grids[self.gridClick]

        st = self.grids[self.gridClick]

        txt = '%sx%s' % (st, st)

        self.gridVar.set(txt)

        w = 3 - self.diff

        r,c = 0,0

        pick = random.randint(0, pow(grid, 2) - 1)

        while pick == self.lastNum:

            pick = random.randint(0, pow(grid, 2) - 1)

        self.lastNum = pick

        self.butts = []

        color0 = 'grey'
        color1 = 'red'

        for i in range(0, pow(grid, 2)):

            if i == pick:

                self.hitter = Button(self.display, width = w, height = w, bg = color1, command=lambda: self.passer(1, True))
                self.hitter.grid(row = r, column = c, padx = self.pad, pady = self.pad)
                self.butts.append(self.hitter)

            else:

                self.butts.append(Button(self.display, width = w, height = w, bg = color0, command=lambda: self.passer(0, True)))
                self.butts[-1].grid(row = r, column = c, padx = self.pad, pady = self.pad)


            c += 1

            if c == grid:

                r += 1
                c = 0

        self.display.grid_propagate(0)

        self.click = False

        while not self.switch:

            if time.time() > mark + self.timer:

                self.passer(0, False)
                break

    def bgclick (self, event):

        if self.diff == 2:

            self.passer(0, True)


    def difficulty (self):

        self.diff += 1
        color = 'white'

        if self.diff == 3:

            self.diff = 0

        if self.gridClick > len(self.grids) - 1:

            self.gridClick = len(self.grids) - 1

        if self.diff == 0:

            self.timer = 1.8
            self.rate = 0.05
            self.pad = 3
            self.grids = [3,4]

        elif self.diff == 1:

            self.timer = 1.65
            self.rate = 0.045
            self.pad = 6
            self.grids = [3,4,5]
            color = 'black'

        elif self.diff == 2:

            self.timer = 1.5
            self.rate = 0.055
            self.pad = 9
            self.grids = [3,4,5,6]

        self.btdif.destroy()

        self.btdif = Button(self.dFrame, width = 2, height = 1, text = self.txtList[self.diff], fg = color, bg = self.bgList[self.diff], command = lambda: self.difficulty())
        self.btdif.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = 'n')

        pass


    def gridsel (self):

        l = len(self.grids) - 1

        self.gridClick += 1

        if self.gridClick > l:

            self.gridClick = 0

        st = self.grids[self.gridClick]

        txt = '%sx%s' % (st, st)

        self.gridVar.set(txt)


    def quitter (self, switch = True):

        self.switch = True

        if switch:

            p = messagebox.askyesno('Quit Square Hit', 'Quit!?\nAre you for real?')

        if p or not switch:

            [i.destroy() for i in self.butts]

            try:

                self.go.join()

            except:

                pass

            self.destroy()

        else:

            self.destroy()

            app = Body(None)
            app.configure(bg = '#000018')
            app.title('Square Hit')
            app,mainloop()



if __name__ == '__main__':

    app = Body(None)
    app.configure(bg = '#000018')
    app.title('Square Hit')
    app,mainloop()
