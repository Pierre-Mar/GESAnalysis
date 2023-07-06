import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from GESAnalysis.FC.PATTERNS.Observer import Observer
from typing import Tuple, List

import GESAnalysis.UI.categories.common as common 


class TotalEmission(QtWidgets.QWidget, Observer):
    """ Class to draw a graph representing the emission for each year
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    __spacing = 0.8                                 # Spacing between bars of each mode
    
    
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class by setting the data and draw the graph

        Args:
            model (GESAnalysis): Model
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        super(TotalEmission, self).__init__(parent)
        
        self.__years_ind = {}
        self.__name_ind = {}
        self.__data_tot = {}
        self.__unit = ""
        
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Initialise the UI
        self.__init_UI()
        
        # Draw the graph
        self.__draw()
        

#######################################################################################################
#  Initialisation of the interface                                                                    #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialize the UI
        """
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)
        
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(widget_canvas)
    

#######################################################################################################
#  Draw the graph in the canvas                                                                       #
####################################################################################################### 
    def __draw(self) -> None:
        """ Draw the graph in the figure canvas
        """
        # Clear the canvas
        self.__axes.cla()
        
        # Get the position for the labels and the labels
        x_bars, x_labels = self.__get_x_label()
        
        y_labels = ["" for i in range(len(self.__name_ind.keys()))]
        bottom = [0 for i in x_bars] # Useful for stacked bar
        
        # Add bar to the graph
        for name, data_name in self.__data_tot.items():
            self.__axes.bar(x_bars, data_name["data"], width=self.__width, bottom=bottom, linewidth=0.5, edgecolor='black')
            for i in range(len(bottom)):
                bottom[i] += data_name["data"][i]
            y_labels[self.__name_ind[name]["index"]] = name
        
        # Set x labels
        self.__axes.set_xticks(x_bars, x_labels)
        
        # Put a legend if there are data display
        if len(y_labels):
            self.__axes.legend(y_labels)
        
        # Put a label on y-axis
        self.__axes.set_ylabel(f"Empreinte carbonne ({self.__unit})")
        
        # Draw the canvas
        self.__figCanvas.draw()
        
        
    def __get_x_label(self) -> Tuple[List[str], List[str]]:
        """ Create a list to place the label in x-axis and another list with the label

        Returns:
            Tuple[List[str], List[str]]: Lists
        """
        current_space = 0
        x_bars = [] # Contains the position of the labels
        x_labels = ["" for i in range(len(self.__years_ind.keys()))]
        for year in self.__years_ind.keys():
            x_bars.append(current_space)
            current_space += self.__spacing
            x_labels[self.__years_ind[year]["index"]] = year
        return x_bars, x_labels
            

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update_canvas(self, name_ind, years_ind, data_dict) -> None:
        """ Update the structure when the model are updated
        """
        self.__years_ind = years_ind
        self.__name_ind = name_ind
        self.__data_tot = data_dict["data"]
        self.__unit = data_dict["unit"]

        self.__draw()