from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.PATTERNS.Observer import Observer



class FileOpenUI(QtWidgets.QWidget, Observer):
    """ Widget containing all the name of file who are currently read
    """
    
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the widget

        Args:
            model (GESAnalysis): Model of the UI, contains the data
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this dialog. Defaults to ....
        """
        super(FileOpenUI, self).__init__(parent)
                
        self.__gesanalysis = model
        self.__controller = controller
        
        self.__gesanalysis.add_observer(self)
        
        self.__init_UI()
        
    
    def __init_UI(self) -> None:
        """ Initialise the UI of the widget
        """
        # Create list view to display the files who are open
        self.__list_widget = QtWidgets.QListWidget(self)
        self.__list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # display items (here file)
        file_open = self.__gesanalysis.get_file_open()
        for file in file_open:
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            self.__list_widget.addItem(item)
            
            
    def close_files(self) -> None:
        """ Send a notification to the controller to close some files
        """
        remove_items = [item.text() for item in self.__list_widget.selectedItems()]
        self.__controller.close_files(remove_items)
    
    
    def update(self) -> None:
        """ Update the widget (From observers)
        """
        # Remove all the items
        self.__list_widget.clear()
        
        # Add others items
        for file in self.__gesanalysis.get_file_open():
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            self.__list_widget.addItem(item)
