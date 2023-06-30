from typing import List
from PyQt5 import QtWidgets
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from .TotalEmission import TotalEmission


class TotalWidget(QtWidgets.QWidget):
    
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
        
        self.__init_UI()
        
    
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        layout_principal = QtWidgets.QHBoxLayout(self)
        splitter = QtWidgets.QSplitter(self)
        
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_total_widget = FileOpenUI(self.__gesanalysis, self.__controller, self.__category, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_total_widget)
        
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        self.__total_emission = TotalEmission(self.__gesanalysis, self.__controller, self.__category, self.__tab_graph)
        self.__tab_graph.addTab(self.__total_emission, "Emission")
        
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        
        layout_principal.addWidget(splitter)
        
    
    def close_files(self) -> None:
        self.__file_total_widget.close_files()
        
    
    def get_selected_files(self) -> List[str]:
        return self.__file_total_widget.get_selected_files()