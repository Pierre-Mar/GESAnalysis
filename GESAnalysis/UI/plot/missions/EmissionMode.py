import GESAnalysis.UI.plot.common as common
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.FC.SortedData import SortedData
from functools import partial
from typing import Any, Callable, Dict, List, Tuple, Union


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
        
        self.__gesanalysis.add_observer(self, "Missions")
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_emission = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        self.__is_pourcentage = False
        self.__accumulate = False
        self.__is_bars_selected = True
        
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
    def __init_UI(self) -> None:
        """Initialize the UI
        """
        # Widgets for canvs
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph
        toolbar = NavigationToolbar2QT(self.__figCanvas, self)
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(toolbar)
        layout_canvas.addWidget(self.__figCanvas)
        
        # Create a widget to display a list of buttons to choose the year
        self.__widget_button_years, self.layout_button_years = self.__create_list_buttons(
            self.__years_ind,
            QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
            self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
        )
        
        # Create a widget for a button for pourcentage and accumulate
        widget_pourcentage_accu = QtWidgets.QWidget(self)
        widget_pourcentage_accu.setFixedHeight(40)
        layout_pourcentage_accu = QtWidgets.QHBoxLayout(widget_pourcentage_accu)
        
        # Create a check button to display values as a pourcentage
        self.button_pourcentage = QtWidgets.QCheckBox("Pourcentage")
        self.button_pourcentage.setChecked(self.__is_pourcentage)
        self.button_pourcentage.toggled.connect(self.__click_pourcentage)
        
        # Create a check button to display accumulate values
        self.button_accumulate = QtWidgets.QCheckBox("Cumulées")
        self.button_accumulate.setChecked(self.__accumulate)
        self.button_accumulate.toggled.connect(self.__click_accumulate)
        
        # Add these buttons into the widget
        layout_pourcentage_accu.addWidget(self.button_pourcentage)
        layout_pourcentage_accu.addWidget(self.button_accumulate)
        layout_pourcentage_accu.setAlignment(QtCore.Qt.AlignCenter)
        
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
        
        # Add different widget create above
        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.addWidget(widget_canvas)
        layout_principal.addWidget(self.__widget_button_years)
        layout_principal.addWidget(widget_pourcentage_accu)
        layout_principal.addWidget(widget_bar_curve)
        
        
    def __create_list_buttons(
        self,
        data_dict: Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]],
        type_button: Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox],
        fct: Callable
    ) -> Tuple[QtWidgets.QWidget, QtWidgets.QHBoxLayout]:
        """ Create a widget where the layout is horizontal and it contains the button from a dictionary.
            When you click on a button, it calls the function 'fct'. You can give the type of the button

        Args:
            data_dict (Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]]): Dictionary
            type_button (Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox]): Type of button
            fct (Callable): function call when you click on a button

        Returns:
            Tuple[QtWidgets.QWidget, QtWidgets.QHBoxLayout]: The widget and the layout with all the buttons inside
        """
        # Create the widget and a horizontal layout
        widget = QtWidgets.QWidget(self)
        widget.setFixedHeight(40)
        layout = QtWidgets.QHBoxLayout(widget)
        
        # For each key of the dictionary, we create a button
        for data_ind, data in enumerate(data_dict.keys()):
            data_dict[data]["button"] = type_button(data)
            # If the type of button is a radio button, we need to have oonly one activated
            if type_button == QtWidgets.QRadioButton:
                data_dict[data]["checked"] = True if data_ind == 0 else False
            else:
                data_dict[data]["checked"] = True
            data_dict[data]["button"].setChecked(data_dict[data]["checked"])
            # Connect the button to the function
            data_dict[data]["button"].toggled.connect(partial(fct, data))
            layout.addWidget(data_dict[data]["button"])
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        return widget, layout
    
    
    def __remove_buttons_layout(
        self,
        data_dict: Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]],
        layout: QtWidgets.QHBoxLayout
    ) -> None:
        """ Remove the buttons from the layout and the dictionary

        Args:
            data_dict (Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]]): Dictionary
            layout (QtWidgets.QHBoxLayout): Layout
        """
        # Remove all buttons from the layout and the dictionary
        for d in data_dict:
            layout.removeWidget(data_dict[d]["button"])
            del data_dict[d]["checked"]
            del data_dict[d]["button"]
    
    
    def __update_buttons_layout(
        self,
        data_dict: Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]],
        layout: QtWidgets.QHBoxLayout,
        type_button: Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox],
        fct: Callable
    ) -> None:
        """ Update the buttons from the layout and the dictionary with the new type of buttons.
            When you click on the buttons, it calls the function 'fct'

        Args:
            data_dict (Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]]): Dictionary
            layout (QtWidgets.QHBoxLayout): Layout
            type_button (Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox]): New type of buttons
            fct (Callable): Function calls when the buttons is pressed
        """
        # Add a button for each key of the diictionary
        for data_ind, data in enumerate(data_dict.keys()):
            data_dict[data]["button"] = type_button(data)
            # If the type of button is a radio button, we need to have oonly one activated
            if type_button == QtWidgets.QRadioButton:
                data_dict[data]["checked"] = True if data_ind == 0 else False
            else:
                data_dict[data]["checked"] = True
            data_dict[data]["button"].setChecked(data_dict[data]["checked"])
            data_dict[data]["button"].toggled.connect(partial(fct, data))
            layout.addWidget(data_dict[data]["button"])


