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
    
    
    def __init__(self, model, controller, category, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class by setting the data and draw the graph

        Args:
            model (GESAnalysis): Model
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        super(TotalEmission, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controller = controller
        
        # Add the graph to the observer when there is an update
        self.__gesanalysis.add_observer(self, category)
        
        self.__years_ind = {}
        self.__name_ind = {}
        self.__data_tot = {}
        
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Configure the data for the graph
        self.__configure_data()
        
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
#  Configure data to plot in the graph                                                                #
#######################################################################################################  
    def __configure_data(self) -> None:
        """ Configure the data for the graph
        """
        ind_year = 0
        ind_name = 0
        for val_ges in self.__gesanalysis.get_data().values():
            if val_ges["category"] != "Total":
                continue
            
            data = val_ges["data"]
            
            name = common.get_column(data, "name")
            if name is None:
                continue
            
            # Add all the year concerned for the graph
            year = val_ges["year"]
            if year not in self.__years_ind.keys():
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
            
            # Get all the post for each year
            for i in range(len(name)):
                if name[i][0] not in self.__name_ind.keys():
                    self.__name_ind[name[i][0]] = {"index": ind_name}
                    ind_name += 1
        
        # Create the structure
        for name in self.__name_ind.keys():
            self.__data_tot[name] = {}
            l = [0 for i in range(len(self.__years_ind.keys()))]
            self.__data_tot[name]["data"] = l
            
        # Fill the structure
        for val_ges in self.__gesanalysis.get_data().values():
            if val_ges["category"] != "Total":
                continue
            
            data = val_ges["data"]
            
            name = common.get_column(data, "name")
            if name is None:
                continue
            
            intensity = common.get_column(data, "intensity")
            if intensity is None:
                continue
            
            year = val_ges["year"]
            
            # Add intensity the correct list
            for i in range(len(intensity)):
                name_val = name[i][0]
                intensity_val = sum(intensity[i])
                
                self.__data_tot[name_val]["data"][self.__years_ind[year]["index"]] += intensity_val
            

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update(self) -> None:
        """ Update the structure when the model are updated
        """
        self.__years_ind = {}
        self.__name_ind = {}
        self.__data_tot = {}
        self.__configure_data()
        self.__draw()