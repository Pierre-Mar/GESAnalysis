import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
import numpy as np

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Optional, List, Tuple, Dict, Union
from functools import partial
from GESAnalysis.FC.PATTERNS.Observer import Observer


# class DistanceMode(QtWidgets.QWidget, Observer):
#     """ Class for graphically representing
#         the distance for each year according to the mode of transport
#     """
    
#     def __init__(
#         self,
#         model,
#         controller,
#         parent: Optional[QtWidgets.QWidget]
#     ) -> None:
#         """ Initialisation of class where we configure data to plot later

#         Args:
#             readerData_year_list (Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]): 
#             List of dictionary associated to a year
#         """
#         super(DistanceMode, self).__init__(parent)
        
#         self.__gesanalysis = model
#         self.__controller = controller
        
#         # Add this observer into the list for observable
#         self.__gesanalysis.add_observer(self)
        
        
#         self.__mode_ind = {} # Dictionary where the key is the mode of transport and the value his index
#         self.__years_dist = {} # Dictionary where the key is a year and the value a list with distance for all mode
        
#         self.__check_unit()
#         self.__configure_data()

#         # Create figure
#         self.__fig = Figure()
#         self.__axes = self.__fig.add_subplot(111)
#         self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
#         # Initialisation UI
#         self.__init_UI()
        
#         # Draw canvas
#         self.__draw()
        
        
#     def __init_UI(self):
#         """ Initialise the UI
#         """        
#         # Widget for canvas
#         widget_canvas = QtWidgets.QWidget(self)
        
#         # Add toolbar to control the graph
#         toolbar = NavigationToolbar2QT(self.__figCanvas, self)
#         layout_canvas = QtWidgets.QVBoxLayout()
#         layout_canvas.addWidget(toolbar)
#         layout_canvas.addWidget(self.__figCanvas)
#         widget_canvas.setLayout(layout_canvas)
        
#         # Widget for buttons for years
#         self.__widget_checkbutton_years = QtWidgets.QWidget(self)
#         self.__widget_checkbutton_years.setFixedHeight(40)
#         self.__layout_checkbutton_years = QtWidgets.QHBoxLayout()
        
#         # Create a button for each year
#         for year in self.__years_dist.keys():
#             self.__years_dist[year]["button"] = QtWidgets.QCheckBox(year)
#             self.__years_dist[year]["button"].setChecked(self.__years_dist[year]["checked"])
#             self.__years_dist[year]["button"].toggled.connect(partial(self.__click_year, year))
#             self.__layout_checkbutton_years.addWidget(self.__years_dist[year]["button"])
#         self.__widget_checkbutton_years.setLayout(self.__layout_checkbutton_years)
#         self.__layout_checkbutton_years.setAlignment(QtCore.Qt.AlignCenter)
        
#         # Widget for choose bars or curve
#         widget_bar_curve = QtWidgets.QWidget(self)
#         widget_bar_curve.setFixedHeight(40)
#         layout_bar_curve = QtWidgets.QHBoxLayout() # Horizontal layout
        
#         # Create a radio button to choose "Bars"
#         self.__bar_button = QtWidgets.QRadioButton("Barre")
#         self.__bar_button.setChecked(True)
#         self.__bar_button.toggled.connect(self.__choose_bar_curve)
#         layout_bar_curve.addWidget(self.__bar_button)
        
#         # Create a radio button to choose "Curve"
#         self.__curve_button = QtWidgets.QRadioButton("Courbe")
#         self.__curve_button.toggled.connect(self.__choose_bar_curve)
#         layout_bar_curve.addWidget(self.__curve_button)
#         layout_bar_curve.setAlignment(QtCore.Qt.AlignCenter)
        
#         widget_bar_curve.setLayout(layout_bar_curve)
        
#         self.__displayBar = True
        
#         # Principal widget
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(widget_canvas)
#         layout.addWidget(self.__widget_checkbutton_years)
#         layout.addWidget(widget_bar_curve)
#         self.setLayout(layout)
        
        
#     def __draw(self):
#         """ Draw the data in the canvas
#         """
#         self.__axes.cla() # clear the canvas
        
#         # Values use to print the name of labels
#         width = 0.3                                # Width of bars
#         espacement = 0.8                           # Espacement between bars of each mode
#         number_mode = len(self.__mode_ind.keys())  # Number of mode of transport
#         active_year = 0
#         for year in self.__years_dist.keys():
#             if self.__years_dist[year]["checked"]:
#                 active_year += 1
        
