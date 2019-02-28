#!/usr/bin/python3

from threading import Thread

from time import sleep

from tkinter import Tk, Canvas, PhotoImage
from tkinter.constants import BOTH
from tkinter.ttk import Frame as ttkFrame, Style

class ExperimentApp(object):
    '''
    Basical window to show data provided by devices like sensors.
    It let show the behaviour of the read values through time.
    '''

    PADDING = 10

    def __init__(self, title="My Experiment", width=640, height=480, numPolls=100):
        '''
        Constructor.
        Derived classes can extend this method in order to set up the data provider.
        
        @param title: Window's title
        @param width: Window's width as pixels
        @param heigh: Window's heigh as pixels
        @param numPolls: Maximal number of polls shown on the screen
        '''

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
        
        self._numPolls = numPolls
        self._pollStep = (width - 2*ExperimentApp.PADDING) // self._numPolls
        self._points = []
        
        
    def setPollingPeriod(self, period):
        '''
        Set the time between polls
        
        @param period: Time in seconds
        '''
    
        self._period = period
        

    def getValues(self):
        '''
        Get the values from the provider.
        This method must be implemented by derived classes,
        otherwise a NonImplementedError will be raised.
        
        It is expected to return a list of values
        '''
    
        raise NotImplementedError()
        
        
    def _doPoll(self):
    
        sleep(1) #wait for mainloop initialization
        while self._running:

            values = self.getValues()
            self._drawValues(values)
            sleep(self._period)
            
            
    def _drawValues(self, values):
    
        #Move current points
        movedPoints = []
        for point in self._points:
            
            self._canvas.move(point, -self._pollStep, 0)
            coords = self._canvas.coords(point)
            
            if coords[0] > ExperimentApp.PADDING:
                movedPoints.append(point)
            else:
                self._canvas.delete(point)
        
        self._points = movedPoints
    
        #Draw new points
        originX = self._canvas.winfo_width() - ExperimentApp.PADDING
        
        for value in values:
        
            x1 = originX-1
            x2 = originX+1
    
            y1 = value-1
            y2 = value+1
        
            self._points.append(self._canvas.create_oval((x1, y1, x2, y2), fill="#0000ff", outline="#0000ff"))
            
        self._canvas.update()


    def cleanup(self):
        '''
        Frees all resources.
        This method does nothing by default, but can be extended to release or stop any
        data provider.
        '''
        
        pass


    def run(self):
        '''
        Shows the window and start polling
        '''

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
        
            super().__init__("Example App", numPolls=10)
            

        def getValues(self):
        
            return [random.randint(50, 150)]
        

    ExampleApp().run()
    
