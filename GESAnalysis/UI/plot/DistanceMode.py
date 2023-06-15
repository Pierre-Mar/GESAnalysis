import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Optional, List, Tuple, Dict, Union
from functools import partial
from GESAnalysis.FC.PATTERNS.Observer import Observer
from random import choice




class DistanceMode(QtWidgets.QWidget, Observer):
    """ Class for graphically representing
        the distance for each year according to the mode of transport
    """
    
    # Values use to print the name of labels
    __width = 0.3                                # Width of bars
    __espacement = 0.8                           # Espacement between bars of each mode
    __default_size_text = 10                     # Size of text above bars
    __markers = ['.', ',', 'o', 'v', '^', '<', '>']

    
    def __init__(
        self,
        model,
        controller,
        parent: Optional[QtWidgets.QWidget]
    ) -> None:
        """ Initialisation of class where we configure data to plot later

        Args:
            readerData_year_list (Optional[List[Tuple[Optional[Dict[str, Dict[str, List[Union[str, bool, int, float]]]]], str]]]): 
            List of dictionary associated to a year
        """
        super(DistanceMode, self).__init__(parent)

        self.__gesanalysis = model
        self.__controller = controller
        
        # Add this observer into the list for observable
        self.__gesanalysis.add_observer(self)
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_dist = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        
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
        """ Initialise the UI
        """        
        # Widget for canvas
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout()
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)
        widget_canvas.setLayout(layout_canvas)
        
        # Widget for buttons for years
        self.__widget_checkbutton_years = QtWidgets.QWidget(self)
        self.__widget_checkbutton_years.setFixedHeight(40)
        self.__layout_checkbutton_years = QtWidgets.QHBoxLayout()
        
        # Create a button for each year
        for year in self.__years_ind.keys():
            self.__years_ind[year]["button"] = QtWidgets.QCheckBox(year)
            self.__years_ind[year]["checked"] = True
            self.__years_ind[year]["button"].setChecked(self.__years_ind[year]["checked"])
            self.__years_ind[year]["button"].toggled.connect(partial(self.__click_year, year))
            self.__layout_checkbutton_years.addWidget(self.__years_ind[year]["button"])
        self.__widget_checkbutton_years.setLayout(self.__layout_checkbutton_years)
        self.__layout_checkbutton_years.setAlignment(QtCore.Qt.AlignCenter)
        
        # Widget for choose bars or curve
        widget_bar_curve = QtWidgets.QWidget(self)
        widget_bar_curve.setFixedHeight(40)
        layout_bar_curve = QtWidgets.QHBoxLayout() # Horizontal layout
        
        # Create a radio button to choose "Bars"
        self.__bar_button = QtWidgets.QRadioButton("Barre")
        self.__bar_button.setChecked(True)
        self.__bar_button.toggled.connect(self.__select_bar_graph)
        layout_bar_curve.addWidget(self.__bar_button)
        
        # Create a radio button to choose "Curve"
        self.__curve_button = QtWidgets.QRadioButton("Courbe")
        self.__curve_button.toggled.connect(self.__select_curve_graph)
        layout_bar_curve.addWidget(self.__curve_button)
        layout_bar_curve.setAlignment(QtCore.Qt.AlignCenter)
        
        widget_bar_curve.setLayout(layout_bar_curve)
        
        self.__is_bars_selected = True
        
        # Principal widget
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget_canvas)
        layout.addWidget(self.__widget_checkbutton_years)
        layout.addWidget(widget_bar_curve)
        self.setLayout(layout)

   
