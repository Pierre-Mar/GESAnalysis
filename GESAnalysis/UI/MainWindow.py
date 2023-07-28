from typing import Any, Union
from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI.OpenFileDialog import OpenFileDialog
from GESAnalysis.UI.ExportFileDialog import ExportFileDialog
from GESAnalysis.UI.ViewDataDialog import ViewDataDialog
from GESAnalysis.UI.categories.achats.AchatsWidget import AchatsWidget
from GESAnalysis.UI.categories.deplacement.DeplacementWidget import DeplacementWidget
from GESAnalysis.UI.categories.fluide.FluideWidget import FluideWidget
from GESAnalysis.UI.categories.materiel.MaterielWidget import MaterielWidget
from GESAnalysis.UI.categories.missions.MissionsWidget import MissionsWidget
from GESAnalysis.UI.categories.total.TotalWidget import TotalWidget

import GESAnalysis.UI.common as common


class MainWindow(QtWidgets.QMainWindow):
    """ Main window of the software
    """
    
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        *args,
        **kwargs
    ) -> None:
        """ Initialise the window

        Args:
            model (GESAnalysis): Model of the UI, contains the data
            controller (Controleur): Controller
        """
        # Initialise the parent class
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        
        # Dictionary where the key is a category with an index and the class associated to this category
        self.__dict_categories = {}
        self.__number_categories = 0
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI of the window
        """
        # Set parameters to this window
        self.setWindowTitle("GESAnalysis")
        self.showMaximized()
        
        # Create the menu
        self.__init_menu()
        
        # Create tab widget for differents categories
        self.__tab_widget_categories = QtWidgets.QTabWidget(self)
        self.__tab_widget_categories.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        
        # Create a tab for each category
        self.__create_widget_categories("Achats", AchatsWidget)
        self.__create_widget_categories("Déplacements domicile-travail", DeplacementWidget)
        self.__create_widget_categories("Fluides", FluideWidget)
        self.__create_widget_categories("Matériel Informatique", MaterielWidget)
        self.__create_widget_categories("Missions", MissionsWidget)
        self.__create_widget_categories("Total", TotalWidget)
        
        # Set the current tab to the first tab (Achats)
        self.__tab_widget_categories.setCurrentIndex(0)
        
        self.setCentralWidget(self.__tab_widget_categories)
        
        
    def __init_menu(self) -> None:
        """ Initialise the menu of the window
        """
        menu = self.menuBar()
        
        # Create a sub menu for 'file'
        # Open, close and export file
        file_menu = menu.addMenu("Fichier")
        
        # Create action to open file
        open_file_action = QtWidgets.QAction("Ouvrir", self)
        open_file_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_file_action)
        
        # Create action to close file
        close_file_action = QtWidgets.QAction("Fermer", self)
        close_file_action.triggered.connect(self.close_files)
        file_menu.addAction(close_file_action)
        
        file_menu.addSeparator()
        
        # Create action to export file
        export_action = QtWidgets.QAction("Exporter", self)
        export_action.triggered.connect(self.export_file)
        file_menu.addAction(export_action)
        
        # Create a sub menu for 'Affichage'
        # to display the data (file open)
        display_menu = menu.addMenu("Affichage")
        
        # Create action to display data
        display_data_action = QtWidgets.QAction("Données", self)
        display_data_action.triggered.connect(self.open_view_data)
        display_menu.addAction(display_data_action)
        
        
    def __create_widget_categories(self, category: str, class_category: Any) -> None:
        """ Create a widget of class 'class_category' for a category

        Args:
            category (str): Category
            class_category (Any): Class associated to the category
        """
        category_widget = class_category(self.__gesanalysis, self.__controller, category, self.__tab_widget_categories)
        self.__dict_categories[category] = {"widget": category_widget, "index": self.__number_categories}
        self.__tab_widget_categories.addTab(self.__dict_categories[category]["widget"], category)
        self.__number_categories += 1


#######################################################################################################
#  Methods connected to an action                                                                     #
#######################################################################################################
    def close_files(self) -> None:
        """ Close files of the current category
        """
        current_category = self.get_current_category()
        # If the category is not found, no need to continue
        if current_category is None:
            return
        self.__dict_categories[current_category]["widget"].close_files()
        
    
    def open_file_dialog(self) -> None:
        """ Open a dialog to read a file
        """
        self.file_dialog = OpenFileDialog(self.__controller, self)
        if self.file_dialog.exec_():
            category = self.file_dialog.selected_category
            self.__tab_widget_categories.setCurrentIndex(self.__dict_categories[category]["index"])
    
    
    def export_file(self) -> None:
        """ Open a dialog to export a file.
            The user can select a file from FileOpenUI of the current category
        """
        current_category = self.get_current_category()
        # If the category is not found, no need to continue
        if current_category is None:
            return
        selected_file = self.__dict_categories[current_category]["widget"].get_selected_files()
        self.dialog_export = ExportFileDialog(selected_file, self.__gesanalysis, self.__controller, self)
        self.dialog_export.exec()
        
    
    def open_view_data(self) -> None:
        """ Open a dialog to display the data of all the files open in the app
        """
        view_data_dialog = ViewDataDialog(self.__gesanalysis, self)
        view_data_dialog.exec()
    

#######################################################################################################
#  Getters                                                                                             #
#######################################################################################################
    def get_current_category(self) -> Union[str, None]:
        """ Return the current category of the current tab

        Returns:
            Union[str, None]: Category if it's found, else None
        """
        current_tab_ind = self.__tab_widget_categories.currentIndex()
        for category, data_category in self.__dict_categories.items():
            if data_category["index"] == current_tab_ind:
                return category
        return None