#         # Calculate the necessary space between the bars
#         x = np.zeros(number_mode)
#         for i in range(1, number_mode):
#             x[i] = x[i-1] + active_year*width + espacement
#         multiplier = 0
        
#         # Display bars un canvas
#         for year, dist_mode in self.__years_dist.items():
#             if not self.__years_dist[year]["checked"]:
#                 continue
            
#             if self.__displayBar:
#                 offset = width * multiplier
#                 self.__axes.bar(x+offset, dist_mode["distance"], width=width, label=year)
#                 multiplier += 1
#             else:
#                 self.__axes.plot(x, dist_mode["distance"], "-o", label=year)
                
#         self.__axes.set_ylabel("Distance ({0})".format(self.__unit))
#         # Calulate the space of label which he is in the middle of the bars
#         if self.__displayBar:
#             if active_year % 2 == 0:
#                 offset_xlabel = ((active_year//2) - 1)*width
#                 self.__axes.set_xticks(x+offset_xlabel + width/2, list(self.__mode_ind.keys()))
#             else:
#                 offset_xlabel = active_year//2*width
#                 self.__axes.set_xticks(x+offset_xlabel, list(self.__mode_ind.keys()))
#         else:
#             self.__axes.set_xticks(x, list(self.__mode_ind.keys()))
#         # Display legend in case there are some year active
#         if active_year > 0:
#             self.__axes.legend()
#         self.__figCanvas.draw()
        

#     def __configure_data(self) -> None:
#         """ Configure the data into the correct format for plot
        
#         Raises:
#             TypeError: List is null
#         """
#         if self.__gesanalysis is None:
#             raise TypeError("cannot plot (distance depending mode) because the dictionary is null")
        
#         ind_mode = 0
#         for val_ges in self.__gesanalysis.get_data().values():
#             reader = val_ges["data"]
#             year = val_ges["year"]
            
#             if reader is None:
#                 continue
            
#             # Get the values from the reader for the mode and the distance
#             mode = self.__get_column(reader, "mode")
#             if mode is None:
#                 continue
            
#             distance = self.__get_column(reader, "distance")
#             if distance is None:
#                 continue
            
#             # Associate an index to a mode of transport
#             for i in range(len(mode)):
#                 if mode[i] not in self.__mode_ind.keys():
#                     self.__mode_ind[mode[i]] = ind_mode
#                     ind_mode += 1
            
#             # Construct a dictionary for the values and the button for a year    
#             if year in self.__years_dist.keys():
#                 raise ValueError(f"already data for year '{year}'")
            
#             self.__years_dist[year] = {}
#             self.__years_dist[year]["checked"] = True
#             self.__years_dist[year]["distance"] = [0 for i in range(len(list(self.__mode_ind.keys())))]
            
#             # Calculate the distance for each mode
#             for i in range(len(distance)):
#                    self.__years_dist[year]["distance"][self.__mode_ind[mode[i]]] += distance[i]


#     def __check_unit(
#         self,
#     ) -> None:
#         """ Check the unit of distance for each year is the same
        
#         Args:
#             readerData_year: List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]:
#             List of dictionary associated to a year

#         Raises:
#             ValueError: A year has a different unit of distance
#         """
#         self.__unit = ""
#         for values_ges in self.__gesanalysis.get_data().values():
#             reader = values_ges["data"]
#             year = values_ges["year"]
            
#             unit_reader = self.__get_unit(reader, "distance")
            
#             if self.__unit == "":
#                 self.__unit = "/".join(unit_reader)
                
#             unit_reader = "/".join(unit_reader)
                
#             if unit_reader != self.__unit:
#                 raise ValueError(f"unit of distance for year {year} is '{unit_reader} instead of '{self.__unit}'")
    
    
#     # Mouse Event for checkbox for years
#     def __click_year(self, year: QtWidgets.QCheckBox, state: bool) -> None:
#         """ Change state of the button 'year' and the graph when an user clicked on it

#         Args:
#             year (QtWidgets.QCheckBox): A button
#             state (bool): The button is checked or not
#         """
#         self.__years_dist[year]["checked"] = state
#         self.__draw()
    
