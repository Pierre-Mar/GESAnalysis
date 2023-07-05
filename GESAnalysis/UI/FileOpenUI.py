from PyQt5 import QtWidgets, QtCore, QtGui
from typing import List, Dict, Union
from functools import partial
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.ChangeYearCateDialog import ChangeYearCateDialog

class FileOpenUI(QtWidgets.QWidget):
    """ Widget containing all the name of file who are currently read for a category
    """
    
    def __init__(
        self,
        files_category: Dict[str, Union[bool, List[str], str]],
        category: str,
        controller: Controleur,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the widget

        Args:
            model (GESAnalysis): Model of the UI, contains the data
            controller (Controleur): Controller
            category (str): Category of the opener
            parent (QtWidgets.QWidget | None, optional): Parent to this dialog. Defaults to ....
        """
        super(FileOpenUI, self).__init__(parent)
        
        self.__files_category = files_category
        self.__controller = controller
        self.__category = category
        
        self.__init_UI()

  
#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI of the widget
        """
        # Create list view to display the files who are open
        self.__list_widget = QtWidgets.QListWidget(self)
        self.__list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.__list_widget.installEventFilter(self)
        
        icon_warning = QtGui.QIcon("GESAnalysis/UI/assets/exclamation.png")

        # display items (here file)
        for file, data_file in self.__files_category.items():
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            if not data_file["read"]:
                # Add icon because the file was not read
                item.setIcon(icon_warning)
                item.setToolTip(";".join(data_file["warning"]))
            self.__list_widget.addItem(item)


#######################################################################################################
#  Events with mouse                                                                                  #
#######################################################################################################
    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """ Event filter

        Args:
            source (QtCore.QObject): Object where the mouse is
            event (QtCore.QEvent): Event occurs by the mouse

        Returns:
            bool: Bool
        """
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
    
    
    def __change_year_category(self, source: QtCore.QObject, event: QtCore.QEvent) -> None:
        """ Change the year and the category of the file

        Args:
            source (QtCore.QObject): Object where the mouse is
            event (QtCore.QEvent): Event (needed to get the position of the click)
        """
        item = source.itemAt(event.pos())
        if not isinstance(item, QtWidgets.QListWidgetItem):
            return
        file_selected = item.text()
        year_file = self.__files_category[file_selected]["year"]
        dialog = ChangeYearCateDialog(file_selected, year_file, self.__category, self.__controller, self)
        dialog.exec()
            
            
    def close_files(self) -> None:
        """ Send a notification to the controller to close some files
        """
        self.__controller.close_files(self.get_selected_files(), self.__category)
    

#######################################################################################################
#  Update (from Widget)                                                                            #
#######################################################################################################
    def update_widget(self, files_category) -> None:
        """ Update the widget (From observers)
        """
        # Remove all the items
        self.__list_widget.clear()
        
        self.__files_category = files_category
        
        # Add others items
        icon_warning = QtGui.QIcon("GESAnalysis/UI/assets/exclamation.png")
        for file, data_file in self.__files_category.items():
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            if not data_file["read"]:
                # Add icon because the file was not read
                item.setIcon(icon_warning)
                item.setToolTip("\n".join(data_file["warning"]))
            self.__list_widget.addItem(item)


#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def get_selected_files(self) -> List[str]:
        """ Returns a list of selected files

        Returns:
            List(str): selected files
        """
        return [item.text() for item in self.__list_widget.selectedItems()]
