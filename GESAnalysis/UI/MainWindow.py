from typing import Any
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
    """ Class representing the main window
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
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.__gesanalysis = model
        self.__controller = controller
        self.__dict_categories = {}
        
        self.width = 1280
        self.height = 720
        
        self.__init_UI()
        
        
    def __init_UI(self) -> None:
        """ Initialise the UI of the window
        """
        self.setWindowTitle("GESAnalysis")
        self.resize(self.width, self.height)
        
        # Create the menu
        self.__init_menu()
        
        # Create tab widget for differents categories
        self.__tab_widget_categories = QtWidgets.QTabWidget(self)
        self.__tab_widget_categories.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        
        # Create the class for each category
        self.__create_widget_catefories("Achats", AchatsWidget)
        self.__create_widget_catefories("Déplacements domicile-travail", DeplacementWidget)
        self.__create_widget_catefories("Fluides", FluideWidget)
        self.__create_widget_catefories("Matériel Informatique", MaterielWidget)
        self.__create_widget_catefories("Missions", MissionsWidget)
        self.__create_widget_catefories("Total", TotalWidget)
        # achats_widget = AchatsWidget(self.__gesanalysis, self.__controller, "Achats", self.__tab_widget_categories)
        # deplacement_widget = DeplacementWidget(self.__gesanalysis, self.__controller, "Déplacements domicile-travail", self.__tab_widget_categories)
        # fluide_widget = FluideWidget(self.__gesanalysis, self.__controller, "Fluides", self.__tab_widget_categories)
        # materiel_widget = MaterielWidget(self.__gesanalysis, self.__controller, "Matériel Informatique", self.__tab_widget_categories)
        # missions_widget = MissionsWidget(self.__gesanalysis, self.__controller, "Missions", self.__tab_widget_categories)
        # total_widget = TotalWidget(self.__gesanalysis, self.__controller, "Total", self.__tab_widget_categories)
        
        # # Add widgets to dictionary
        # self.__dict_categories["Achats"] = {"widget": achats_widget}
        # self.__dict_categories["Déplacements domicile-travail"] = {"widget": deplacement_widget}
        # self.__dict_categories["Fluides"] = {"widget": fluide_widget}
        # self.__dict_categories["Matériel Informatique"] = {"widget": materiel_widget}
        # self.__dict_categories["Missions"] = {"widget": missions_widget}
        # self.__dict_categories["Total"] = {"widget": total_widget}
        
        # # Add differents class in the tab widget
        # self.__tab_widget_categories.addTab(achats_widget, "Achats")
        # self.__tab_widget_categories.addTab(deplacement_widget, "Déplacements domicile-travail")
        # self.__tab_widget_categories.addTab(fluide_widget, "Fluides")
        # self.__tab_widget_categories.addTab(materiel_widget, "Matériel Informatique")
        # self.__tab_widget_categories.addTab(missions_widget, "Missions")
        # self.__tab_widget_categories.addTab(total_widget, "Total")
        
        self.__tab_widget_categories.setCurrentIndex(0)
        
        self.setCentralWidget(self.__tab_widget_categories)
        
        
    def __init_menu(self) -> None:
        """ Initialise the menu of the window
        """
        menu = self.menuBar()
        
        # Create a sub menu for 'file'
        # To open, close and export file
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
        
        
    def __create_widget_catefories(self, category: str, class_category: Any) -> None:
        """ Create a widget of class 'class_category' for a category

        Args:
            category (str): Category
            class_category (Any): Class of category
        """
        category_widget = class_category(self.__gesanalysis, self.__controller, category, self.__tab_widget_categories)
        self.__dict_categories[category] = {"widget": category_widget}
        self.__tab_widget_categories.addTab(self.__dict_categories[category]["widget"], category)


    def close_files(self) -> None:
        """ Action to close a file of the current category
        """
        current_category = self.get_current_category()
        self.__dict_categories[current_category]["widget"].close_files()
        
    
    def open_file_dialog(self) -> None:
        """ Open a dialog to read a file
        """
        self.file_dialog = OpenFileDialog(self.__controller, self)
        self.file_dialog.exec()
    
    
    def export_file(self) -> None:
        """ Open a dialog to export a file.
            The user can select a file from FileOpenUI of the current category
        """
        current_category = self.get_current_category()
        selected_file = self.__dict_categories[current_category]["widget"].get_selected_files()
        self.dialog_export = ExportFileDialog(selected_file, self.__gesanalysis, self.__controller, self)
        self.dialog_export.exec()
        
    
    def open_view_data(self) -> None:
        """ When the user click on "Affichage > Données"
            Open a dialog to display the data of all the files open in the app
        """
        view_data_dialog = ViewDataDialog(self.__gesanalysis, self)
        view_data_dialog.exec()
    
    
    def get_current_category(self):
        return common.categories[self.__tab_widget_categories.currentIndex()]