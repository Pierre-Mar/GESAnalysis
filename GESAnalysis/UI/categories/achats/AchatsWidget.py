from typing import List
from PyQt5 import QtWidgets, QtCore
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from GESAnalysis.UI.categories import common
from GESAnalysis.UI.categories.achats.KeyAmount import KeyAmount


class AchatsWidget(QtWidgets.QWidget, Observer):
    """ Widget use to regroup the graphs, the files opener and the stats of the category "Achats"
    """
    
    # Column to get the data from the files
    column_nacres_key = ["code", "Code NACRES"]
    column_amount = ["amount", "Montant"]
    
    
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
        super(AchatsWidget, self).__init__(parent)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        # Add this widget to the list of observers to update his interface
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {}     # Dictionary where the key is the file in 'category' and a bool if it's read or not
        self.__years_ind = {} # Dictionary containing the year and the index
        self.__data = {}      # Dictionary containing the data with the NACRES key and the amount, and the unit of the amount
                
        self.__configure_data()
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI for "Achats"
        """
        # Set parameter of this widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Splitter to divide the sections
        splitter = QtWidgets.QSplitter(self)
        
        # Widget for left-splitter (file open + stats)
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_achats_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_achats_widget)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        self.__key_amount = KeyAmount(self.__tab_graph)
        self.__tab_graph.addTab(self.__key_amount, "Montant")
        
        # Add components to the splitter
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
        """ Configure data
        """
        unit_amount = ""
        ind_year = 0
        for file, data_file in self.__gesanalysis.get_data().items():
            if data_file["category"] != self.__category:
                continue
            
            # Add file to self.__files and set bool
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
            
            data = data_file["data"]
            
            compare_columns = True
            
            # Get the data for the NACRES key 
            nacres_keys = common.get_data_from_columns(data, self.column_nacres_key)
            if nacres_keys is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne pour le code NACRES non-trouvée")
            
            # Same with the amount
            amount = common.get_data_from_columns(data, self.column_amount)
            if amount is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne pour le montant non-trouvée")
            
            # Compare the columns between the NACRES key and the amount
            if compare_columns and len(nacres_keys) != len(amount):
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append("Nombre de lignes différent entre le code NACRES et le montant")
                
            # Get the unit of amount
            unit = common.get_unit_from_columns(data, self.column_amount)
            if unit is None:
                self.__files[file]["warning"].append(f"Colonne 'Montant' n'a pas d'unité")
            else:
                unit = "/".join(unit)
                if unit_amount == "":
                    unit_amount = unit
                if unit != unit_amount:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'Montant' a une unité différente")
            
            # No need to continue if there are problems
            if not self.__files[file]["read"]:
                continue
            
            # Check if all the NACRES key is correct
            nacres_key_correct = True
            for key_line in nacres_keys:
                for key in key_line:
                    nacres_key = key.upper()
                    if not self.__check_NACRES_key(nacres_key):
                        nacres_key_correct = False
                        break
                
                if not nacres_key_correct:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append("Des codes NACRES sont incorrectes")
                    break
            
            year = data_file["year"]
            if year not in self.__years_ind.keys():
                self.__years_ind[year] = {"index": ind_year}
                ind_year += 1
                
        # Create structure for data
        data_achats = {}
        for year in self.__years_ind.keys():
            data_achats[year] = []
            
        # Fill the structure
        for file, data_file in self.__files.items():
            if not data_file["read"]:
                continue
            
            data = self.__gesanalysis.get_data_from_file(file)
            nacres_keys = common.get_data_from_columns(data, self.column_nacres_key)
            amount = common.get_data_from_columns(data, self.column_amount)
            year = data_file["year"]
            
            for i in range(len(nacres_keys)):
                for j in range(len(nacres_keys[i])):
                    data_achats[year].append((nacres_keys[i][j], sum(amount[i])))
        
        self.__data["data"] = data_achats
        self.__data["unit"] = unit_amount
            
    
    def __check_NACRES_key(self, key: str) -> bool:
        """ Check if a NACRES key is correct. Use a parsing describe below:
            A -> pB
            B -> pC
            C -> .D
            C -> qE
            D -> qE
            E -> qF
            F -> True
            
            p = { 'A', ..., 'Z' }
            q = { '0', ..., '9' }

        Args:
            key (str): NACRES key

        Returns:
            bool: True if the key is correct or false
        """
        if len(key) == 4 or len(key) == 5:
            return self.__A(key, 0)
        return False
    
    #-- Methods uses for the parsing --#
    def __A(self, key: str, index: int) -> bool:
        if 'A' <= key[index] and key[index] <= 'Z':
            return self.__B(key, index+1)
        return False
    
    def __B(self, key: str, index: int) -> bool:
        if 'A' <= key[index] and key[index] <= 'Z':
            return self.__C(key, index+1)
        return False
    
    def __C(self, key: str, index: int) -> bool:
        if key[index] == '.':
            return self.__D(key, index+1)
        elif '0' <= key[index] and key[index] <= '9':
            return self.__E(key, index+1)
        return False
    
    def __D(self, key: str, index: int) -> bool:
        if '0' <= key[index] and key[index] <= '9':
            return self.__E(key, index+1)
        return False
    
    def __E(self, key: str, index: int) -> bool:
        if '0' <= key[index] and key[index] <= '9':
            return self.__F()
        return False
    
    def __F(self) -> bool:
        return True
        
                        
#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def close_files(self) -> None:
        """ Close files from this widget
        """
        self.__file_achats_widget.close_files()
    

#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def get_selected_files(self) -> List[str]:
        """ Get selected files from FileOpenUI

        Returns:
            List[str]: List of file name's
        """
        return self.__file_achats_widget.get_selected_files()
            

#######################################################################################################
#  Update widgets                                                                                     #
#######################################################################################################        
    def update(self):
        """ Update this widget (from observers)
        """
        self.__files.clear()
        self.__years_ind.clear()
        self.__data.clear()
        
        self.__configure_data()
        
        self.__file_achats_widget.update_widget(self.__files)
        
        self.__key_amount.update_canvas(self.__years_ind, self.__data)


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
