import matplotlib

matplotlib.use('Qt5Agg')

import GESAnalysis.UI.categories.common as common

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Optional, List, Tuple, Dict, Union
from functools import partial
from GESAnalysis.FC.PATTERNS.Observer import Observer
from random import choice


class DistanceMode(QtWidgets.QWidget, Observer):
    """ Class to represent graphically
        the distance for each year according to the mode of transport
        and the position of people
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    __spacing = 0.8                                 # Spacing between bars of each mode
    __default_size_text = 10                        # Size of text above bars
    __markers = ['.', ',', 'o', 'v', '^', '<', '>'] # Markers use to plot the curves

    
    def __init__(
        self,
        model,
        category: str, 
        parent: Optional[QtWidgets.QWidget]
    ) -> None:
        """ Initialisation of class where we configure data to plot it

        Args:
            model (GESAnalysis): model
            parent (Optional[QtWidgets.QWidget]): Parent of this widget
        """
        super(DistanceMode, self).__init__(parent)

        self.__gesanalysis = model
        
        # Add this observer into the list for observable
        self.__gesanalysis.add_observer(self, category)
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_dist = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        
        # Add values from the model to the structures define above
        self.__unit = common.check_value(self.__gesanalysis, "distance")
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
        self.__widget_checkbuttons_years, self.__layout_checkbuttons_years = self.__create_list_buttons(self.__years_ind, self.__click_year)
        self.__widget_checkbuttons_modes, self.__layout_checkbuttons_modes = self.__create_list_buttons(self.__mode_ind, self.__click_mode)
        self.__widget_checkbuttons_positions, self.__layout_checkbuttons_positions = self.__create_list_buttons(self.__position_ind, self.__click_position)

        
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
    
    
    def __update_list_buttons(self, data_dict, layout: QtWidgets.QHBoxLayout, fct) -> None:
        """ Update a layout of a list of buttons (used for modes, years and positions)

        Args:
            data_dict (dict): dictionary with data (mode, year, position)
            layout (QHBoxLayout) : Layout to put the buttons
            fct : fun,ction associated when the user click on the button
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
        x_bars, x_labels, labels = self.__get_x_val_label()
        y_labels = []
        last_position = ""
        sum_y = [0 for i in x_bars]                               # Useful for stacked bars
        position_draw = []
        for position in self.__position_ind.keys():
            if not self.__position_ind[position]["checked"]:
                continue
            
            # Get a list with the values of each bar for the position 'position'
            y_values, y_labels_pos = self.__get_y_val_label_position(position, labels)
            
            # Check the differents values
            # Compare if there are the same number of values between y-axis and x-axis
            if len(x_bars) != len(y_values):
                raise ValueError(f"has {len(y_values)} for y instead of {len(x_bars)} for position '{position}'")
            if position_draw != []:
                # Compare labels
                if len(y_labels) != len(y_labels_pos):
                    raise ValueError(f"has {len(y_labels)} labels instead of {len(y_labels_pos)} for position '{position}'")
                for label_ind in range(len(y_labels_pos)):
                    if y_labels[label_ind] != y_labels_pos[label_ind]:
                        raise ValueError(f"has different labels for bars between position '{position}' and '{last_position}'")
            
            # Draw bar
            self.__axes.bar(x_bars, y_values, width=self.__width, bottom=sum_y, linewidth=0.5, edgecolor='black')
            
            # Update values for next bars
            sum_y = [(lambda x,y: x+y)(sum_y[i], y_values[i]) for i in range(len(sum_y))]
            y_labels = y_labels_pos
            last_position = position
            position_draw.append(position)

        # # Add text to precise which year corresponding to the bar
        size_text = self.__default_size_text -  1.15*len(self.__years_ind.keys())
        for i, label in enumerate(y_labels):
            self.__axes.text(x_bars[i], sum_y[i] + 1000, label, ha = 'center', color = 'black', fontsize=size_text)
            
        # Add correct labels on x-axis
        self.__axes.set_xticks(x_labels, labels)        

        # # Display legend and draw canvas
        if len(position_draw):
            self.__axes.legend(position_draw)
        
    
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
        x_label = []
        label = []
        current_ind = 0
        for mode in self.__mode_ind.keys():
            if not self.__mode_ind[mode]["checked"]:
                continue
            active_year_mode = 0
            for i in range(len(self.__data_dist[mode]["year"])):
                # In case, the user don't want to display bars for year
                year_mode = self.__data_dist[mode]["year"][i]
                if not self.__years_ind[year_mode]["checked"]:
                    continue
                
                # Need to display a bar for mode and year
                x_bars.append(current_space)
                current_ind += 1
                current_space += self.__width
                active_year_mode += 1

            # Calculate the position of the label on x-axis
            if active_year_mode > 0:
                offset = active_year_mode//2 + (active_year_mode % 2)
                imp = x_bars[current_ind-offset] - self.__width/2
                pai = x_bars[current_ind-offset]
                x_label.append(pai if active_year_mode % 2 else imp)
                label.append(mode)

                # Next mode : add the space between the last bar of this mode et the first bar of the next mode
                current_space += self.__spacing
        
        return x_bars, x_label, label


    def __get_y_val_label_position(self, position: str, mode_accepted: List[str]) -> Tuple[List[Union[int, float]], List[str]]:
        """ Construct a list to plot a bar for the position 'position' and a list of mode accepted (from buttons).
            The value is the distance of the position when using a mode in different year

        Args:
            position (str): Position
            mode_accepted (List[str]): List of mode accepted

        Returns:
            Tuple[List[Union[int, float]], List[str]]: Values of distance for each bar of position 'position'
        """
        y = []
        labels = []
        for mode in mode_accepted:
            for year in self.__data_dist[mode]["year"]:
                if not self.__years_ind[year]["checked"]:
                    continue
                y.append(self.__data_dist[mode]["data"][position][year])
                labels.append(year)
        return y, labels
    
    
    def __draw_curve(self):
        """ Draw a graph with curves
        """
        x_labels = {}
        x = 0
        # Dictionary where a mode is associated to a value (x-axis)
        for mode in self.__mode_ind.keys():
            if not self.__mode_ind[mode]["checked"]:
                continue
            x_labels[mode] = x
            x += self.__spacing

        # Calculate th y value for each year
        has_year = False
        for year in self.__years_ind.keys():
            if not self.__years_ind[year]["checked"]:
                continue
            
            x_year = []
            y_year = []
            for mode in x_labels.keys():
                s = 0
                for position in self.__position_ind.keys():
                    if not self.__position_ind[position]["checked"]:
                        continue
                    
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
        """
        ind_mode = 0
        ind_year = 0
        ind_position = 0
        # Get the mode, the year and the position and associate an index
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
            if val_ges["category"] != "Missions":
                continue
            
            data = val_ges["data"]
                 
            mode = common.get_column(data, "mode")
            position = common.get_column(data, "position")
            year = val_ges["year"]
            distance = common.get_column(data, "distance")
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
        
    
    def __click_mode(self, mode: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'mode' and the graph when an user clicked on it

        Args:
            mode (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__mode_ind[mode]["checked"] = state
        self.__draw()
        
    
    def __click_position(self, position: QtWidgets.QCheckBox, state: bool) -> None:
        """ Change state of the button 'position' and the graph when an user clicked on it

        Args:
            position (QtWidgets.QCheckBox): A button
            state (bool): The button is checked or not
        """
        self.__position_ind[position]["checked"] = state
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
    

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update(self):
        """ Update the graph and the data when the FC has a modification
        """
        # Remove the button years, modes, positions
        self.__remove_list_buttons(self.__years_ind, self.__layout_checkbuttons_years)
        self.__remove_list_buttons(self.__mode_ind, self.__layout_checkbuttons_modes)
        self.__remove_list_buttons(self.__position_ind, self.__layout_checkbuttons_positions)

        
        # Reset data
        self.__mode_ind = {}
        self.__years_ind = {}
        self.__position_ind = {}
        self.__data_dist = {}
        
        self.__unit = common.check_value(self.__gesanalysis, "distance")
        self.__configure_data()
        
        # Repaint the UI
        # Only need to change the button for years, modes and positions
        self.__update_list_buttons(self.__years_ind, self.__layout_checkbuttons_years, self.__click_year)
        self.__update_list_buttons(self.__mode_ind, self.__layout_checkbuttons_modes, self.__click_mode)
        self.__update_list_buttons(self.__position_ind, self.__layout_checkbuttons_positions, self.__click_position)
        
        # Draw the graph
        self.__draw()
