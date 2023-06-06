from PyQt5 import QtWidgets
from GESAnalysis.FC.PATTERNS.Observer import Observer



class FileOpenUI(QtWidgets.QWidget, Observer):
    
    def __init__(self, model, controller, parent) -> None:
        super(FileOpenUI, self).__init__(parent)
        
        self.__parent = parent
        
        self.__gesanalysis = model
        self.__controller = controller
        
        self.__gesanalysis.add_observer(self)
        
        self.__init_UI()
        
    
    def __init_UI(self):
        # Create list view to display the files who are open
        self.__list_widget = QtWidgets.QListWidget(self)
        self.__list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # display items (here file)
        file_open = self.__gesanalysis.get_file_open()
        for file in file_open:
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            self.__list_widget.addItem(item)
            
            
    def get_selected_files(self):
        return [item.text() for item in self.__list_widget.selectedItems()]
