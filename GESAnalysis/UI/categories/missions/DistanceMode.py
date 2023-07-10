import matplotlib

matplotlib.use('Qt5Agg')

import GESAnalysis.UI.categories.common as common

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Any, Optional, List, Tuple, Dict, Union
from functools import partial
from random import choice


class DistanceMode(QtWidgets.QWidget):
    """ Class to represent graphically
        the distance for each year according to the mode of transport
        and the position of people
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    __spacing = 0.8                                 # Spacing between bars of each mode
    __ratio_text = 1000/723405                      # Ratio to place the text above the bars
    __default_size_text = 10                        # Size of text above bars
    __markers = ['.', ',', 'o', 'v', '^', '<', '>'] # Markers use to plot the curves

    
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget]
    ) -> None:
        """ Initialisation of class where we configure data to plot it

        Args:
            model (GESAnalysis): model
            parent (Optional[QtWidgets.QWidget]): Parent of this widget
        """
        super(DistanceMode, self).__init__(parent)
        
        self.__mode_dict = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_dict = {} # Same with position
        self.__years_dict = {}    # Same with year
        self.__data_dict = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        self.__unit = ""
        
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
        """ Initialize the UI
        """        
        # Widget for canvas
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout()
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)
        widget_canvas.setLayout(layout_canvas)
        
        # Widget for buttons for years, modes, positions
        self.__widget_checkbuttons_years, self.__layout_checkbuttons_years = self.__create_list_buttons(self.__years_dict, self.__click_year)
        self.__widget_checkbuttons_modes, self.__layout_checkbuttons_modes = self.__create_list_buttons(self.__mode_dict, self.__click_mode)
        self.__widget_checkbuttons_positions, self.__layout_checkbuttons_positions = self.__create_list_buttons(self.__position_dict, self.__click_position)

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
        layout.addWidget(self.__widget_checkbuttons_years)
        layout.addWidget(self.__widget_checkbuttons_modes)
        layout.addWidget(self.__widget_checkbuttons_positions)
        layout.addWidget(widget_bar_curve)
        self.setLayout(layout)
        
        
    def __create_list_buttons(self, data_dict, fct) -> Tuple[QtWidgets.QWidget, QtWidgets.QHBoxLayout]:
        """ Create a list of buttons (used for modes, years and positions)

        Args:
            data_dict (dict): dictionary with data (mode, year, position)
            fct : fun,ction associated when the user click on the button

        Returns:
            QWidget, QHBoxLayout: Widget and layout associated to the list of buttons
        """
        widget = QtWidgets.QWidget(self)
        widget.setFixedHeight(40)
        layout = QtWidgets.QHBoxLayout(widget)
        for d in data_dict.keys():
            data_dict[d]["button"] = QtWidgets.QCheckBox(d)
            data_dict[d]["checked"] = True
            data_dict[d]["button"].setChecked(data_dict[d]["checked"])
            data_dict[d]["button"].toggled.connect(partial(fct, d))
            layout.addWidget(data_dict[d]["button"])
        layout.setAlignment(QtCore.Qt.AlignCenter)
        return widget, layout
    
    
    def __remove_list_buttons(self, data_dict, layout: QtWidgets.QHBoxLayout) -> None:
        """ Remove the buttons from the layout

        Args:
            data_dict (dict): dictionary with data (mode, year, position)
            layout (QHBoxLayout): layout of button
        """
        for d in data_dict.keys():
            layout.removeWidget(data_dict[d]["button"])
            del data_dict[d]["checked"]
            del data_dict[d]["button"]
    
    
    def __update_list_buttons(self, data_dict, layout: QtWidgets.QHBoxLayout, fct: Any) -> None:
        """ Update a layout of a list of buttons (used for modes, years and positions)

        Args:
            data_dict (dict): dictionary with data (mode, year, position)
            layout (QHBoxLayout): Layout to put the buttons
            fct (Any): fun,ction associated when the user click on the button
        """
        for d in data_dict.keys():
            data_dict[d]["button"] = QtWidgets.QCheckBox(d)
            data_dict[d]["checked"] = True
            data_dict[d]["button"].setChecked(data_dict[d]["checked"])
            data_dict[d]["button"].toggled.connect(partial(fct, d))
            layout.addWidget(data_dict[d]["button"])

   
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
        self.__axes.set_ylabel(f"Distance ({self.__unit})")
        self.__figCanvas.draw()
        
    
    def __draw_bars(self):
        """ Draw a graph with bars

        Raises:
            ValueError: When the number of values for y-axis is different from
            the number of values for x-axis. Same with labels
        """     
        # Get all the data to draw the bars for each mode
        x_bars, bars_labels, x_labels, labels = self.__get_x_val_label()
        y_labels = [year for year, mode in bars_labels]     # Contains the label for each bars
        sum_y = [0 for i in x_bars]                         # Useful for stacked bars
        position_draw = []                                  # Contains the position draw in the graph
        for position in self.__position_dict.keys():
            if not self.__position_dict[position]["checked"]:
                continue
            
            y_values, y_labels_pos = self.__get_y_val_label_position(position, bars_labels)
            
            if sum(y_values) == 0:
                continue
            
            # Raise error when the number of values on y-axis is different with the number of bars
            if len(y_labels_pos) != len(y_labels):
                raise ValueError(f"has {len(y_values)} for y instead of {len(x_bars)} for position '{position}'")
            for label_ind in range(len(y_labels_pos)):
                if y_labels[label_ind] != y_labels_pos[label_ind]:
                    raise ValueError(f"has different labels for bars for position '{position}'")
            
            # Draw bars
            self.__axes.bar(x_bars, y_values, width=self.__width, bottom=sum_y, linewidth=0.5, edgecolor='black')
            
            # Update values for next bars
            sum_y = [(lambda x,y: x+y)(sum_y[i], y_values[i]) for i in range(len(sum_y))]
            position_draw.append(position)
        
        # Add text to precise which year corresponding to the bar
        self.__set_text_bars(x_bars, sum_y, y_labels)

        # Add labels on x-axis
        self.__axes.set_xticks(x_labels, labels)
        
        # Display legend if there some mode
        if len(position_draw):
            self.__axes.legend(position_draw)
            
    
    def __set_text_bars(self, bars_pos: List[Union[int, float]], len_bars: List[Union[int, float]], y_labels: List[str]) -> None:
        """ Set text above each bars

        Args:
            bars_pos (List[Union[int, float]]): Position of labels on x-axis
            len_bars (List[Union[int, float]]): size of each bar
            y_labels (List[str]): Labels
        """
        if not len(len_bars):
            return
        size_text = self.__default_size_text -  1.15*len(self.__years_dict.keys())
        max_bars = max(len_bars)
        for i, label in enumerate(y_labels):
            self.__axes.text(bars_pos[i], len_bars[i]+ self.__ratio_text*max_bars, label, ha='center', color='black', fontsize=size_text)
        
    
    def __get_x_val_label(self) -> Tuple[List[Union[int, float]], List[Union[int, float]], List[str]]:
        """ Create a tuple of 3 lists where
             - 1st : values where the first bar of a mode is on x-axis.
             - 2nd : values where the label is on x-axis
             - 3rd : labels
            Another list but for labels and a list with labels

        Returns:
            Tuple[List[Union[int, float]], List[Union[int, float]], List[str]]: The 3 lists
        """
        current_space = 0
        x_bars = []
        bars_labels = []
        x_labels = []
        labels = []
        current_ind = 0
        for mode, data_mode in self.__data_dict.items():
            if not self.__mode_dict[mode]["checked"]:
                continue
            
            active_year_mode = 0
            for year, sum_year in data_mode["sum"].items():
                if not self.__years_dict[year]["checked"] or sum_year == 0:
                    continue
                
                s = 0
                for position, data_position in data_mode["data"].items():
                    if self.__position_dict[position]["checked"]:
                        s += data_position[year]
                if s == 0:
                    continue
                
                x_bars.append(current_space)
                bars_labels.append((year, mode))
                current_ind += 1
                current_space += self.__width
                active_year_mode += 1
                
            if active_year_mode > 0:
                offset = active_year_mode//2 + (active_year_mode % 2)
                imp = x_bars[current_ind-offset] - self.__width/2
                pai = x_bars[current_ind-offset]
                x_labels.append(pai if active_year_mode % 2 else imp)
                labels.append(mode)
                
                # Next mode : add the space between the last bar of this mode et the first bar of the next mode
                current_space += self.__spacing
        
        return x_bars, bars_labels, x_labels, labels


    def __get_y_val_label_position(self, position: str, year_mode: Tuple[List[str], List[str]]) -> Tuple[List[Union[int, float]], List[str]]:
        """ Construct a list to plot the bars for the position 'position' and a list of year and mode accepted (from buttons).
            The value is the distance of the position when using a mode in different year

        Args:
            position (str): Position
            mode_accepted (List[str]): List of year and mode concerned for the graph

        Returns:
            Tuple[List[Union[int, float]], List[str]]: Values of distance for each bar of position 'position'
        """
        y = []
        labels = []
        for year, mode in year_mode:
            y.append(self.__data_dict[mode]["data"][position][year])
            labels.append(year)
        return y, labels
    
    
    def __draw_curve(self):
        """ Draw a graph with curves
        """
        x_labels = {}
        x = 0
        # Dictionary where a mode is associated to a value (x-axis)
        for mode in self.__mode_dict.keys():
            if not self.__mode_dict[mode]["checked"]:
                continue
            x_labels[mode] = x
            x += self.__spacing

        # Calculate th y value for each year
        has_year = False
        for year in self.__years_dict.keys():
            if not self.__years_dict[year]["checked"]:
                continue
            
            x_year = []
            y_year = []
            for mode in x_labels.keys():
                s = 0
                for position in self.__position_dict.keys():
                    if not self.__position_dict[position]["checked"]:
                        continue
                    
                    s += self.__data_dict[mode]["data"][position][year]
                
                # If there are no value, we don't plot the year
                if s == 0:
                    continue
                
                x_year.append(x_labels[mode])
                y_year.append(s)
                has_year = True
            # Choose randomly a marker
            marker_random = choice(self.__markers)
            self.__axes.scatter(x_year, y_year, marker=marker_random, label=year)
        
        # Set the label on x-axis
        self.__axes.set_xticks(list(x_labels.values()), list(x_labels.keys()))
        
        # display legend
        if has_year:
            self.__axes.legend()

    
#######################################################################################################
#  Mouse event to change the graph                                                                    #
#######################################################################################################
    def __click_year(self, year: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'year' and the graph when an user clicked on it

        Args:
            year (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__years_dict[year]["checked"] = state
        self.__draw()
        
    
    def __click_mode(self, mode: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'mode' and the graph when an user clicked on it

        Args:
            mode (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__mode_dict[mode]["checked"] = state
        self.__draw()
        
    
    def __click_position(self, position: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'position' and the graph when an user clicked on it

        Args:
            position (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__position_dict[position]["checked"] = state
        self.__draw()
    
    
    def __select_bar_graph(self, selected):
        """ Check if the radio button to draw bars is selected or not

        Args:
            selected (bool): the button is selected or not
        """
        if selected:
            self.__is_bars_selected = True
            self.__draw()
    
    
    def __select_curve_graph(self, selected):
        """ Check if the radio button to draw curves is selected or not

        Args:
            selected (bool): the button is selected or not
        """
        if selected:
            self.__is_bars_selected = False
            self.__draw()
    

# #######################################################################################################
# #  Update graph from MissionWidget                                                                    #
# #######################################################################################################
    def update_canvas(self, mode_dict, position_dict, year_dict, data_dict):
        # Remove the button years, modes, positions
        self.__remove_list_buttons(self.__years_dict, self.__layout_checkbuttons_years)
        self.__remove_list_buttons(self.__mode_dict, self.__layout_checkbuttons_modes)
        self.__remove_list_buttons(self.__position_dict, self.__layout_checkbuttons_positions)
        
        # Update the structure
        self.__mode_dict = self.__update_structure(mode_dict)
        self.__position_dict = self.__update_structure(position_dict)
        self.__years_dict = self.__update_structure(year_dict)

        self.__data_dict = self.__rearrange_data_dict(data_dict["data"].copy())
        self.__unit = data_dict["unit_distance"]
        
        # Repaint the UI
        # Only need to change the button for years, modes and positions
        self.__update_list_buttons(self.__years_dict, self.__layout_checkbuttons_years, self.__click_year)
        self.__update_list_buttons(self.__mode_dict, self.__layout_checkbuttons_modes, self.__click_mode)
        self.__update_list_buttons(self.__position_dict, self.__layout_checkbuttons_positions, self.__click_position)

        # Draw the graph
        self.__draw()
        
        
    def __rearrange_data_dict(self, data_dict):
        dictionary = {}
        for mode, data_mode in data_dict.items():
            dictionary[mode] = {
                "data": {},
                "sum": {}
            }
            # Fill "data"
            for position, data_position in data_mode["data"].items():
                dictionary[mode]["data"][position] = {}
                for year, data_year in data_position.items():
                    dictionary[mode]["data"][position][year] = data_year["total_distance"]
            # Fill "sum"
            for year, sum_year in data_mode["sum"].items():
                dictionary[mode]["sum"][year] = sum_year["distance"]
        
        return dictionary
    
    
    def __update_structure(self, data_dict):
        data_class = {}
        for data in data_dict.keys():
            data_class[data] = {}
        return data_class
