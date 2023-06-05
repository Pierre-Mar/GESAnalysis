from PyQt5.QtWidgets import QApplication
from GESAnalysis.FC.ReaderData import ReaderData
from GESAnalysis.UI import MainWindow

def run():
    r = ReaderData()
    l = []
    
    d = r.read_file("/home/pierre/Documents/python/files_gesanalyser/files/2019_missions.txt")
    l.append((d, '2019'))
    l.append((d, '2020'))
    app = QApplication([])
    
    window = MainWindow.MainWindow(l)
    window.show()
    
    app.exec()

if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()