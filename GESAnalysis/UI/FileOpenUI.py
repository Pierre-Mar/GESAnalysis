from PyQt5 import QtWidgets, QtCore
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.PATTERNS.Observer import Observer
from typing import List
from functools import partial
from GESAnalysis.UI.ChangeYearCateDialog import ChangeYearCateDialog

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
        self.__list_widget.installEventFilter(self)

        # display items (here file)
        file_open = self.__gesanalysis.get_file_open()
        for file in file_open:
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            self.__list_widget.addItem(item)
            
    
    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.ContextMenu and source is self.__list_widget:
            menu = QtWidgets.QMenu()
            
            # Action to change the year and the caegory of the file
            change_year_category_action = QtWidgets.QAction("Modifier")
            change_year_category_action.triggered.connect(partial(self.__change_year_category, source, event))
            menu.addAction(change_year_category_action)
            
            # Action to close files
            close_file_action = QtWidgets.QAction("Fermer")
            close_file_action.triggered.connect(self.close_files)
            menu.addAction(close_file_action)
            
            menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)
            
            
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


    def get_selected_files(self) -> List[str]:
        """ Returns a list of selected files

        Returns:
            List(str): selected files
        """
        return [item.text() for item in self.__list_widget.selectedItems()]
    
    
    def __change_year_category(self, source: QtCore.QObject, event: QtCore.QEvent) -> None:
        item = source.itemAt(event.pos())
        if not isinstance(item, QtWidgets.QListWidgetItem):
            return
        dialog = ChangeYearCateDialog(item.text(), self.__gesanalysis, self.__controller, self)
        dialog.exec()
