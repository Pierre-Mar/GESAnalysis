import GESAnalysis.UI.categories.common as common
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from functools import partial
from typing import Any, Callable, Dict, List, Tuple, Union


class EmissionMode(QtWidgets.QWidget):
    """ Class to represent graphically
        the emission for each mission according to the mode of transport
        and the position of people
    """
    __width = 0.5
    
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        super(EmissionMode, self).__init__(parent)
        
        self.__mode_dict = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__years_dict = {}    # Same with year
        self.__emission_dict = {}    # Dictionary where the key is a year and the value a list with distance for all mode
        self.__is_pourcentage = False
        self.__accumulate = False
        self.__with_contrails = False
        self.__is_bars_selected = True
        self.__unit_emission = ""
        self.__unit_emission_contrails = ""
        
        # Create figure
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Initialisation UI
        self.__init_UI()


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
        self.__widget_button_years, self.__layout_button_years = self.__create_list_buttons(
            self.__years_dict,
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
        
        # Create a check button to display the emission with contrails
        self.button_contrails = QtWidgets.QCheckBox("Trainées")
        self.button_contrails.setChecked(self.__with_contrails)
        self.button_contrails.toggled.connect(self.__click_contrails)
        
        # Add these buttons into the widget
        layout_pourcentage_accu.addWidget(self.button_pourcentage)
        layout_pourcentage_accu.addWidget(self.button_accumulate)
        layout_pourcentage_accu.addWidget(self.button_contrails)
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
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        if len(data_dict) == 0:
            widget.hide()
            return widget, layout
        
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
        widget: QtWidgets.QWidget,
        layout: QtWidgets.QHBoxLayout,
        type_button: Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox],
        fct: Callable
    ) -> None:
        """ Update the buttons from the layout and the dictionary with the new type of buttons.
            When you click on the buttons, it calls the function 'fct'

        Args:
            data_dict (Dict[str, Dict[str, Union[int, bool, QtWidgets.QRadioButton, QtWidgets.QCheckBox]]]): Dictionary
            widget (QtWidgets.QWidget): Widget
            layout (QtWidgets.QHBoxLayout): Layout
            type_button (Union[QtWidgets.QRadioButton, QtWidgets.QCheckBox]): New type of buttons
            fct (Callable): Function calls when the buttons is pressed
        """
        # Add a button for each key of the dictionary
        for data_ind, data in enumerate(data_dict.keys()):
            data_dict[data]["button"] = type_button(data)
            # If the type of button is a radio button, we need to have only one activated
            if type_button == QtWidgets.QRadioButton:
                data_dict[data]["checked"] = True if data_ind == 0 else False
            else:
                data_dict[data]["checked"] = True
            data_dict[data]["button"].setChecked(data_dict[data]["checked"])
            data_dict[data]["button"].toggled.connect(partial(fct, data))
            layout.addWidget(data_dict[data]["button"])
            
        if len(data_dict.keys()) == 0:
            widget.hide()
        else:
            widget.show()


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
        
        # Set unit to y-label
        if self.__is_pourcentage:
            label_y += " (%)"
        else:
            if self.__with_contrails:
                label_y += f" ({self.__unit_emission_contrails})"
            else:
                label_y += f" ({self.__unit_emission})"
        self.__axes.set_ylabel(label_y)
        
        # Draw the graph
        self.__figCanvas.draw()

    
    def __draw_bars(self) -> None:
        """ Draw a graph with bars into the canvas
        """
        has_bars = False
        nb_missions = 0
        for year in self.__years_dict.keys():
            # No need to draw a bar for a year who are not selected by the user
            if not self.__years_dict[year]["checked"]:
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
        
        # Use the correct dictionary with contrails or not
        use_dict = self.__emission_dict["normal"]
        if self.__with_contrails:
            use_dict = self.__emission_dict["contrails"]
            
        for mode in self.__mode_dict.keys():
            x_label_value[mode] = {"mission" : [], "value": []}
        
        data_year = use_dict[year]["data"]
        data_year_sum = use_dict[year]["sum"]
        value_accumulate = 0
        for val_ind, val in enumerate(data_year):
            emission, mode = val
            x_label_value[mode]["mission"].append(val_ind + 1)
            
            # Depending on the parameters, we calculate the correct value
            # Pourcentage or value, and if it's accumulate
            value_modif = 100*emission/data_year_sum if self.__is_pourcentage else emission
            value_accumulate += value_modif
            x_label_value[mode]["value"].append(value_accumulate if self.__accumulate else value_modif)

        return x_label_value
        
        
    def __draw_curve(self) -> None:
        """ Draw a graph with curves into the canvas
        """
        has_curve = False
        nb_mission_max = 0
        for year in self.__years_dict.keys():
            # If the year is not selected by the user, no need to plot it
            if not self.__years_dict[year]["checked"]:
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
        
        # Use the correct dictionary with contrails or not
        use_dict = self.__emission_dict["normal"]
        if self.__with_contrails:
            use_dict = self.__emission_dict["contrails"]
        
        data_year = use_dict[year]["data"]
        data_year_sum = use_dict[year]["sum"]
        value_accumulate = 0
        if self.__accumulate:
            x_label_value["mission"].append(0)
            x_label_value["value"].append(0)
        for val_ind, val in enumerate(data_year):
            value = val[0]
            x_label_value["mission"].append(val_ind + 1)
            
            # Depending on the parameters, we calculate the correct value
            # Pourcentage or value, and if it's accumulate
            value_modif = 100*value/data_year_sum if self.__is_pourcentage else value
            value_accumulate += value_modif
            x_label_value["value"].append(value_accumulate if self.__accumulate else value_modif)
            
        return x_label_value


