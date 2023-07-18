from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.ExportStatDialog import ExportStatDialog


class TotalStatWidget(QtWidgets.QWidget):
    """ Widget to display the stat of the files from "Total"
    """
    
    def __init__(self, controller: Controleur, parent: QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            controller (Controleur): Controller
            parent (QWidget | None, optional): Parent to this widget. Defaults to ....
        """
        # Initialise the parent class
        super(TotalStatWidget, self).__init__(parent)
        
        # Set parameter to attribute
        self.__controller = controller

        # Data structure
        self.__years_dict = {}     # Dictionary of year
        self.__name_dict = {}      # Dictionary of category
        self.__data_dict = {}      # Dictionary of data
        self.__column_stats = []   # Header columns table
        self.__name_stat_list = [] # Header rows table

        # Create the widget
        self.__combobox_year = QtWidgets.QComboBox(self)                    # Combobox to choose the year to display the stat
        self.__tab_stats = QtWidgets.QTableWidget(self)                     # Table containing the stat
        self.__export_stat_button = QtWidgets.QPushButton("Exporter", self) # Button to export the table

        # Boolean use to fill or not the table
        self.__can_fill = False

        self.__init_UI()

        self.__construct_tab()


#######################################################################################################
#  Initialise UI                                                                                      #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameter to this widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Label : Statistiques
        label = QtWidgets.QLabel(self)
        label.setText("Statistiques")
        label.setFixedHeight(20)

        # Add different years to the combobox
        self.__combobox_year.addItems(self.__years_dict.keys())
        
        # Connect actions
        self.__combobox_year.currentTextChanged.connect(self.__refill_table)
        self.__export_stat_button.clicked.connect(self.__open_dialog_export_stat)
        # If there are no data, we hide some widgets
        if len(self.__years_dict.keys()) == 0:
            self.__combobox_year.hide()
            self.__export_stat_button.hide()

        # Layout of this widget
        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.setSpacing(0)
        layout_principal.addWidget(label, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        layout_principal.addWidget(self.__combobox_year)
        layout_principal.addWidget(self.__tab_stats)
        layout_principal.addWidget(self.__export_stat_button)
        self.setLayout(layout_principal)


#######################################################################################################
#  Methods associated to the table                                                                    #
#######################################################################################################
    def __construct_tab(self) -> None:
        """ Initialise and set the header for columns and rows of the table
        """
        self.__column_stats = ["Empreinte carbone"] if len(self.__name_dict.keys()) > 0 else []
        self.__name_stat_list = list(self.__name_dict.keys()) + (["total"] if len(self.__name_dict.keys()) > 0 else [])

        self.__tab_stats.setRowCount(len(self.__name_stat_list))
        self.__tab_stats.setColumnCount(len(self.__column_stats))
        self.__tab_stats.setVerticalHeaderLabels(self.__name_stat_list)
        self.__tab_stats.setHorizontalHeaderLabels(self.__column_stats)

        self.__can_fill = True
        self.__fill_table()


    def __fill_table(self) -> None:
        """ Fill the table
        """
        # if there are no stats, return
        if len(self.__column_stats) == 0 or len(self.__name_stat_list) == 0:
            return
        
        # Clear the table in case of the table have some stats
        self.__tab_stats.clearContents()
        
        # Get the selected year
        selected_year = self.__combobox_year.currentText()

        total = 0
        # Get the index of the year
        index_year = self.__years_dict[selected_year]["index"]
        # Fill each column by a stat
        for name_ind, name in enumerate(self.__name_stat_list):
            if name == 'total':
                data = total
            else:
                data = self.__data_dict[name]["data"][index_year]

            data_str = str(data)
            data_item = QtWidgets.QTableWidgetItem(data_str)
            data_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.__tab_stats.setItem(name_ind, 0, data_item)

            total += data


#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def __refill_table(self) -> None:
        """ Refill the table if the user change the year (from the combobox)
        """
        if self.__can_fill:
            self.__fill_table()
            
    
    def __open_dialog_export_stat(self) -> None:
        """ Open a dialog to export the table of stat
        """
        # Get the headers
        header_columns = self.__column_stats
        header_rows = self.__name_stat_list
        
        # Configure data to export it
        data = []
        for row in range(len(header_rows)):
            l = []
            for col in range(len(header_columns)):
                item = self.__tab_stats.item(row, col)
                l.append(item.text())
            data.append(l)
        
        # open and execute the dialog
        export_dialog = ExportStatDialog(data, header_columns, header_rows, self.__controller, self)
        export_dialog.exec()


#######################################################################################################
#  Update                                                                                             #
#######################################################################################################
    def update_widget(self, years_dict, name_dict, data_dict):
        """ Update this widget (from TotalWidget)

        Args:
            years_dict: New dictionary of year
            name_dict: New dictionary of categories
            data_dict: new dictionary of data
        """
        # Clear table
        self.__tab_stats.clear()
        self.__can_fill = False

        # get the new dictionaries
        self.__years_dict = years_dict
        self.__name_dict = name_dict
        self.__data_dict = data_dict["data"]

        # Update the widget
        self.__combobox_year.clear()
        self.__combobox_year.addItems(self.__years_dict.keys())
        if len(self.__years_dict.keys()) == 0:
            self.__combobox_year.hide()
            self.__export_stat_button.hide()
        else:
            if self.__combobox_year.isHidden():
                self.__combobox_year.show()
            if self.__export_stat_button.isHidden():
                self.__export_stat_button.show()

        # Construct and fill the table
        self.__construct_tab()
        

#######################################################################################################
#  Overwrite method to resize the widget                                                              #
#######################################################################################################
    def sizeHint(self) -> QtCore.QSize:
        """ Return the ideal length of the widget

        Returns:
            QtCore.QSize: Width and height
        """
        return QtCore.QSize(300, 500)
    
    
    def minimumSizeHint(self) -> QtCore.QSize:
        """ Return the minimal and ideal length of the widget

        Returns:
            QtCore.QSize: Width and height
        """
        return QtCore.QSize(50, 100)
    
    
    def sizePolicy(self) -> QtWidgets.QSizePolicy:
        """ Return the size policy of the widget.
            The width of the widget can extend but the height is fixed

        Returns:
            QtWidgets.QSizePolicy: Size policy
        """
        return QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
