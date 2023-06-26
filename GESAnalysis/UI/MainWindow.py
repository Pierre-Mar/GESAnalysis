from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from GESAnalysis.UI.OpenFileDialog import OpenFileDialog
from GESAnalysis.UI.ExportFileDialog import ExportFileDialog
from GESAnalysis.UI.ViewDataDialog import ViewDataDialog
from GESAnalysis.UI.plot.missions.DistanceMode import DistanceMode
from GESAnalysis.UI.plot.missions.EmissionMode import EmissionMode


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
        
        splitter = QtWidgets.QSplitter(self)
        
        # Create widgets        
        self.file_open_UI = FileOpenUI(self.__gesanalysis, self.__controller, splitter)
        
        self.tab_graphs_widget = QtWidgets.QTabWidget(splitter)
        self.distance_canvas = DistanceMode(self.__gesanalysis, self.tab_graphs_widget)
        self.emission_canvas = EmissionMode(self.__gesanalysis, self.tab_graphs_widget)
        self.tab_graphs_widget.addTab(self.distance_canvas, "Distance")
        self.tab_graphs_widget.addTab(self.emission_canvas, "Emissions")

        # Set layout
        splitter.addWidget(self.file_open_UI)
        splitter.addWidget(self.tab_graphs_widget)
        
        self.setCentralWidget(splitter)
        
        
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
        """ Action to close a file
        """
        self.file_open_UI.close_files()
        
    
    def open_file_dialog(self) -> None:
        """ Open a dialog to read a file
        """
        self.file_dialog = OpenFileDialog(self.__controller, self)
        self.file_dialog.exec()
    
    
    def export_file(self) -> None:
        """ Open a dialog to export a file.
            The user can select a file from FileOpenUI
        """
        selected_file = self.file_open_UI.get_selected_files()
        self.dialog_export = ExportFileDialog(selected_file, self.__gesanalysis, self.__controller, self)
        self.dialog_export.exec()
        
    
    def open_view_data(self) -> None:
        """ When the user click on "Affichage > Données"
            Open a dialog to display the data of all the files open in the app
        """
        view_data_dialog = ViewDataDialog(self.__gesanalysis, self)
        view_data_dialog.exec()
        