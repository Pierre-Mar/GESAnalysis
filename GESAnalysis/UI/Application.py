from PyQt5.QtWidgets import QApplication
from GESAnalysis.UI.MainWindow import MainWindow
class Application:
    
    def __init__(self, model, controller) -> None:        
        self.__app = QApplication([])
        self.__main_window = MainWindow(model, controller)
    
    
    def run(self):
        self.__main_window.show()
        self.__app.exec()