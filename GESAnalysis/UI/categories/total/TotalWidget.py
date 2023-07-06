from typing import List
from PyQt5 import QtWidgets
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from GESAnalysis.UI.categories import common
from .TotalEmission import TotalEmission


class TotalWidget(QtWidgets.QWidget, Observer):
    
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
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        super(TotalWidget, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {}
        self.__years_ind = {}
        self.__name_ind = {}
        self.__data = {}
        
        self.__configure_data()
        
        self.__init_UI()
        
    
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        layout_principal = QtWidgets.QHBoxLayout(self)
        splitter = QtWidgets.QSplitter(self)
        
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_total_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_total_widget)
        
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        self.__total_emission = TotalEmission(self.__tab_graph)
        self.__tab_graph.addTab(self.__total_emission, "Emission")
        
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        
        layout_principal.addWidget(splitter)
        
    
    def close_files(self) -> None:
        self.__file_total_widget.close_files()
        
    
    def get_selected_files(self) -> List[str]:
        return self.__file_total_widget.get_selected_files()
    
    def __configure_data(self):
        ind_year = 0
        ind_name = 0
        unit_intensity = ""
        for file, data_file in self.__gesanalysis.get_data().items():
            if data_file["category"] != self.__category:
                continue
            
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
            
            compare_columns = True
            
            data = data_file["data"]
            
            name = common.get_column(data, "name")
            if name is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'name' non-trouvée")
                
            intensity = common.get_column(data, "intensity")
            if name is None:
                compare_columns = False
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'intensity' non-trouvée")
                
            if not compare_columns or len(name) != len(intensity):
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'name' et 'intensity' n'ont pas les mêmes lignes")

            unit = common.get_unit(data, "intensity")
            if unit is None:
                self.__files[file]["read"] = False
                self.__files[file]["warning"].append(f"Colonne 'intensity' n'a pas d'unité")
            else:
                unit = '/'.join(unit)
                if unit_intensity == "":
                    unit_intensity = unit
                if unit != unit_intensity:
                    self.__files[file]["read"] = False
                    self.__files[file]["warning"].append(f"Colonne 'intensity' a une unité différente")
            
            year = data_file["year"]
            
            if not self.__files[file]["read"]:
                continue
            
            for i in range(len(name)):
                name_val = name[i][0]
                if name_val not in self.__name_ind.keys():
                    self.__name_ind[name_val] = {"index": ind_name}
                    ind_name += 1
                    
            self.__years_ind[year] = {"index": ind_year}
            ind_year += 1
            
        # Create structure
        for name in self.__name_ind.keys():
            self.__data[name] = {}
            l = [0 for i in range(len(self.__years_ind))]
            self.__data[name]["data"] = l
            
        # Fill the structure
        for file, data_file in self.__files.items():
            if not data_file["read"]:
                continue
            
            data = self.__gesanalysis.get_data_from_file(file)
            
            name = common.get_column(data, "name")
            intensity = common.get_column(data, "intensity")
            year = data_file["year"]
            
            for i in range(len(name)):
                name_val = name[i][0]
                intensity_val = sum(intensity[i])
                
                self.__data[name_val]["data"][self.__years_ind[year]["index"]] += intensity_val
                
            
    def update(self):
        self.__data.clear()
        self.__years_ind.clear()
        self.__name_ind.clear()
        self.__files.clear()
        
        self.__configure_data()
        
        self.__file_total_widget.update_widget(self.__files)
        
        self.__total_emission.update_canvas(self.__name_ind, self.__years_ind, self.__data)
        