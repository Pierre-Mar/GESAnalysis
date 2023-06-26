from PyQt5 import QtWidgets, QtCore
from typing import List, Union


class ViewDataDialog(QtWidgets.QDialog):
    """ Open a dialog to display the data of all the files open in the model
    """
    
    def __init__(self, model, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            model (GESAnalysis): Model
            parent (QtWidgets.QWidget | None, optional): Parent of this dialog. Defaults to ....
        """
        super(ViewDataDialog, self).__init__(parent)
        
        # Set the model
        self.__gesanalysis = model
        
        # Create UI
        self.__init_UI()
    
    
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameters to the dialog
        self.setWindowTitle("Affichage - Données")
        self.resize(900, 600)
        
        # Create the layout for the dialog
        principal_layout = QtWidgets.QHBoxLayout(self)
        
        # Get the file who are opened in the model
        file_open = self.__gesanalysis.get_file_open()
        
        # To display all the data, we create a tab for each file
        tab_widget = QtWidgets.QTabWidget(self)
        for file in file_open:
            # For each file, create a widget and his layout to display the data from the file
            file_widget = QtWidgets.QWidget()
            file_layout = QtWidgets.QHBoxLayout(file_widget)
            
            # Create the table widget to display the data of the file
            table_data_widget = QtWidgets.QTableWidget(file_widget)

            # Get the data of the file
            data_file = self.__gesanalysis.get_data_from_file(file)
            
            # Set columns (number and labels)
            label_col_file = list(data_file.keys())
            table_data_widget.setColumnCount(len(label_col_file))
            table_data_widget.setHorizontalHeaderLabels(label_col_file)
            
            # Set number of rows
            table_data_widget.setRowCount(len(data_file[label_col_file[0]]["data"]))
            
            # Fill the table with the data
            for column_ind, column in enumerate(label_col_file):
                for data_ind, data in enumerate(data_file[column]["data"]):
                    # Transform the data to string
                    data_str = self.__transform_data_to_str(data, data_file[column]["type"])
                    item_data = QtWidgets.QTableWidgetItem(data_str)
                    # Remove flags to edit the item
                    item_data.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                    table_data_widget.setItem(data_ind, column_ind, item_data)
                    
            # Add the table to the widget
            file_layout.addWidget(table_data_widget)
            
            # Add this widget because it's the tab
            tab_widget.addTab(file_widget, file)

        # Add the principal widget to the dialog
        principal_layout.addWidget(tab_widget)
        
        
    def __transform_data_to_str(self, data_list: List[Union[bool, int, float, str]], type_data: type) -> str:
        """ Transform the elements in data_list to a string

        Args:
            data_list (List[Union[bool, int, float, str]]): List with elements
            type_data (type): Type of these elements

        Returns:
            str: String where the elements are separated by ','
        """
        data_list_to_str = data_list
        if not type_data == str:
            # Transform all elements to string
            data_list_to_str = map(str, data_list_to_str)
        return ",".join(data_list_to_str)
            
        