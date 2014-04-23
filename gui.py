from Tkinter import *
from sensors import *
import sys

global inputs

class Application(Frame):
    def mash_on(self):
        print "mash ON!"
        inputs['mash_temp'] = 1
        self.mash_valve["text"] = "Mash OFF"
        self.mash_valve["command"] = self.mash_off
    
    def mash_off(self):
        print "mash OFF!"
        inputs['mash_temp'] = 0
        self.mash_valve["text"] = "Mash ON"
        self.mash_valve["command"] = self.mash_on
    
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        
        self.QUIT.pack({"side": "left"})
        
        self.mash_valve = Button(self)
        self.mash_valve["text"] = "Mash ON"
        self.mash_valve["command"] = self.mash_on
        
        self.mash_valve.pack({"side": "left"})
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def open_gui():
    
    print "gui created"
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    
    print "Exiting from gui."

    sys.exit()