#######################################################################################################
#  Mouse event to change the graph                                                                    #
#######################################################################################################
    def __click_year_radiobutton(self, year: str, state: bool) -> None:
        """ When a user click on the radio button of "year", update the graph

        Args:
            year (str): radio button associated to the year
            state (bool): if it's checked or not
        """
        self.__years_dict[year]["checked"] = state
        if state or len(self.__years_dict.keys()) == 1:
            self.__draw()
            
            
    def __click_year_checkbutton(self, year: str, state: bool) -> None:
        """ Same as __click_year_radiobutton but with check buttons

        Args:
            year (str): check button associated to the year
            state (bool): if it's checked or not
        """
        self.__years_dict[year]["checked"] = state
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
        
        
    def __click_contrails(self, state: bool) -> None:
        """ When an user click on the button "Trainées", the graph display the emission with contrails

        Args:
            state (bool): Button is checked or not
        """
        self.__with_contrails = state
        self.__draw()
        
        
    def __select_bar_graph(self, selected):
        """ Check if the radio button to draw bars is selected or not

        Args:
            selected (bool): the button is selected or not
        """
        if selected:
            self.__is_bars_selected = True
            self.__remove_buttons_layout(self.__years_dict, self.__layout_button_years)
            self.__update_buttons_layout(
                self.__years_dict,
                self.__widget_button_years,
                self.__layout_button_years,
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
            self.__remove_buttons_layout(self.__years_dict, self.__layout_button_years)
            self.__update_buttons_layout(
                self.__years_dict,
                self.__widget_button_years,
                self.__layout_button_years,
                QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
                self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
            )
            self.__draw()


#######################################################################################################
#  Update graph from Mission Widget                                                                   #
#######################################################################################################    
    def update_canvas(self, mode_ind, years_ind, data_dict):
        """ Update the structure and the UI of the graph when it's call by MissionWidget.
        """
        self.__remove_buttons_layout(self.__years_dict, self.__layout_button_years)
        
        self.__mode_dict = self.__update_structure(mode_ind)
        self.__years_dict = self.__update_structure(years_ind)
        self.__emission_dict = self.__rearrange_data(data_dict["data"].copy())
        self.__unit_emission = data_dict["unit_emission"]
        self.__unit_emission_contrails = data_dict["unit_emission_contrails"]
        
        self.__update_buttons_layout(
            self.__years_dict,
            self.__widget_button_years,
            self.__layout_button_years,
            QtWidgets.QRadioButton if self.__is_bars_selected else QtWidgets.QCheckBox,
            self.__click_year_radiobutton if self.__is_bars_selected else self.__click_year_checkbutton
        )
        
        self.__draw()
        
        
    def __rearrange_data(self, data_dict):
        """ Arrange data for the graph

        Args:
            data_dict : Data

        Returns:
            Data for graph
        """
        dictionary = {}
        dictionary["normal"] = {}
        dictionary["contrails"] = {}
        for year in self.__years_dict.keys():
            dictionary["normal"][year] = {
                "data" :[],
                "sum": 0
            }
            dictionary["contrails"][year] = {
                "data" :[],
                "sum": 0
            }
        
        # Arrange data into the dictionary
        for mode, data_mode in data_dict.items():
            for position, position_data in data_mode["data"].items():
                for year, year_data in position_data.items():
                    missions = year_data["mission"]
                    for value in missions:
                        emis = value[2]
                        emis_contrails = value[3]
                        dictionary["normal"][year]["data"].append((emis, mode))
                        dictionary["normal"][year]["sum"] += emis
                        dictionary["contrails"][year]["data"].append((emis_contrails, mode))
                        dictionary["contrails"][year]["sum"] += emis_contrails
        
        # Sort value of emission by descending order
        for d in dictionary.values():
            for data_year in d.values():
                data_year["data"].sort(key=lambda a:a[0], reverse=True)
                data_year["data"].sort(key=lambda a:a[0], reverse=True)

        return dictionary
    

    def __update_structure(self, data_dict):
        """ Update the structure for dictionary

        Args:
            data_dict : Dictionary

        Returns:
            Dictionary for graph
        """
        data_class = {}
        for data in data_dict.keys():
            data_class[data] = {}
        return data_class
