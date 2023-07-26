from PyQt5 import QtWidgets, QtCore
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.ExportStatDialog import ExportStatDialog


class AchatsStatWidget(QtWidgets.QWidget):
    """ Widget to display the stat of the files from "Achats"
    """
    
    def __init__(self, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(AchatsStatWidget, self).__init__(parent)
        
        # Set parameter to attribute
        self.__controller = controller
        
        self.__years_dict = {}     # Dictionary of years
        self.__data_dict = {}      # Dictionary of data
        self.__data_table = {}     # Dictionary of data for table
        self.__column_stats = []   # Header columns table (Amount)
        self.__row_name_stats = [] # Header rows table (NACRES key)
        
        # Create widgets
        self.__combobox_year = QtWidgets.QComboBox(self)                    # Combobox to choose the year to display the stat
        self.__tab_stats = QtWidgets.QTableWidget(self)                     # Table containing the stat
        self.__export_stat_button = QtWidgets.QPushButton("Exporter", self) # Button to export the table
        
        # Boolean use to indicate if we can fill the table
        self.__can_fill = False
        
        self.__init_UI()
        
        self.__construct_tab()
        

#######################################################################################################
#  Initialise UI                                                                                      #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameters to this widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Label : Statistiques
        label = QtWidgets.QLabel("Statistiques", self)
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
        self.__tab_stats.clear()
        self.__column_stats.clear()
        self.__row_name_stats.clear()
        self.__can_fill = True
        self.__data_table = {}
        if len(self.__years_dict.keys()) > 0:
            # Configure list and dictionary for the table
            self.__column_stats = ["Montant"]
            total = 0
            selected_year = self.__combobox_year.currentText()
            # Row contains all the NACRES key of the year
            for nacres_key, amount in self.__data_dict[selected_year]:
                if nacres_key not in self.__row_name_stats:
                    self.__row_name_stats.append(nacres_key)
                    self.__data_table[nacres_key] = {"Montant" : amount}
                else:
                    self.__data_table[nacres_key]["Montant"] += amount
                total += amount
            
            self.__row_name_stats.append("total")
            self.__data_table["total"] = {"Montant": total}
        else:
            self.__column_stats = []
            self.__row_name_stats = []
        
        self.__tab_stats.setRowCount(len(self.__row_name_stats))
        self.__tab_stats.setVerticalHeaderLabels(self.__row_name_stats)
        self.__tab_stats.setColumnCount(len(self.__column_stats))
        self.__tab_stats.setHorizontalHeaderLabels(self.__column_stats)
        
        self.__fill_table()
        
    
    def __fill_table(self) -> None:
        """ Fill the table with data
        """
        # If there are no stats, return
        if len(self.__column_stats) == 0 or len(self.__row_name_stats) == 0:
            return
        
        # Clear the table in case there are already data
        self.__tab_stats.clearContents()
        
        # Fill the table
        for col_index, col in enumerate(self.__column_stats):
            for row_index, row in enumerate(self.__row_name_stats):
                self.__data_table[row][col] = round(self.__data_table[row][col], 2)
                amount = self.__data_table[row][col]
                amount_str = str(amount)
                
                amount_item = QtWidgets.QTableWidgetItem(amount_str)
                amount_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                self.__tab_stats.setItem(row_index, col_index, amount_item)
                
                
#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def __refill_table(self) -> None:
        """ Refill the table if the user change the year
        """
        if self.__can_fill:
            self.__construct_tab()
                
    
    def __open_dialog_export_stat(self) -> None:
        """ Open a dialog to export the table
        """
        header_columns = self.__column_stats
        header_rows = self.__row_name_stats
        
        # Configure data to export it
        data = []
        for row in range(len(header_rows)):
            l = []
            for col in range(len(header_columns)):
                item = self.__tab_stats.item(row, col)
                l.append(item.text())
            data.append(l)
            
        # Open and execute the dialog
        export_dialog = ExportStatDialog(data, header_columns, header_rows, self.__controller, self)
        export_dialog.exec()
        
        
#######################################################################################################
#  Update                                                                                             #
#######################################################################################################
    def update_widget(self, years_dict, data_dict) -> None:
        """ Update this widget (from AchatsWidget)

        Args:
            years_dict : New dictionary of years
            data_dict : New dictionary of data
        """
        self.__can_fill = False
        
        # Get the new dictionaries
        self.__years_dict = years_dict.copy()
        self.__data_dict = data_dict["data"].copy()
        
        # Update the widgets
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