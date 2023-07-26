from typing import List

from PyQt5 import QtCore, QtWidgets
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from .DistanceMode import DistanceMode
from .EmissionMode import EmissionMode
from .MissionStatWidget import MissionStatWidget
import GESAnalysis.UI.categories.common as common


class MissionsWidget(QtWidgets.QWidget, Observer):
    """ Widget use to regroup the graphs, the files opener and the stats of the category "Missions"
    """
     
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        category: str,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the class

        Args:
            model (GESAnalysis): Model
            controller (Controleur): Controller
            category (str): Category
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(MissionsWidget, self).__init__(parent)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        # Add this widget to the list of observers to update his interface
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {}        # Dictionary where the key is the file in 'category' and a bool if it's read or not
        self.__mode_ind = {}     # Dictionary where the key is the mode of transport and the value his index
        self.__years_ind = {}    # Same with year
        self.__position_ind = {} # Same with position
        self.__data = {}         # Dictionary where the key is a year and the value a list with distance for all mode

        self.__configure_data()
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameter of this widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Splitter to divide the sections
        splitter = QtWidgets.QSplitter(self)
        
        # Widget for left-splitter (file open + stats)
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_mission_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        self.__stat_mission_widget = MissionStatWidget(self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_mission_widget)
        splitter_left_layout.addWidget(self.__stat_mission_widget)
        splitter_left_widget.setLayout(splitter_left_layout)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graphs_widget = QtWidgets.QTabWidget(splitter)
        self.__distance_canvas = DistanceMode(self.__tab_graphs_widget)
        self.__emissions_canvas = EmissionMode(self.__tab_graphs_widget)
        self.__tab_graphs_widget.addTab(self.__distance_canvas, "Distance")
        self.__tab_graphs_widget.addTab(self.__emissions_canvas, "Emission")
        
        # Add both widgets to splitter
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graphs_widget)
        splitter.setSizes([200, 1000])
        
        # layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(splitter)
        self.setLayout(layout_principal)
        

#######################################################################################################
#  Configure data                                                                                     #
#######################################################################################################
    def __configure_data(self) -> None:
        """ Configure the data for the canvas inside this widget (distance/emission)
        """
        ind_mode = 0
        ind_year = 0
        ind_position = 0
        unit_distance = ""
        unit_emission = ""
        unit_emission_contrails = ""
        # Get all the mode, position and for each file
        for file, data_file in self.__gesanalysis.get_data().items():
            if data_file["category"] != self.__category:
                continue
            
            # Add file to self.__files and set bool
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
            
            compare_column = True
            
            data = data_file["data"]
            
            mission = common.get_column(data, "name")
            if mission is None:
                compare_column = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'name' non-trouvée")
            
            # Get the mode
            mode = common.get_column(data, "mode")
            if mode is None:
                compare_column = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'mode' non-trouvée")
            
            # Get the position
            position = common.get_column(data, "position")
            if position is None:
                compare_column = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'position' non-trouvée")
            
            # Check if there are the same number of lines between position and mode
            if compare_column and len(mode) != len(position):
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonnes 'mode' et 'position' n'ont pas les mêmes lignes")

            # Check if the column distance exist and there is the same number of lines with mode and position
            distance = common.get_column(data, "distance")
            if distance is None:
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'distance' non-trouvée")
            else:
                if compare_column and (len(distance) != len(mode) or len(distance) != len(position)):
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'distance' a un nombre de ligne différent")
                    
            emission = common.get_column(data, "emission")
            if distance is None:
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'emission' non-trouvée")
            else:
                if compare_column and (len(distance) != len(mode) or len(distance) != len(position)):
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'emission' a un nombre de ligne différent")
                    
            emission_contrails = common.get_column(data, "emission withcontrails")
            if emission_contrails is None:
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'emission avec trainées' non-trouvée")
            else:
                if compare_column and len(emission_contrails) != len(emission):
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'emission avec trainées' a un nombre de ligne différent")
                    
            # If there are some warnings, we don't calculate
            if not self.__files[file]["read"]:
                continue
            
            # Check the unit of distance
            unit = common.get_unit(data, "distance")
            if unit is None:
                self.__files[file]["warning"].append(f"Colonne 'distance' n'a pas d'unité")
            else:
                unit = "/".join(unit)
                if unit_distance == "":
                    unit_distance = unit
                if unit != unit_distance:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'distance' a une unité différente")
            
            # Same with emission
            unit = common.get_unit(data, "emission")
            if unit is None:
                self.__files[file]["warning"].append(f"Colonne 'emission' n'a pas d'unité")
            else:
                unit = "/".join(unit)
                if unit_emission == "":
                    unit_emission = unit
                if unit != unit_emission:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'emission' a une unité différente")
                    
            # Same with emission with contrails
            unit = common.get_unit(data, "emission withcontrails")
            if unit is None:
                self.__files[file]["warning"].append(f"Colonne 'emission avec trainées' n'a pas d'unité")
            else:
                unit = "/".join(unit)
                if unit_emission_contrails == "":
                    unit_emission_contrails = unit
                if unit != unit_emission_contrails:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'emission avec trainées' a une unité différente")   
            
            # Get the year
            year = data_file["year"]
            
            # If there are some warnings, we don't calculate
            if not self.__files[file]["read"]:
                continue
            
            # Add the mode and the position into their dictionary
            for i in range(len(mode)):
                mode_val = self.__analyse_mode(mode[i][0])
                if mode_val not in self.__mode_ind.keys():
                    self.__mode_ind[mode_val] = {"index": ind_mode}
                    ind_mode += 1
                if position[i][0] not in self.__position_ind.keys():
                    self.__position_ind[position[i][0]] = {"index": ind_position}
                    ind_position += 1
            
            # Add year to his dictionary   
            if year not in self.__years_ind.keys():     
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
         
        # Create structure to calculate the distance and the emission
        data_dist = {}
        for mode in self.__mode_ind.keys():
            data_dist[mode] = {
                "data": {},
                "sum": {}
            }
            for position in self.__position_ind.keys():
                data_dist[mode]["data"][position] = {}
                for year in self.__years_ind.keys():
                    data_dist[mode]["data"][position][year] = {
                        "mission": [],
                        "total_distance": 0,
                        "total_emission": 0,
                        "total_emission_contrails": 0
                    }
                    data_dist[mode]["sum"][year] = {
                        "distance": 0,
                        "emission": 0,
                        "emission_contrails": 0
                    }
                    
        # Now calculate the distance and the emission
        for file, data_file in self.__files.items():
            if not self.__files[file]["read"]:
                continue
            
            data = self.__gesanalysis.get_data_from_file(file)
            
            mission = common.get_column(data, "name")
            mode = common.get_column(data, "mode")
            position = common.get_column(data, "position")
            distance = common.get_column(data, "distance")
            emission = common.get_column(data, "emission")
            emission_contrails = common.get_column(data, "emission withcontrails")
            year = data_file["year"]
            
            for i in range(len(mission)):
                
                mode_val = self.__analyse_mode(mode[i][0])
                pos_val = position[i][0]
                
                # Add the distance
                sum_distance = sum(distance[i])
                sum_emission = sum(emission[i])
                sum_emission_contrails = sum(emission_contrails[i])
                for mis in mission[i]:
                    data_dist[mode_val]["data"][pos_val][year]["mission"].append((mis, sum_distance, sum_emission, sum_emission_contrails))
                    data_dist[mode_val]["data"][pos_val][year]["total_distance"] += sum_distance
                    data_dist[mode_val]["data"][pos_val][year]["total_emission"] += sum_emission
                    data_dist[mode_val]["data"][pos_val][year]["total_emission_contrails"] += sum_emission_contrails
                    data_dist[mode_val]["sum"][year]["distance"] += sum_distance
                    data_dist[mode_val]["sum"][year]["emission"] += sum_emission
                    data_dist[mode_val]["sum"][year]["emission"] += sum_emission_contrails
                
        self.__data = {
            "data": data_dist,
            "unit_distance": unit_distance,
            "unit_emission": unit_emission,
            "unit_emission_contrails": unit_emission_contrails
        }
        
        
    def __analyse_mode(self, mode: str) -> str:
        """ Test if a 'mode' is in the dictionary of mode

        Args:
            mode (str): Mode

        Returns:
            str: Mode in dictionary if it's in. Else return 'mode'
        """
        mode = mode.lower()
        if mode in self.__mode_ind.keys():
            return mode
        
        mode_cpy = mode + "s"
        if mode_cpy in self.__mode_ind.keys():
            return mode_cpy
        return mode


