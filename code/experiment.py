#!/usr/bin/python3

from threading import Thread

from time import sleep

from tkinter import Tk, Canvas, PhotoImage
from tkinter.constants import BOTH
from tkinter.ttk import Frame as ttkFrame, Style

class ExperimentApp(object):

    DEFAULT_WIDTH=640
    DEFAULT_HEIGHT=480

    def __init__(self, title="My Experiment", width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):

        self._root = Tk()
        self._root.geometry("{0}x{1}".format(width,height))
        self._root.configure()
        self._root.title(title)

        self._frame = ttkFrame(self._root)
        self._frame.style = Style()
        self._frame.style.theme_use("default")
        self._frame.pack(fill=BOTH, expand=1)

        self._canvas = Canvas(self._frame, bg="#c0c0c0")
        self._canvas.pack(fill=BOTH, expand=1)
        
        self._running = False
        self._period = 1
        
        
    def setPollingPeriod(self, period):
    
        self._period = period
        

    def getValues(self):
    
        raise NotImplementedError()
        
        
    def _doPoll(self):
    
        sleep(1) #wait for mainloop initialization
        while self._running:

            coords = self.getValues()
            self._drawValues(coords)
            sleep(self._period)
            
            
    def _drawValues(self, coords):
    
        x1 = coords[0]-1
        x2 = coords[0]+1
    
        y1 = coords[1]-1
        y2 = coords[1]+1
        
        self._canvas.create_oval((x1, y1, x2, y2), fill="#0000ff", outline="#0000ff")


    def cleanup(self):
        pass


    def run(self):

        if not self._running:
        
            try:
                thread = Thread(target=self._doPoll)
                thread.start()
                self._running = True
                self._root.mainloop()
                self._running = False
                thread.join()
                
            finally:
                self.cleanup()
            
        else:
            raise Exception("Already running!")


if __name__ == '__main__':

    import random
    
    class ExampleApp(ExperimentApp):
    
        def __init__(self):
        
            super().__init__("Example App")
            

        def getValues(self):    
            return (100,random.randint(50, 150))
        

    ExampleApp().run()
    