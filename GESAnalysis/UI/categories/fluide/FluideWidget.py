from typing import List
from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI


class FluideWidget(QtWidgets.QWidget, Observer):
    
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        category: str,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        super(FluideWidget, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {}
        
        self.__configure_data()
        
        self.__init_UI()
        
        
    def __init_UI(self):
        """ Initialise the UI for "Deplacement"
        """
        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        
        splitter = QtWidgets.QSplitter(self)
        
        # Widget for left-splitter (file open + stats)
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_fluide_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_fluide_widget)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        # TODO : Add graph for "Deplacement" here
        
        # Add components to the splitter
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        
        layout_principal.addWidget(splitter)
        
        
    def close_files(self) -> None:
        self.__file_fluide_widget.close_files()
        
        
    def get_selected_files(self) -> List[str]:
        return self.__file_fluide_widget.get_selected_files()
    
    def __configure_data(self):
        for file, data_file in self.__gesanalysis.get_data().items():
            if data_file["category"] != self.__category:
                continue
            
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
            
            
    def update(self):
        self.__files.clear()
        
        self.__configure_data()
        
        self.__file_fluide_widget.update_widget(self.__files)
        