#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def close_files(self) -> None:
        """ Close files from this widget
        """
        self.__file_mission_widget.close_files()
        

#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def get_selected_files(self) -> List[str]:
        """ Get selected files from FileOpenUI

        Returns:
            List[str]: List of file names's
        """
        return self.__file_mission_widget.get_selected_files()


#######################################################################################################
#  Update widgets                                                                                     #
#######################################################################################################  
    def update(self):
        """ Update all the widget of this widget when the model change
        """
        # Remove all data inside the structure
        self.__data.clear()
        self.__position_ind.clear()
        self.__years_ind.clear()
        self.__mode_ind.clear()
        self.__files.clear()
        
        self.__configure_data()
        
        # Update FileOpenUI
        self.__file_mission_widget.update_widget(self.__files)
        
        # Update Stats
        self.__stat_mission_widget.update_widget(self.__years_ind, self.__mode_ind, self.__position_ind, self.__data)
        
        # Update the graph for distance
        self.__distance_canvas.update_canvas(self.__mode_ind, self.__position_ind, self.__years_ind, self.__data)
        
        # Update the graph for emission
        self.__emissions_canvas.update_canvas(self.__mode_ind, self.__years_ind, self.__data)
        
    
#######################################################################################################
#  Overwrite method to resize the widget                                                              #
####################################################################################################### 
    def sizeHint(self) -> QtCore.QSize:
        """ Return the ideal length of the widget

        Returns:
            QtCore.QSize: Width and height
        """
        return QtCore.QSize(1280, 720)
    
    
    def minimumSizeHint(self) -> QtCore.QSize:
        """ Return the minimal and ideal length of the widget

        Returns:
            QtCore.QSize: Width and height
        """
        return QtCore.QSize(640, 360)
    
    
    def sizePolicy(self) -> QtWidgets.QSizePolicy:
        """ Return the size policy of the widget.
            The width of the widget can extend but the height is fixed

        Returns:
            QtWidgets.QSizePolicy: Size policy
        """
        return QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
