import GESAnalysis.UI.plot.missions.common as common
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.FC.SortedData import SortedData


class EmissionMode(QtWidgets.QWidget, Observer):
    """ Class to represent graphically
        the emission for each mission according to the mode of transport
        and the position of people
    """
    __width = 0.5
    
    def __init__(self, model, parent: QtWidgets.QWidget | None = ...) -> None:
        """_summary_

        Args:
            model (GESAnalysis): model
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        super(EmissionMode, self).__init__(parent)
        
        self.__gesanalysis = model
        
        self.__gesanalysis.add_observer(self)
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_emission = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        self.__max_mission = 0
        
        self.__sort = SortedData()
        
        # Add values from the model to the structures define above
        self.__unit = common.check_value(self.__gesanalysis, "emission")
        self.__configure_data()
        
        # Create figure
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Initialisation UI
        self.__init_UI()
        
        # Draw canvas
        self.__draw()


#######################################################################################################
#  Initialisation of the interface                                                                    #
#######################################################################################################
    def __init_UI(self):
        """Initialize the UI
        """
        # Widgets for canvs
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)


        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.addWidget(widget_canvas)


#######################################################################################################
#  Draw the graph in the canvas                                                                       #
#######################################################################################################    
    def __draw(self):
        self.__axes.cla()
        
        self.__axes.set_xlim(1, self.__max_mission)
        
        self.__draw_bars()
        
        self.__figCanvas.draw()
        pass
    
    
    def __draw_bars(self):
        for year in self.__years_ind.keys():
            emission_mode = self.__get_x(year)
            
            for mode in emission_mode:
                self.__axes.bar(emission_mode[mode]["mission"], emission_mode[mode]["value"], width=self.__width, label=mode)
        
        self.__axes.legend()
    
    def __get_x(self, year):
        # Create structure
        x_label_value = {}
        for mode in self.__mode_ind.keys():
            x_label_value[mode] = {"mission" : [], "value": []}
        
        data_year = self.__data_emission[year]
        for val in data_year:
            mission, value, mode, pos = val
            x_label_value[mode]["mission"].append(mission + 1)
            x_label_value[mode]["value"].append(value)
        return x_label_value
        

#######################################################################################################
#  Configure data to plot in the graph                                                                #
#######################################################################################################  
    def __configure_data(self):
        ind_mode = 0
        ind_year = 0
        ind_position = 0
        for val_ges in self.__gesanalysis.get_data().values():
            if val_ges["category"] != "Missions":
                continue
            
            data = val_ges["data"]
            
            mode = common.get_column(data, "mode")
            if mode is None:
                continue
            
            position = common.get_column(data, "position")
            if position is None:
                continue
                
            year = val_ges["year"]
            if year not in self.__years_ind.keys():
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
                
            for i in range(len(mode)):
                if mode[i][0] not in self.__mode_ind.keys():
                    self.__mode_ind[mode[i][0]] = {"index": ind_mode}
                    ind_mode += 1
                if position[i][0] not in self.__position_ind.keys():
                    self.__position_ind[position[i][0]] = {"index": ind_position}
                    ind_position += 1
        self.__sorted_data()
                    
                    
    def __sorted_data(self) -> None:
        """ Sort the data and add into the structure
        """
        for val_ges in self.__gesanalysis.get_data().values():
            year = val_ges["year"]
            data_val_ges = val_ges["data"]
            
            self.__data_emission[year] = []
            
            column_values = common.get_name_column(data_val_ges, "emission")
            column_mode = common.get_name_column(data_val_ges, "mode")
            column_position = common.get_name_column(data_val_ges, "position")
            sort_data_list = self.__sort.sorted_by_column(data_val_ges, "emission", reversed=True)

            # Add values into the structure (index, value emission, mode, position)
            for i in range(len(sort_data_list)):
                ind = sort_data_list.index(i)
                value = sum(data_val_ges[column_values]["data"][ind])
                mode = data_val_ges[column_mode]["data"][ind][0]
                position = data_val_ges[column_position]["data"][ind][0]
                self.__data_emission[year].append((i, value, mode, position))
            
            if len(self.__data_emission[year]) > self.__max_mission:
                self.__max_mission = len(self.__data_emission[year])
                

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################    
    def update(self):
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_emission = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        self.__max_mission = 0
        
        self.__unit = common.check_value(self.__gesanalysis, "emission")
        self.__configure_data()
        
        self.__draw()