#     def __choose_bar_curve(self) -> None:
#         """ Change the graph is the user want curve or bars
#         """
#         self.__displayBar = self.__bar_button.isChecked()
#         self.__draw()
    
            
#     def __get_column(
#         self,
#         reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
#         column: str
#     ) -> Optional[List[Union[str, int, float, bool]]]:
#         """ Returns the data associated to the column 'column' in the dictionary 'reader'
        
#         Args:
#             reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]) : the dictionary
#             column (str): the column

#         Returns:
#             List[Union[str, int, float, bool]] | None: The data associated to the column if the column exist, else None
#         """
#         name_col = list(reader.keys())
#         for c in name_col:
#             if column == " ".join(reader[c]["name"]):
#                 return reader[c]["data"]
#         return None
    
    
#     def __get_unit(
#         self,
#         reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
#         column: str
#     ) -> Optional[List[str]]:
#         """ Return the unit associated to the column 'column' in the dictionary 'reader'

#         Args:
#             reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionnaire de données
#             column (str): Nom de colonne
            
#         Returns:
#             List[str] | None: List of strings if the column was found, else None
#         """
#         name_col = list(reader.keys())
#         for c in name_col:
#             if column == " ".join(reader[c]["name"]):
#                 return reader[c]["unit"]
#         return None
    
    
#     def update(self):
#         # Remove the button years from the widget
#         for year in self.__years_dist.keys():
#             self.__layout_checkbutton_years.removeWidget(self.__years_dist[year]["button"])
        
#         # Reset data
#         self.__mode_ind = {}
#         self.__years_dist = {}
        
#         self.__check_unit()
#         self.__configure_data()
        
#         # Repaint the UI
#         # Only need to change the button for years
#         for year in self.__years_dist.keys():
#             self.__years_dist[year]["button"] = QtWidgets.QCheckBox(year)
#             self.__years_dist[year]["button"].setChecked(self.__years_dist[year]["checked"])
#             self.__years_dist[year]["button"].toggled.connect(partial(self.__click_year, year))
#             self.__layout_checkbutton_years.addWidget(self.__years_dist[year]["button"])
                
#         # Draw the graph
#         self.__draw()



