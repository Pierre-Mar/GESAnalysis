from PyQt5 import QtWidgets
from GESAnalysis.UI.FileOpenUI import FileOpenUI
from GESAnalysis.UI.OpenFileDialog import OpenFileDialog
from GESAnalysis.UI.plot.DistanceMode import DistanceMode


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, model, controller, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.__gesanalysis = model
        self.__controller = controller
        
        self.width = 1280
        self.height = 720
        
        self.__init_UI()
        
        
    def __init_UI(self):
        self.setWindowTitle("GESAnalysis")
        self.resize(self.width, self.height)
        
        # Create the menu
        self.__init_menu()
        
        splitter = QtWidgets.QSplitter(self)
        
        # Create widgets        
        self.file_open_UI = FileOpenUI(self.__gesanalysis, self.__controller, splitter)
        self.distance_canvas = DistanceMode(self.__gesanalysis, self.__controller, splitter)

        # Set layout
        splitter.addWidget(self.file_open_UI)
        splitter.addWidget(self.distance_canvas)
        
        self.setCentralWidget(splitter)
        
        
    def __init_menu(self):
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
        file_menu.addAction(export_action)
    
    
    def close_files(self):
        self.file_open_UI.close_files()
        
    
    def open_file_dialog(self):
        self.file_dialog = OpenFileDialog(self.__gesanalysis, self.__controller, self)
        self.file_dialog.exec()