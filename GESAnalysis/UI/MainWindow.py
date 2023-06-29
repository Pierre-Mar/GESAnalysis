from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI.OpenFileDialog import OpenFileDialog
from GESAnalysis.UI.ExportFileDialog import ExportFileDialog
from GESAnalysis.UI.ViewDataDialog import ViewDataDialog
from GESAnalysis.UI.categories.missions.MissionsWidget import MissionsWidget

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
        # TODO : variable with "todo" need to be define
        todo_achats = QtWidgets.QWidget(self.__tab_widget_categories)
        todo_deplacement = QtWidgets.QWidget(self.__tab_widget_categories)
        todo_fluide = QtWidgets.QWidget(self.__tab_widget_categories)
        todo_materiel = QtWidgets.QWidget(self.__tab_widget_categories)
        self.__missions_widget = MissionsWidget(self.__gesanalysis, self.__controller, self.__tab_widget_categories)
        todo_total = QtWidgets.QWidget(self.__tab_widget_categories)
        
        # Add widgets to dictionary
        self.__dict_categories["Achats"] = {"widget": todo_achats}
        self.__dict_categories["Déplacements domicile-travail"] = {"widget": todo_deplacement}
        self.__dict_categories["Fluides"] = {"widget": todo_fluide}
        self.__dict_categories["Matériel Informatique"] = {"widget": todo_materiel}
        self.__dict_categories["Missions"] = {"widget": self.__missions_widget}
        self.__dict_categories["Total"] = {"widget": todo_total}
        
        # Add differents class in the tab widget
        self.__tab_widget_categories.addTab(todo_achats, "Achats")
        self.__tab_widget_categories.addTab(todo_deplacement, "Déplacements domicile-travail")
        self.__tab_widget_categories.addTab(todo_fluide, "Fluides")
        self.__tab_widget_categories.addTab(todo_materiel, "Matériel Informatique")
        self.__tab_widget_categories.addTab(self.__missions_widget, "Missions")
        self.__tab_widget_categories.addTab(todo_total, "Total")
        
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