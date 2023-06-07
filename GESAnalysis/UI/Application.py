from PyQt5.QtWidgets import QApplication
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI.MainWindow import MainWindow


class Application:
    """ Main application of the tool
    """
    
    def __init__(self, model: GESAnalysis, controller: Controleur) -> None:
        """ Initialise the application

        Args:
            model (GESAnalysis): Model of the UI, contains the data
            controller (Controleur): Controller
        """
        self.__app = QApplication([])
        self.__main_window = MainWindow(model, controller)
    
    
    def run(self) -> None:
        """ Start the application
        """
        self.__main_window.show()
        self.__app.exec()