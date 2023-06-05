import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Optional, List, Tuple, Dict, Union
from functools import partial


class DistanceMode(QtWidgets.QWidget):
    """ Class for graphically representing
        the distance for each year according to the mode of transport
    """
    
    def __init__(
        self, 
        readerData_year_list: Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]],
        parent: Optional[QtWidgets.QWidget]
    ) -> None:
        """ Initialisation of class where we configure data to plot later

        Args:
            readerData_year_list (Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]): 
            List of dictionary associated to a year
        """
        super(DistanceMode, self).__init__(parent)
        
        
        self.__mode_ind = {} # Dictionary where the key is the mode of transport and the value his index
        self.__years_check = {} # Dictionary to display years in the canvas
        self.__years_dist = {} # Dictionary where the key is a year and the value a list with distance for all mode
        self.__check_unit(readerData_year_list)
        self.__configure_data(readerData_year_list)

        # Create figure
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Initialisation UI
        self.__init_UI()
        
        self.__draw()
        
        
    def __init_UI(self):
        """ Initialise the UI
        """
        # Widget for canvas
        widget_canvas = QtWidgets.QWidget(self)
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout()
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)
        widget_canvas.setLayout(layout_canvas)
        
        # Widget for buttons for years
        widget_checkbutton_years = QtWidgets.QWidget(self)
        layout_checkbutton_years = QtWidgets.QHBoxLayout()
        for year in self.__years_check.keys():
            self.__years_check[year]["button"] = QtWidgets.QCheckBox(year)
            self.__years_check[year]["button"].setChecked(self.__years_check[year]["checked"])
            self.__years_check[year]["button"].toggled.connect(partial(self.__click_year, year))
            layout_checkbutton_years.addWidget(self.__years_check[year]["button"])
        widget_checkbutton_years.setLayout(layout_checkbutton_years)
        layout_checkbutton_years.setAlignment(QtCore.Qt.AlignCenter)
        # Principal widget
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget_canvas)
        layout.addWidget(widget_checkbutton_years)
        self.setLayout(layout)
        

    def __configure_data(
        self,
        readerdata_year: Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]
    ) -> None:
        """ Configure the data into the correct format for plot

        Args:
            readerData_year_list (Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]): 
            List of dictionary associated to a year
        
        Raises:
            TypeError: List is null
        """
        if readerdata_year is None:
            raise TypeError("cannot plot (distance depending mode) because the list is null")
        
        ind_mode = 0
        for reader, year in readerdata_year:
            if reader is None:
                continue
            
            # Récupères les données du reader pour le mode et la distance
            mode = self.__get_column(reader, "mode")
            if mode is None:
                continue
            
            distance = self.__get_column(reader, "distance")
            if distance is None:
                continue
            
            if year not in self.__years_check:
                self.__years_check[year] = {}
                self.__years_check[year]["checked"] = True
            
            # On regarde le nombre de mode qu'il y a en associant un index
            for i in range(len(mode)):
                if mode[i] not in self.__mode_ind.keys():
                    self.__mode_ind[mode[i]] = ind_mode
                    ind_mode += 1
                    
            # On construit une liste avec où la valeur est la distance
            # du mode où l'index est associé dans le dictionnaire
            self.__years_dist[year] = [0 for i in range(len(list(self.__mode_ind.keys())))]
            
            # On calcule la distance pour chaque mode
            for i in range(len(distance)):
                   self.__years_dist[year][self.__mode_ind[mode[i]]] += distance[i]

    
    def __draw(self):
        """ Draw the data in the canvas
        """
        self.__axes.cla() # clear the canvas
        
        # Values use to print the name of labels
        width = 0.3
        espacement = 0.8
        
        # Calculate the necessary space between the bars
        x = np.zeros(len(self.__mode_ind.keys()))
        for i in range(1, len(self.__mode_ind.keys())):
            x[i] = x[i-1] + len(self.__years_dist.keys())*width + espacement
        multiplier = 0
        
        for year, dist_mode in self.__years_dist.items():
            if not self.__years_check[year]["checked"]:
                continue
            offset = width * multiplier
            self.__axes.bar(x+offset, dist_mode, width=width, label=year)
            multiplier += 1
                
        self.__axes.set_ylabel("Distance ({0})".format(self.__unit))
        # Calulate the space of label which he is in the middle of the bars
        if len(self.__years_dist) % 2 == 0:
            offset_xlabel = ((len(self.__years_dist)//2) - 1)*width
            self.__axes.set_xticks(x+offset_xlabel + width/2, list(self.__mode_ind.keys()))
        else:
            offset_xlabel = len(self.__years_dist)//2*width
            self.__axes.set_xticks(x+offset_xlabel, list(self.__mode_ind.keys()))
        
        self.__axes.legend()
        self.__figCanvas.draw()


    def __check_unit(
        self,
        readerData_year: List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]
    ) -> None:
        """ Check the unit of distance for each year is the same
        
        Args:
            readerData_year: List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]:
            List of dictionary associated to a year

        Raises:
            ValueError: A year has a different unit of distance
        """
        self.__unit = ""
        for reader, year in readerData_year:
            unit_reader = self.__get_unit(reader, "distance")
            
            if self.__unit == "":
                self.__unit = "/".join(unit_reader)
                
            unit_reader = "/".join(unit_reader)
                
            if unit_reader != self.__unit:
                raise ValueError(f"unit of distance for year {year} is '{unit_reader} instead of '{self.__unit}'")
    
    
    # Mouse Event for checkbox for years
    def __click_year(self, year, state):
        self.__years_check[year]["checked"] = state
        self.__draw()
    
    
            
    def __get_column(
        self,
        reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
        column: str
    ) -> Optional[List[Union[str, int, float, bool]]]:
        """ Returns the data associated to the column 'column' in the dictionary 'reader'
        
        Args:
            reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]) : the dictionary
            column (str): the column

        Returns:
            List[Union[str, int, float, bool]] | None: The data associated to the column if the column exist, else None
        """
        name_col = list(reader.keys())
        for c in name_col:
            if column == " ".join(reader[c]["name"]):
                return reader[c]["data"]
        return None
    
    
    def __get_unit(
        self,
        reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
        column: str
    ) -> Optional[List[str]]:
        """ Return the unit associated to the column 'column' in the dictionary 'reader'

        Args:
            reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionnaire de données
            column (str): Nom de colonne
            
        Returns:
            List[str] | None: List of strings if the column was found, else None
        """
        name_col = list(reader.keys())
        for c in name_col:
            if column == " ".join(reader[c]["name"]):
                return reader[c]["unit"]
        return None