#######################################################################################################
#  Draw the graph in the canvas                                                                       #
#######################################################################################################    
    def __draw(self) -> None:
        """ Draw the graph into the canvas
        """
        # Clear the graph
        self.__axes.cla()
        
        # Draw the graph with bars or curves depending on the parameters
        if self.__is_bars_selected:
            self.__draw_bars()
        else:
            self.__draw_curve()
        
        # Construct the label for y-axis depending on the parameters
        label_y = "Nombre d'émissions"
        if self.__accumulate:
            label_y += " en cumulées"
        label_y +=  " (%)" if self.__is_pourcentage else f" ({self.__unit})"
        self.__axes.set_ylabel(label_y)
        
        # Draw the graph
        self.__figCanvas.draw()

    
    def __draw_bars(self) -> None:
        """ Draw a graph with bars into the canvas
        """
        has_bars = False
        nb_missions = 0
        for year in self.__years_ind.keys():
            # No need to draw a bar for a year who are not selected by the user
            if not self.__years_ind[year]["checked"]:
                continue
            
            # Get the data to plot bars
            emission_mode = self.__get_x_bars(year)

            # Plot bars for each mode
            # The color of the bar represent a mode
            nb_missions_mode = 0
            for mode in emission_mode:
                if len(emission_mode[mode]["mission"]) == 0:
                    continue
                self.__axes.bar(emission_mode[mode]["mission"], emission_mode[mode]["value"], width=self.__width, label=mode)
                has_bars = True
                nb_missions_mode += len(emission_mode[mode]["mission"]) 
        
            if nb_missions < nb_missions_mode:
                nb_missions = nb_missions_mode
    
        # Display legend if there are some bars plot
        if has_bars:
            self.__axes.set_xlim(left=0, right=nb_missions)
            self.__axes.legend()
    
    
    def __get_x_bars(self, year: str) -> Dict[str, Dict[str, List[Union[int, float]]]]:
        """ Create and fill a structure to plot the bar depending for a year

        Args:
            year (str): The year

        Returns:
            Dict[str, Dict[str, List[Union[int, float]]]]: Structure
        """
        # Create structure
        # The structure contains :
        # - mission: a list with the number of the mission for a certain mode
        # - value: a list with the emission due to the mission by the moe
        x_label_value = {}
        for mode in self.__mode_ind.keys():
            x_label_value[mode] = {"mission" : [], "value": []}
        
        data_year = self.__data_emission[year]["data"]
        data_year_sum = self.__data_emission[year]["sum"]
        value_accumulate = 0
        for val in data_year:
            mission, value, mode, pos = val
            x_label_value[mode]["mission"].append(mission + 1)
            
            # Depending on the parameters, we calculate the correct value
            # Pourcentage or value, and if it's accumulate
            value_modif = 100*value/data_year_sum if self.__is_pourcentage else value
            value_accumulate += value_modif
            x_label_value[mode]["value"].append(value_accumulate if self.__accumulate else value_modif)

        return x_label_value
        
        
    def __draw_curve(self) -> None:
        """ Draw a graph with curves into the canvas
        """
        has_curve = False
        nb_mission_max = 0
        for year in self.__years_ind.keys():
            # If the year is not selected by the user, no need to plot it
            if not self.__years_ind[year]["checked"]:
                continue
            
            # Get data to plot curve for the year
            emission = self.__get_x_curve(year)
            if len(emission["mission"]) == 0:
                continue
            self.__axes.plot(emission["mission"], emission["value"], label=year)
            has_curve = True
            
            if len(emission["mission"]) > nb_mission_max:
                nb_mission_max = len(emission["mission"])
        
        # If there are some curves, we display a legend
        if has_curve:
            self.__axes.set_xlim(left=0, right=nb_mission_max)
            self.__axes.legend()
    
    
    def __get_x_curve(self, year: str) -> Dict[str, List[Union[int, float]]]:
        """ Create and fill the structure used to plot curves for a year

        Args:
            year (str): A year

        Returns:
            Dict[str, List[Union[int, float]]]: Structure
        """
        # Structure is the same as bars
        x_label_value = {"mission": [], "value": []}
        data_year = self.__data_emission[year]["data"]
        data_year_sum = self.__data_emission[year]["sum"]
        value_accumulate = 0
        if self.__accumulate:
            x_label_value["mission"].append(0)
            x_label_value["value"].append(0)
        for val in data_year:
            mission, value, mode, pos = val
            x_label_value["mission"].append(mission + 1)
            
            # Depending on the parameters, we calculate the correct value
            # Pourcentage or value, and if it's accumulate
            value_modif = 100*value/data_year_sum if self.__is_pourcentage else value
            value_accumulate += value_modif
            x_label_value["value"].append(value_accumulate if self.__accumulate else value_modif)
            
        return x_label_value