#######################################################################################################
#  Draw the graph in the canvas                                                                       #
#######################################################################################################  
    def __draw(self):
        """ Draw the data in the canvas
        """
        self.__axes.cla() # clear the canvas
        
        if self.__is_bars_selected:  
            self.__draw_bars()
        else:
            self.__draw_curve()
        
        self.__figCanvas.draw()
        
    
    def __draw_bars(self):
        """ Draw a graph with bars

        Raises:
            ValueError: When the number of values for y-axis is different from
            the number of values for x-axis
        """
        # Construct list for labels
        label_bars = [0 for i in self.__position_ind.keys()]
        for position, ind_position in self.__position_ind.items():
            label_bars[ind_position["index"]] = position
                
        # Get all the data to draw the bars for each mode
        x_values, x_labels, labels = self.get_x_val_label()
        sum_y = [0 for i in x_values]                     # Useful for stacked bars
        y_labels = []
        for position in label_bars:
            # Get y values for a position and plot the bar
            y_values, y_labels = self.get_y_val_label_position(position)
            if len(x_values) != len(y_values):
                raise ValueError(f"has {len(y_values)} for y instead of {len(x_values)} for position '{position}'")
            # Plot the bar
            self.__axes.bar(x_values, y_values, width=self.__width, bottom=sum_y, linewidth=0.5, edgecolor='black')
            
            # Update sum_y for next position (and bar)
            sum_y = [(lambda x,y: x+y)(sum_y[i], y_values[i]) for i in range(len(sum_y))]

        # Add text to precise which year corresponding to the bar
        size_text = self.__default_size_text -  1.15*len(self.__years_ind.keys())
        for i, label in enumerate(y_labels):
            self.__axes.text(x_values[i], sum_y[i] + 1000, label, ha = 'center', color = 'black', fontsize=size_text)
            
        # Add correct labels on x-axis
        self.__axes.set_xticks(x_labels, labels)        

        # Display legend and draw canvas
        if len(label_bars):
            self.__axes.legend(label_bars)
        
    
    def get_x_val_label(self) -> Tuple[List[Union[int, float]], List[Union[int, float]], List[str]]:
        """ Create a list where the values is where the bar is on x-axis.
            Another list but for labels and a list with labels

        Returns:
            Tuple[List[Union[int, float]], List[Union[int, float]], List[str]]: The 3 lists
        """
        current_space = 0
        x = []
        x_label = []
        label = []
        current_ind = 0
        for mode in self.__mode_ind.keys():
            active_year_mode = 0
            for i in range(len(self.__data_dist[mode]["year"])):
                # In case, the user don't want to display bars for year
                year_mode = self.__data_dist[mode]["year"][i]
                if not self.__years_ind[year_mode]["checked"]:
                    continue
                
                # Need to display a bar for mode and year
                x.append(current_space)
                current_ind += 1
                current_space += self.__width
                active_year_mode += 1

            # Calculate the position of the label in x-axis
            if active_year_mode > 0:
                offset = active_year_mode//2 + (active_year_mode % 2)
                imp = x[current_ind-offset] - self.__width/2
                pai = x[current_ind-offset]
                x_label.append(pai if active_year_mode % 2 else imp)
                label.append(mode)

                # Next mode : add the space between the last bar of this mode et the first bar of the next mode
                current_space += self.__espacement
        
        return x, x_label, label


    def get_y_val_label_position(self, position: str) -> Tuple[List[Union[int, float]], List[str]]:
        """ Construct a list to plot a bar for the position 'position'.
            The value is the distance of the position when using a mode in different year

        Args:
            position (str): Position

        Returns:
            Tuple[List[Union[int, float]], List[str]]: Values of distance for each bar of position 'position'
        """
        y = []
        labels = []
        for mode in self.__mode_ind.keys():
            for year in self.__data_dist[mode]["year"]:
                if not self.__years_ind[year]["checked"]:
                    continue
                y.append(self.__data_dist[mode]["data"][position][year])
                labels.append(year)
        return y, labels
    
    
    def __draw_curve(self):
        x_labels = {}
        x = 0
        # Dictionary where a mode is associated to a value (x-axis)
        for mode in self.__mode_ind.keys():
            x_labels[mode] = x
            x += self.__espacement

        # Calculate th y value for each year
        has_year = False
        for year in self.__years_ind.keys():
            if not self.__years_ind[year]["checked"]:
                continue
            
            x_year = []
            y_year = []
            for mode in self.__mode_ind.keys():
                s = 0
                for position in self.__position_ind.keys():
                    s += self.__data_dist[mode]["data"][position][year]
                
                # If there are no value, we don't plot the year
                if s == 0:
                    continue
                
                x_year.append(x_labels[mode])
                y_year.append(s)
            has_year = True
            # Choose randomly a marker
            marker_random = choice(self.__markers)
            self.__axes.scatter(x_year, y_year, marker=marker_random, label=year)
            
        self.__axes.set_xticks(list(x_labels.values()), list(x_labels.keys()))
        if has_year:
            self.__axes.legend()
                

#######################################################################################################
#  Configure data to plot in the graph                                                                #
#######################################################################################################  
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
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
            
            for i in range(len(mode)):
                if mode[i][0] not in self.__mode_ind.keys():
                    self.__mode_ind[mode[i][0]] = {"index": ind_mode}
                    ind_mode += 1
                if position[i][0] not in self.__position_ind.keys():
                    self.__position_ind[position[i][0]] = {"index": ind_position}
                    ind_position += 1
        
        # Create structure to calculate the distance
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
        
        # Find the distance for years for each mode who are equal to 0
        # If it's equal to 0, we don't add it => no bar
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
    

#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################  
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
    
    
#######################################################################################################
#  Mouse event to change the graph                                                                    #
#######################################################################################################
    def __click_year(self, year: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'year' and the graph when an user clicked on it

        Args:
            year (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__years_ind[year]["checked"] = state
        self.__draw()
    
    
    def __select_bar_graph(self, selected):
        if selected:
            self.__is_bars_selected = True
            self.__draw()
    
    
    def __select_curve_graph(self, selected):
        if selected:
            self.__is_bars_selected = False
            self.__draw()
    

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update(self):
        """ Update the graph and the data when the FC has a modification
        """
        # Remove the button years from the widget
        for year in self.__years_ind.keys():
            self.__layout_checkbutton_years.removeWidget(self.__years_ind[year]["button"])
        
        # Reset data
        self.__mode_ind = {}
        self.__years_ind = {}
        self.__position_ind = {}
        self.__data_dist = {}
        
        self.__check_value()
        self.__configure_data()
        
        # Repaint the UI
        # Only need to change the button for years
        for year in self.__years_ind.keys():
            self.__years_ind[year]["button"] = QtWidgets.QCheckBox(year)
            self.__years_ind[year]["checked"] = True
            self.__years_ind[year]["button"].setChecked(self.__years_ind[year]["checked"])
            self.__years_ind[year]["button"].toggled.connect(partial(self.__click_year, year))
            self.__layout_checkbutton_years.addWidget(self.__years_ind[year]["button"])
        
        # Draw the graph
        self.__draw()
