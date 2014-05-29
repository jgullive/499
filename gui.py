from Tkinter import *
from sensors import *
import sys

class Application(Frame):
    
    def sys_start(self):
        print "Brew started!"
        
        self.sys_control.systemOn = 1
        self.start_button["text"] = "SYSTEM OFF"
        self.start_button["command"] = self.sys_stop

    
    def sys_stop(self):
        print "Brew stopped!"
        self.sys_control.systemOn = 0
        self.start_button["text"] = "SYSTEM ON"
        self.start_button["command"] = self.sys_start
    
    def read_xml(self):
        path = self.xml_input.get()
        self.sys_control.recipe_profile.grain_weight = self.sys_control.recipe_xml.read_xml(path)
    
        self.create_start_button()
    
    def create_start_button(self):
        self.start_button["text"] = "SYSTEM ON"
        self.start_button["command"] = self.sys_start
    
    
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})
        
        self.xml_button = Button(self)
        self.xml_button["text"] = "READ XML"
        self.xml_button["command"] = self.read_xml
        self.xml_button.pack({"side": "left"})
    
        self.xml_input = Entry(self)
        self.xml_input.pack({"side": "left"})
    
        self.start_button = Button(self)
        self.start_button["text"] = "            "
        self.start_button.pack({"side": "bottom"})
    
    def __init__(self, sys_control, master=None):
        self.sys_control = sys_control
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def open_gui(sys_control):
    
    
    print "gui created"
    root = Tk()
    app = Application(sys_control, master=root)
    app.mainloop()
    root.destroy()
    
    print "Exiting from gui."

    sys.exit()