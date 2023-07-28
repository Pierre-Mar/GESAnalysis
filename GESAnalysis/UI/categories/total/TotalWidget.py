from typing import List
from PyQt5 import QtWidgets, QtCore
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from GESAnalysis.UI.categories import common
from GESAnalysis.UI.categories.total.TotalStatWidget import TotalStatWidget
from .TotalEmission import TotalEmission


class TotalWidget(QtWidgets.QWidget, Observer):
    """ Widget use to regroup the graphs, the files opener and the stat of the category "Total"
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
        # Initialise the parent
        super(TotalWidget, self).__init__(parent)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        # Add this widget to the list of observers to update his interface
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {}     # Dictionary where the key is a file and the value is 
                              # - a boolean to indicate if the file was read
                              # - a list of warning during the reading
                              # - Year of the file
        self.__years_ind = {} # Dictionary containing the year and an index
        self.__name_ind = {}  # Dictionary with the differents categories inside the the files
        self.__data = {}      # Dictionary with the data
        
        self.__configure_data()
        
        self.__init_UI()

  
#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameters to the widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Splitter to divise the sections
        # Right : Graphs
        # Left : List of files open, Stats
        splitter = QtWidgets.QSplitter(self)
        
        # Create the left-side of the splitter
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_total_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        self.__stat_total_widget = TotalStatWidget(self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_total_widget)
        splitter_left_layout.addWidget(self.__stat_total_widget)
        splitter_left_widget.setLayout(splitter_left_layout)
        
        # Create the right-side of the splitter
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        self.__total_emission = TotalEmission(self.__controller, self.__tab_graph)
        self.__tab_graph.addTab(self.__total_emission, "Emission")
        
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        splitter.setSizes([200, 1000])

        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(splitter)
        self.setLayout(layout_principal)
        
        
#######################################################################################################
#  Configure data                                                                                     #
#######################################################################################################
    def __configure_data(self) -> None:
        """ Configure the data
        """
        ind_year = 0
        ind_name = 0
        unit_intensity = ""
        for file, data_file in self.__gesanalysis.get_data().items():
            # If the file is not in the category, we skip it
            if data_file["category"] != self.__category:
                continue
            
            # Add to the dictionary of files
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
            
            compare_columns = True # Use to compare the length of selected column below
            
            data = data_file["data"]
            
            # Get categories for emission
            name = common.get_column(data, "name")
            # If we don't find the column, put a warning
            if name is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'name' non-trouvée")
            
            # Get the carbon footprint
            intensity = common.get_column(data, "intensity")
            # If we don't find the column, put a warning
            if intensity is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'intensity' non-trouvée")
            
            # Compare the columns if they have the same number of lines
            if compare_columns and len(name) != len(intensity):
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'name' et 'intensity' n'ont pas les mêmes lignes")
                
            # If there are some warnings, we don't calculate
            if not self.__files[file]["read"]:
                continue

            # Get the unit
            unit = common.get_unit(data, "intensity")
            # If the unit is not found, put a warning
            if unit is None:
                self.__files[file]["warning"].append(f"Colonne 'intensity' n'a pas d'unité")
            else:
                unit = '/'.join(unit)
                if unit_intensity == "":
                    unit_intensity = unit
                    # If the unit is different, put a warning
                if unit != unit_intensity:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'intensity' a une unité différente")
            
            year = data_file["year"]
            
            # If there are warnings, then we read the next file
            if not self.__files[file]["read"]:
                continue
            
            # Add different categories to our dictionary
            for i in range(len(name)):
                name_val = name[i][0]
                if name_val not in self.__name_ind.keys():
                    self.__name_ind[name_val] = {"index": ind_name}
                    ind_name += 1
            
            # Same for year
            if year not in self.__years_ind.keys():
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
            
        # Create structure for data
        data_total = {}
        for name in self.__name_ind.keys():
            data_total[name] = {}
            l = [0 for i in range(len(self.__years_ind))]
            data_total[name]["data"] = l
            
        # Fill the structure
        for file, data_file in self.__files.items():
            if not data_file["read"]:
                continue
            
            data = self.__gesanalysis.get_data_from_file(file)
            
            name = common.get_column(data, "name")
            intensity = common.get_column(data, "intensity")
            year = data_file["year"]
            
            # Add value to their correct place
            for i in range(len(name)):
                name_val = name[i][0]
                intensity_val = sum(intensity[i])
                
                data_total[name_val]["data"][self.__years_ind[year]["index"]] += intensity_val
        
        self.__data["data"] = data_total    
        self.__data["unit"] = unit_intensity
        

#######################################################################################################
#  Method associated to an action                                                                     #
#######################################################################################################
    def close_files(self) -> None:
        """ Close files of this category
        """
        self.__file_total_widget.close_files()
        

#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def get_selected_files(self) -> List[str]:
        """ Return a list of files selected from the list

        Returns:
            List[str]: Files
        """
        return self.__file_total_widget.get_selected_files()

            
#######################################################################################################
#  Update widgets                                                                                     #
#######################################################################################################        
    def update(self) -> None:
        """ Update widget (from observers)
        """
        # Clear all dictionaries
        self.__data.clear()
        self.__years_ind.clear()
        self.__name_ind.clear()
        self.__files.clear()
        
        # Read and configure the data
        self.__configure_data()
        
        # update the widget (File opener, stat and graphs)
        self.__file_total_widget.update_widget(self.__files)
        self.__stat_total_widget.update_widget(self.__years_ind, self.__name_ind, self.__data)
        self.__total_emission.update_canvas(self.__name_ind, self.__years_ind, self.__data)


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
        