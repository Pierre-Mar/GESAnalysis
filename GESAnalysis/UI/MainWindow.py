import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from GESAnalysis.UI.plot.DistanceMode import DistanceMode

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, readerdata_year_list, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.distance_canvas = DistanceMode(readerdata_year_list, self)
        self.setCentralWidget(self.distance_canvas)
        
        
        