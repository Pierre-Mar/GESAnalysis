from typing import List
from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI.FileOpenUI import FileOpenUI


class MaterielWidget(QtWidgets.QWidget):
    
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        category: str,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        super(MaterielWidget, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
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
        self.__file_depl_widget = FileOpenUI(self.__gesanalysis, self.__controller, self.__category, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_depl_widget)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        # TODO : Add graph for "Deplacement" here
        
        # Add components to the splitter
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        
        layout_principal.addWidget(splitter)
        
        
    def close_files(self) -> None:
        self.__file_depl_widget.close_files()
        
        
    def get_selected_files(self) -> List[str]:
        return self.__file_depl_widget.get_selected_files()
        