from typing import Callable, Dict, Tuple, Union
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from GESAnalysis.UI.ChangeNacresCodeDialog import ChangeNacresCodeDialog
from functools import partial


class KeyAmount(QtWidgets.QWidget):
    """ Widget to draw a graph representing the amount for each NACRES key
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    __spacing = 0.7                                 # Spacing between bars of each mode
    
    
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class by setting the data and draw the graph

        Args:
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(KeyAmount, self).__init__(parent)
        
        # Data structure
        self.__years_ind = {}          # Dictionary of year
        self.__nacres_key_code = ['*'] # Nacres key code
        self.__data_achats = {}        # Dictionary of data
        self.__unit = ""               # Unit
        
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        self.__init_UI()
        
        self.__draw()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar and a button to control the graph and the nacres code
        widget_toolbar_button = QtWidgets.QWidget(widget_canvas)
        widget_toolbar_button.setContentsMargins(0, 0, 0, 0)
        widget_toolbar_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout_toolbar_button = QtWidgets.QHBoxLayout(widget_toolbar_button)
        toolbar = NavigationToolbar2QT(self.__figCanvas, widget_toolbar_button)
        button_code = QtWidgets.QPushButton("Code NACRES", widget_toolbar_button)
        button_code.setFixedHeight(20)
        button_code.clicked.connect(self.__change_nacres_key_code)
        layout_toolbar_button.addWidget(toolbar)
        layout_toolbar_button.addWidget(button_code)
        widget_toolbar_button.setLayout(layout_toolbar_button)
        
        # Create list of radio buttons to select the year
        self.__widget_buttons_years, self.__layout_buttons_years = self.__create_radiobuttons(
            self.__years_ind,
            self.__click_year_radiobutton
        )
        
        # Add to widget canvas
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(widget_toolbar_button)
        layout_canvas.addWidget(self.__figCanvas)
        layout_canvas.addWidget(self.__widget_buttons_years)
        widget_canvas.setLayout(layout_canvas)
        
        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(widget_canvas)
        self.setLayout(layout_principal)
        
        
    def __create_radiobuttons(self, data_dict:dict, fct: Callable) -> Tuple[QtWidgets.QWidget, QtWidgets.QHBoxLayout]:
        """ Create a list of radiobuttons from the keys in a dictionary. 
            When you press on the button, it called the function fct

        Args:
            data_dict (dict): Dictionary
            fct (Callable): Function

        Returns:
            Tuple[QtWidgets.QWidget, QtWidgets.QHBoxLayout]: Widget, with buttons, and his layout
        """
        widget = QtWidgets.QWidget(self)
        widget.setFixedHeight(40)
        layout = QtWidgets.QHBoxLayout(widget)
        
        for data_ind, data_key in enumerate(data_dict.keys()):
            data_dict[data_key]["button"] = QtWidgets.QRadioButton(data_key, widget)
            data_dict[data_key]["checked"] = True if data_ind == 0 else False
            data_dict[data_key]["button"].setChecked(data_dict[data_key]["checked"])
            data_dict[data_key]["button"].toggled.connect(partial(fct, data_key))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        return widget, layout
    
    
    def __remove_radiobuttons(self, data_dict, layout: QtWidgets.QHBoxLayout) -> None:
        """ Remove the buttons in the dictionary and the layout

        Args:
            data_dict (dict): Dictionary
            layout (QtWidgets.QHBoxLayout): Layout
        """
        for data_key in data_dict.keys():
            layout.removeWidget(data_dict[data_key]["button"])
            del data_dict[data_key]["checked"]
            del data_dict[data_key]["button"]
            
            
    def __update_radiobuttons(self, data_dict, layout: QtWidgets.QHBoxLayout, fct: Callable) -> None:
        """ Update the radiobuttons in the layout and the dictionary.
            When you click on the buttons, it calls the function fct

        Args:
            data_dict (dict): Dictionary
            layout (QtWidgets.QHBoxLayout): Layout
            fct (Callable): Function
        """
        for data_ind, data_key in enumerate(data_dict.keys()):
            data_dict[data_key]["button"] = QtWidgets.QRadioButton(data_key)
            data_dict[data_key]["checked"] = True if data_ind == 0 else False
            data_dict[data_key]["button"].setChecked(data_dict[data_key]["checked"])
            data_dict[data_key]["button"].toggled.connect(partial(fct, data_key))
            layout.addWidget(data_dict[data_key]["button"])
        

#######################################################################################################
#  Draw the graph in the canvas                                                                       #
#######################################################################################################
    def __draw(self) -> None:
        """ Draw the graph in the canvas
        """
        self.__axes.cla()
        
        data_graph_dict = self.__build_dict_graph()
        
        # Transform dict to list
        dict_to_list = []
        for key, data_key in data_graph_dict.items():
            dict_to_list.append((key, data_key["position"], data_key["amount"]))
        
        # Sort this list by position
        dict_to_list.sort(key=lambda a:a[1])
        
        # Separate this list into 3 lists
        x_labels_code = []
        x_position = []
        y_amount_code = []
        for key, pos, amount in dict_to_list:
            x_labels_code.append(key)
            x_position.append(pos)
            y_amount_code.append(amount)
        
        # Draw the bars
        self.__axes.bar(x_position, y_amount_code, width=self.__width)
        
        # Set labels on x-axis
        self.__axes.set_xticks(x_position)
        self.__axes.set_xticklabels(x_labels_code, rotation=90, fontsize=10)
        
        # Set a label for y-axis
        self.__axes.set_ylabel(f"Montant ({self.__unit})")
        
        # Set x limit
        if len(x_position) > 0:
            self.__axes.set_xlim(0-self.__width, x_position[len(x_position) - 1]+self.__width)
        
        # Draw on canvas
        self.__figCanvas.draw()

        
    def __build_dict_graph(self) -> Dict[str, Dict[str, Union[float, int]]]:
        """ Create a dictionary for the graph. This dictionary contains the keys
            accepted by the code (nacres_key_code) with the position on X-axis and his amount.

        Returns:
            Dict[str, Dict[str, Union[float, int]]]: Dictionary
        """
        data_for_graph = {}
        current_position = 0
        for year, data_year in self.__data_achats.items():
            # If the year is not select, then pass to next year
            if not self.__years_ind[year]["checked"]:
                continue
            
            for nacres_key, amount in data_year:
                # If the key is not accepted by the nacres code (user), continue with the next key
                if not self.__analyse_key_code_list(nacres_key):
                    continue
                
                # Else, if the key is already in the dictionary, then add his amount
                if nacres_key in data_for_graph.keys():
                    data_for_graph[nacres_key]["amount"] += amount
                # Else, add into the dictionary
                else:
                    data_for_graph[nacres_key] = {
                        "position": current_position,
                        "amount": amount
                    }
                    current_position += self.__width + self.__spacing

        return data_for_graph     
                
                
    def __analyse_key_code_list(self, key: str) -> bool:
        """ Indicate if the key is accepted by the list of code

        Args:
            key (str): Key

        Returns:
            bool: True if the key is accepted by the list of codes, else False
        """
        for code in self.__nacres_key_code:
            if self.__is_key_in_code(key, code):
                return True
        return False
    
    
    def __is_key_in_code(self, key: str, code: str) -> bool:
        """ Indicate if the key is accepted by the code

        Args:
            key (str): Key
            code (str): Code

        Returns:
            bool: True if the key is accepted, else False
        """
        # code = '*' -> accept all keys
        if code == "*":
            return True
        
        if code[0] == '*':
            # Code = "*Z*" -> Search if the key is in the code
            if code[len(code) - 1] == '*':
                search_code = code[1:len(code)-1]
                return search_code in key
            # Code = "*Z" -> Compare the end between the key and the coe
            else:
                return self.__compare_end(key, code)
        elif code[len(code) - 1] == '*':
            return self.__compare_start(key, code)
        elif '*' in code:
            split_code = code.split('*')
            code_start = split_code[0] + '*'
            code_end = '*' + split_code[1]
            return self.__compare_start(key, code_start) and self.__compare_end(key, code_end)
        else:
            return key == code
                
    
    def __compare_end(self, key: str, code: str) -> bool:
        """ Compare if key and code has the same end

        Args:
            key (str): Key
            code (str): Key

        Returns:
            bool: True if the end is the same, else False
        """
        for i in range(1, len(code)):
            if code[len(code)-i] != key[len(key)-i]:
                return False
        return True
    
    
    def __compare_start(self, key: str, code: str) -> bool:
        """ Compare if key and code has the same start

        Args:
            key (str): Key
            code (str): Code

        Returns:
            bool: True if the start is the same, else False
        """
        for i in range(len(code)-1):
            if key[i] != code[i]:
                return False
        return True
    

#######################################################################################################
#  Mouse event to change the graph                                                                    #
#######################################################################################################
    def __click_year_radiobutton(self, year:str, state:bool) -> None:
        self.__years_ind[year]["checked"] = state
        if state or len(self.__years_ind.keys()) == 1:
            self.__draw()
                        
        
#######################################################################################################
#  Method associated to an action                                                                     #
#######################################################################################################
    def __change_nacres_key_code(self):
        """ Execute a dialog to change the code when the user press on the button "code NACRES"
        """
        self.change_nacres_code_dialog = ChangeNacresCodeDialog(';'.join(self.__nacres_key_code), self)
        if self.change_nacres_code_dialog.exec_():
            new_code = self.change_nacres_code_dialog.selected_code
            self.__nacres_key_code = new_code.split(';')
            
            # Re-draw the graph due to the update of the code
            self.__draw()
            
        
#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update_canvas(self, years_ind, data_dict) -> None:
        """ Update the data structure and the graph when there is an update from AchatsWidget

        Args:
            years_ind : Dictionary of years
            data_dict : Dictionary of data
        """
        # Remove all data in the dictionaries
        self.__remove_radiobuttons(self.__years_ind, self.__layout_buttons_years)
        self.__years_ind.clear()
        self.__data_achats.clear()
        self.__unit = ""
        
        # Update the data structure
        self.__years_ind = years_ind.copy()
        self.__data_achats = data_dict["data"]
        self.__unit = data_dict["unit"]
        
        self.__update_radiobuttons(self.__years_ind, self.__layout_buttons_years, self.__click_year_radiobutton)
        
        self.__draw()