#######################################################################################################
#  Configure data to plot in the graph                                                                #
#######################################################################################################  
    def __configure_data(self) -> None:
        """ Create and fill the different structure defined in init()
        """
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
            if val_ges["category"] != "Missions":
                continue
            year = val_ges["year"]
            data_val_ges = val_ges["data"]
            
            self.__data_emission[year] = {"data": [], "sum": 0}
            
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
                self.__data_emission[year]["data"].append((i, value, mode, position))
                self.__data_emission[year]["sum"] += value


#######################################################################################################
#  Mouse event to change the graph                                                                    #
#######################################################################################################
    def __click_year_radiobutton(self, year: str, state: bool) -> None:
        """ When a user click on the radio button of "year", update the graph

        Args:
            year (str): radio button associated to the year
            state (bool): if it's checked or not
        """
        self.__years_ind[year]["checked"] = state
        if state or len(self.__years_ind.keys()) == 1:
            self.__draw()
            
            
    def __click_year_checkbutton(self, year: str, state: bool) -> None:
        """ Same as __click_year_radiobutton but with check buttons

        Args:
            year (str): check button associated to the year
            state (bool): if it's checked or not
        """
        self.__years_ind[year]["checked"] = state
        self.__draw()


    def __click_pourcentage(self, state: bool) -> None:
        """ When a user click on the button, the values of the graph are in pourcentage if state is true.
            Else it remains the value.
        Args:
            state (bool): Button is checked or not
        """
        self.__is_pourcentage = state
        self.__draw()
        
    
    def __click_accumulate(self, state: bool) -> None:
        """ When an user click on the button, the graph display the value in a descending order.
            If state is true, then the graph display accumulate values
        Args:
            state (bool): Button is checked or not
        """
        self.__accumulate = state
        self.__draw()
        
        
    def __select_bar_graph(self, selected):
        """ Check if the radio button to draw bars is selected or not

        Args:
            selected (bool): the button is selected or not
        """
        if selected:
            self.__is_bars_selected = True
            self.__remove_buttons_layout(self.__years_ind, self.layout_button_years)
            self.__update_buttons_layout(
                self.__years_ind,
                self.layout_button_years,
                QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
                self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
            )
            self.__draw()
    
    
    def __select_curve_graph(self, selected):
        """ Check if the radio button to draw curves is selected or not

        Args:
            selected (bool): the button is selected or not
        """
        if selected:
            self.__is_bars_selected = False
            self.__remove_buttons_layout(self.__years_ind, self.layout_button_years)
            self.__update_buttons_layout(
                self.__years_ind,
                self.layout_button_years,
                QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
                self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
            )
            self.__draw()

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################    
    def update(self):
        """ Update the structure and the UI of the graph when the controller is update.
        """
        self.__remove_buttons_layout(self.__years_ind, self.layout_button_years)
        
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__position_ind = {} # Same with position
        self.__years_ind = {}    # Same with year
        self.__data_emission = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        
        self.__unit = common.check_value(self.__gesanalysis, "emission")
        self.__configure_data()
        
        self.__update_buttons_layout(
            self.__years_ind,
            self.layout_button_years,
            QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
            self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
        )
        
        self.__draw()