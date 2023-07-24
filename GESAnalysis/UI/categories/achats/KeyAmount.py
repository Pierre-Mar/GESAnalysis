import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class KeyAmount(QtWidgets.QWidget):
    """ Widget to draw a graph representing the amount for each NACRES key
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    
    
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class by setting the data and draw the graph

        Args:
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(KeyAmount, self).__init__(parent)
        
        # Data structure
        self.__years_ind = {}          # Dictionary of year
        self.__nacres_key_code = ['*'] # Nacres key code
        self.__data_achats = {}        # Dictionary of data
        self.__unit = ""               # Unit
        
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        self.__init_UI()
        
        self.__draw()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar and a button to control the graph and the nacres code
        widget_toolbar_button = QtWidgets.QWidget(widget_canvas)
        widget_toolbar_button.setContentsMargins(0, 0, 0, 0)
        widget_toolbar_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout_toolbar_button = QtWidgets.QHBoxLayout(widget_toolbar_button)
        toolbar = NavigationToolbar2QT(self.__figCanvas, widget_toolbar_button)
        button_code = QtWidgets.QPushButton("Code NACRES", widget_toolbar_button)
        button_code.setFixedHeight(20)
        layout_toolbar_button.addWidget(toolbar)
        layout_toolbar_button.addWidget(button_code)
        widget_toolbar_button.setLayout(layout_toolbar_button)
        
        # Add to widget canvas
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(widget_toolbar_button)
        layout_canvas.addWidget(self.__figCanvas)
        widget_canvas.setLayout(layout_canvas)
        
        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(widget_canvas)
        self.setLayout(layout_principal)
        

#######################################################################################################
#  Draw the graph in the canvas                                                                       #
#######################################################################################################
    def __draw(self) -> None:
        """ Draw the graph in the canvas
        """
        self.__axes.cla()
        
        
#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update_canvas(self, years_ind, data_dict) -> None:
        self.__years_ind = years_ind
        self.__data_achats = data_dict["data"]
        self.__unit = data_dict["unit"]