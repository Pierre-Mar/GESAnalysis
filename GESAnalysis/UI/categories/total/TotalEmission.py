import matplotlib
from GESAnalysis.FC.Controleur import Controleur

from GESAnalysis.UI.AgentFileDialog import AgentFileDialog

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from typing import Optional, Tuple, List
from GESAnalysis.UI import common


class TotalEmission(QtWidgets.QWidget):
    """ Widget to draw a graph representing the emission for each year
    """
    
    # Values use to draw the graph
    __width = 0.3                                   # Width of bars
    __spacing = 0.8                                 # Spacing between bars of each mode
    
    
    def __init__(self, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class by setting the data and draw the graph

        Args:
            controller (Controleur): controller
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(TotalEmission, self).__init__(parent)
        
        # Set parameter to attribute
        self.__controller = controller
        
        # Data structure
        self.__years_ind = {}       # Dictionary of year
        self.__name_ind = {}        # Dictionary of categories
        self.__data_tot = {}        # Dictionary of data
        self.__unit = ""            # Unit of data
        self.__data_agent = {}      # Dictionary containing the number of agent
        self.__path_to_agent = None # Path to read the agent file
        
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)
        self.__figCanvas = FigureCanvasQTAgg(self.__fig)
        
        # Initialise the UI
        self.__init_UI()
        
        # Draw the graph
        self.__draw()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialize the UI
        """
        widget_canvas = QtWidgets.QWidget(self)
        
        # Add toolbar to control the graph and button to read "effectif"
        widget_buttons = QtWidgets.QWidget(widget_canvas)
        widget_buttons.setContentsMargins(0,0,0,0)
        widget_buttons.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout_buttons = QtWidgets.QHBoxLayout(widget_buttons)
        toolbar = NavigationToolbar2QT(self.__figCanvas, widget_buttons)
        read_agent_button = QtWidgets.QPushButton("Fichier Agents", widget_buttons)
        read_agent_button.setFixedHeight(20)
        read_agent_button.clicked.connect(self.__read_agent_file)
        layout_buttons.addWidget(toolbar)
        layout_buttons.addWidget(read_agent_button)
        widget_buttons.setLayout(layout_buttons)
        
        # Create checkbutton to display the emission per agent (from effectif)
        widget_checkbutton = QtWidgets.QWidget(self)
        widget_checkbutton.setFixedHeight(40)
        widget_checkbutton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout_checkbutton = QtWidgets.QHBoxLayout(widget_checkbutton)
        self.__agent_checkbutton = QtWidgets.QCheckBox("Par Agents", widget_canvas)
        self.__agent_checkbutton.setFixedHeight(20)
        self.__agent_checkbutton.clicked.connect(self.__draw_graph_per_agents)
        layout_checkbutton.addWidget(self.__agent_checkbutton)
        layout_checkbutton.setAlignment(QtCore.Qt.AlignCenter)
        widget_checkbutton.setLayout(layout_checkbutton)
        
        layout_canvas = QtWidgets.QVBoxLayout(widget_canvas)
        layout_canvas.addWidget(widget_buttons)
        layout_canvas.addWidget(self.__figCanvas)
        layout_canvas.addWidget(widget_checkbutton)
        widget_canvas.setLayout(layout_canvas)
        
        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(widget_canvas)
        self.setLayout(layout_principal)
    

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
        bar_container = None
        
        # Add bar to the graph
        for name, data_name in self.__data_tot.items():
            data_transform = self.__data_per_agent(data_name["data"])

            bar_container = self.__axes.bar(x_bars, data_transform, width=self.__width, bottom=bottom, linewidth=0.5, edgecolor='black')
            for i in range(len(bottom)):
                # Add text if we display the emission per agent
                if self.__agent_checkbutton.isChecked():
                    color = bar_container[0].get_facecolor()
                    self.__axes.text(
                        x_bars[i] + self.__width/2,
                        bottom[i] + data_transform[i]/2,
                        str(round(data_transform[i], 2)),
                        color=color
                    )
                bottom[i] += data_transform[i]
            y_labels[self.__name_ind[name]["index"]] = name
        
        # Set x labels
        self.__axes.set_xticks(x_bars, x_labels)
        
        # Put a legend if there are data display
        if len(y_labels):
            self.__axes.legend(y_labels)
        
        # Put a label on y-axis
        self.__axes.set_ylabel(f"Empreinte carbonne ({self.__unit})")
        
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
    
    
    def __data_per_agent(self, data: list) -> list:
        """ Transform the data to data per agent for the graph

        Args:
            data (list): Data

        Returns:
            list: Data per agent if the button 'Par Agents' is checked, else Data.
        """
        data_transform = data.copy()
        if not self.__agent_checkbutton.isChecked():
            return data
        
        for year, year_val in self.__years_ind.items():
            try:
                index_year = year_val['index']
                data_transform[index_year] /= self.__data_agent[year]
            except:
                return data
        return data_transform
    
    
#######################################################################################################
#  Method associated to an action                                                                     #
#######################################################################################################
    def __read_agent_file(self) -> None:
        """ Open a dialog to read a file who contains the number of agent for each year
        """
        open_file_dialog = AgentFileDialog(self.__path_to_agent, self.__controller, self)
        if open_file_dialog.exec_():
            # If it's the same file, no need to continue, we already have the information
            if open_file_dialog.selected_file == self.__path_to_agent:
                return
            
            self.__path_to_agent = open_file_dialog.selected_file
            self.__data_agent = open_file_dialog.data_agent_per_year
    
    
    def __draw_graph_per_agents(self, state:bool) -> None:
        """ Draw the graph per agent if the user clicked on the button "Par Agents"

        Args:
            state (bool): True if the button is checked, else False
        """
        if state:
            # If there are no agent, then send an error
            if self.__path_to_agent is None:
                self.__agent_checkbutton.setChecked(False)
                common.message_warning(
                    "Veuillez indiquer un fichier contenant les agents.\nPour cela, appuyer sur le bouton 'Fichier Agents' et renseigner le chemin du fichier",
                    self
                )
                return

            # Else, we check if all the year are in the dictionary
            is_missing_year = False
            missing_year = []
            for year in self.__years_ind.keys():
                if year not in self.__data_agent.keys():
                    is_missing_year = True
                    missing_year.append(year)
            
            if is_missing_year:
                text = "Les années"
                if len(missing_year) == 1:
                    text = "L'année"
                join_year = ",".join(missing_year)
                common.message_warning(
                    f"Il n'y a pas d'agents pour {text} '{join_year}'",
                    self
                )
                return
            
        self.__draw()
            

#######################################################################################################
#  Update graph from Observer                                                                         #
#######################################################################################################
    def update_canvas(self, name_ind, years_ind, data_dict) -> None:
        """ Update the structure when the model are updated
        """
        self.__agent_checkbutton.setChecked(False)
        self.__years_ind = years_ind
        self.__name_ind = name_ind
        self.__data_tot = data_dict["data"]
        self.__unit = data_dict["unit"]

        self.__draw()
