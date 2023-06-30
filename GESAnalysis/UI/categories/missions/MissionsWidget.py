from typing import List

from PyQt5 import QtWidgets
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from .DistanceMode import DistanceMode
from .EmissionMode import EmissionMode


class MissionsWidget(QtWidgets.QWidget):
     
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
        super(MissionsWidget, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        self.__init_UI()
        
        
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        layout_principal = QtWidgets.QHBoxLayout(self)
        splitter = QtWidgets.QSplitter(self)
        
        # Widget for left-splitter (file open + stats)
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_mission_widget = FileOpenUI(self.__gesanalysis, self.__controller, self.__category, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_mission_widget)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graphs_widget = QtWidgets.QTabWidget(splitter)
        self.__distance_canvas = DistanceMode(self.__gesanalysis, self.__category, self.__tab_graphs_widget)
        self.__emissions_canvas = EmissionMode(self.__gesanalysis, self.__category, self.__tab_graphs_widget)
        self.__tab_graphs_widget.addTab(self.__distance_canvas, "Distance")
        self.__tab_graphs_widget.addTab(self.__emissions_canvas, "Emission")
        
        # Add both widgets to splitter
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graphs_widget)
        
        layout_principal.addWidget(splitter)
        
        
    def close_files(self) -> None:
        """ Close files from this widget
        """
        self.__file_mission_widget.close_files()
        
        
    def get_selected_files(self) -> List[str]:
        """ Get selected files from FileOpenUI

        Returns:
            List[str]: List of file names's
        """
        return self.__file_mission_widget.get_selected_files()