class DistanceMode():
    """ Class for graphically representing
        the distance for each year according to the mode of transport
    """
    
    def __init__(
        self,
        model,
    ) -> None:
        """ Initialisation of class where we configure data to plot later

        Args:
            readerData_year_list (Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]): 
            List of dictionary associated to a year
        """
        
        self.__gesanalysis = model        
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__years_ind = {}    # Same with year
        self.__position_ind = {} # Same with position
        self.__data_dist = {}   # Dictionary to calculate the distance for each mode, year and position
        
        self.__check_value()
        self.__configure_data()

        # Create figure
        self.__fig = plt.figure()
        self.__axes = self.__fig.add_subplot(111)
        
        
        # Draw canvas
        self.draw()
        
        
    def draw(self):
        """ Draw the data in the canvas
        """
        # self.__axes.cla() # clear the canvas

        # Values use to print the name of labels
        self.__width = 0.3                                # Width of bars
        self.__espacement = 0.8                           # Espacement between bars of each mode

        # Construct list for labels
        label_bars = [0 for i in self.__position_ind.keys()]
        for position, ind_position in self.__position_ind.items():
            label_bars[ind_position] = position
        
        print(label_bars)
        
        # Get all the data to draw the bars for each mode
        x_values = self.get_x_val()
        sum_y = [0 for i in x_values]                     # Useful for stacked bars
        for position in label_bars:
            # Get y values for a position and plot the bar
            y_values, y_labels = self.get_y_val_label_position(position)
            if len(x_values) != len(y_values):
                raise ValueError(f"has {len(y_values)} for y instead of {len(x_values)} for position '{position}'")
            self.__axes.bar(x_values, y_values, width=self.__width, bottom=sum_y)
            
            # Update sum_y for next position (and bar)
            sum_y = [(lambda x,y: x+y)(sum_y[i], y_values[i]) for i in range(len(sum_y))]
            
            
        # Configure the legend
        self.__axes.legend(label_bars)
        self.__fig.canvas.draw()
        plt.show()
            
    def get_x_val(self):
        current_space = 0
        x = []
        for mode in self.__mode_ind.keys():
            for i in range(len(self.__data_dist[mode]["year"])):
                x.append(current_space)
                if i != len(self.__data_dist[mode]["year"]):
                    current_space += self.__width
            current_space += self.__espacement
        return x


    def get_y_val_label_position(self, position):
        y = []
        labels = []
        for mode in self.__mode_ind.keys():
            for year in self.__data_dist[mode]["year"]:
                y.append(self.__data_dist[mode]["data"][position][year])
                labels.append(year)

        return y, labels

    def __configure_data(self) -> None:
        """ Configure the data into the correct format for plot
        
        Raises:
            TypeError: List is null
        """
        if self.__gesanalysis is None:
            raise TypeError("cannot plot (distance depending mode) because the dictionary is null")
        
        ind_mode = 0
        ind_year = 0
        ind_position = 0
        # Get the mode, the year and the position and associate an index
        for val_ges in self.__gesanalysis.get_data().values():
            data = val_ges["data"]
            
            mode = self.__get_column(data, "mode")
            if mode is None:
                continue
            
            position = self.__get_column(data, "position")
            if position is None:
                continue
            
            year = val_ges["year"]
            if year not in self.__years_ind.keys():
                self.__years_ind[year] = ind_year
                ind_year += 1
            
            for i in range(len(mode)):
                if mode[i][0] not in self.__mode_ind.keys():
                    self.__mode_ind[mode[i][0]] = ind_mode
                    ind_mode += 1
                if position[i][0] not in self.__position_ind.keys():
                    self.__position_ind[position[i][0]] = ind_position
                    ind_position += 1
        
        # Create list to calculate the distance
        for mode in self.__mode_ind.keys():
            self.__data_dist[mode] = {}
            self.__data_dist[mode]["data"] = {}
            self.__data_dist[mode]["year"] = []
            self.__data_dist[mode]["sum"] = {}
            for position in self.__position_ind.keys():
                self.__data_dist[mode]["data"][position] = {}
                for year in self.__years_ind.keys():
                    self.__data_dist[mode]["data"][position][year] = 0
                    
        # Now calculate the distance
        for val_ges in self.__gesanalysis.get_data().values():
            data = val_ges["data"]
                 
            mode = self.__get_column(data, "mode")
            position = self.__get_column(data, "position")
            year = val_ges["year"]
            distance = self.__get_column(data, "distance")
            if distance is None:
                continue
            
            for i in range(len(distance)):
                # Get the index for postion and year
                mode_val = mode[i][0]
                pos_ind = position[i][0]
                year_ind = year
                
                # Add the distance
                self.__data_dist[mode_val]["data"][pos_ind][year_ind] += sum(distance[i])

        # Find the year for each mode who are different from 0 (useful to plot)
        for mode in self.__mode_ind.keys():
            for year in self.__years_ind.keys():
                s = 0
                for position in self.__position_ind.keys():
                    s += self.__data_dist[mode]["data"][position][year]
                self.__data_dist[mode]["sum"][year] = s
                if s > 0 :
                    self.__data_dist[mode]["year"].append(year)


    def __check_value(
        self,
    ) -> None:
        """ Check the unit of distance for each year is the same

        Raises:
            ValueError: A year has a different unit of distance or the values are not integers or float
        """
        self.__unit = ""
        for values_ges in self.__gesanalysis.get_data().values():
            reader = values_ges["data"]
            year = values_ges["year"]          
            unit_reader = self.__get_unit(reader, "distance")
            type_reader = self.__get_type(reader, "distance")
            
            if self.__unit == "":
                self.__unit = "/".join(unit_reader)
                
            unit_reader = "/".join(unit_reader)
                
            if unit_reader != self.__unit:
                raise ValueError(f"unit of distance for year {year} is '{unit_reader} instead of '{self.__unit}'")
            if type_reader not in [int, float]:
                raise ValueError(f"type of distance for year {year} is '{type_reader} instead of int or float")
    
    
            
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
    
    def __get_type(
        self,
        reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
        column: str
    ) -> Optional[Union[str, bool, int, float]]:
        """ Returns the type associated to the column 'column' in the dictionary 'reader'
        
        Args:
            reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]) : the dictionary
            column (str): the column

        Returns:
            Union[str, int, float, bool] | None: The type associated to the column if the column exist, else None
        """
        name_col = list(reader.keys())
        for c in name_col:
            if column == " ".join(reader[c]["name"]):
                return reader[c]["type"]
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
