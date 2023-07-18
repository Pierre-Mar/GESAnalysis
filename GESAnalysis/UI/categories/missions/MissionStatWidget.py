from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QSizePolicy
from GESAnalysis.FC.Controleur import Controleur

from GESAnalysis.UI.ExportStatDialog import ExportStatDialog

class MissionStatWidget(QtWidgets.QWidget):
    """ Widget to display the stat of the files from "Missions"
    """
    
    def __init__(self, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the class
        super(MissionStatWidget, self).__init__(parent)
        
        # Set parameter to attribute
        self.__controller = controller
        
        # Data structure
        self.__years_dict = {}         # Dictionary of years
        self.__mode_dict = {}          # Dictionary of mode
        self.__position_dict = {}      # Dictionary of position
        self.__data_dict = {}          # Dictionary of data
        self.__mode_stat_list = []     # Header rows
        self.__position_stat_list = [] # Header columns
        
        # Create widgets
        self.__combobox_choice = QtWidgets.QComboBox(self)                  # Combobox to choose "Missions", "Distance", "Emission"
        self.__combobox_year = QtWidgets.QComboBox(self)                    # Combobox to choose the year
        self.__tab_stats = QtWidgets.QTableWidget(self)                     # Table containing the stat
        self.__export_stat_button = QtWidgets.QPushButton("Exporter", self) # Button to export the table
        
        # Boolean use to fill or not the table
        self.__can_fill = False
        
        self.__init_UI()
        
        self.__construct_tab()


#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the Ui
        """
        # Set parameter to the widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Label : Statistiques
        label = QtWidgets.QLabel()
        label.setText("Statistiques")
        label.setFixedHeight(20)
        
        # add different choices to the combobox
        self.__combobox_choice.currentTextChanged.connect(self.__refill_table)
        self.__combobox_choice.addItems(["Missions", "Distance", "Emission", "Emission avec trainées"])
        
        # Add years to the combobox
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
        layout_principal.addWidget(self.__combobox_choice)
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
        self.__mode_stat_list = list(self.__mode_dict.keys()) + (['total'] if len(self.__mode_dict.keys()) > 0 else [])
        self.__position_stat_list = list(self.__position_dict.keys()) + (['total'] if len(self.__mode_dict.keys()) > 0 else [])
        
        # Set number of row and columns + labels
        self.__tab_stats.setRowCount(len(self.__mode_stat_list))
        self.__tab_stats.setColumnCount(len(self.__position_stat_list))
        self.__tab_stats.setVerticalHeaderLabels(self.__mode_stat_list)
        self.__tab_stats.setHorizontalHeaderLabels(self.__position_stat_list)
        
        self.__can_fill = True
        self.__fill_table()
        
        
    def __fill_table(self) -> None:
        """ Fill the table
        """
        # if there are no stats, return
        if len(self.__mode_stat_list) == 0 or len(self.__position_stat_list) == 0:
            return
        
        # Clear the table in case of the table have some stats
        self.__tab_stats.clearContents()
        
        # Get parameters for table
        selected_category = self.__combobox_choice.currentText()
        selected_year = self.__combobox_year.currentText()
        
        # Depending on the choice, set a variable to corresponding key in the data structure
        corres_data_dict = ""
        if selected_category == "Missions":
            corres_data_dict = "mission"
        elif selected_category == "Distance":
            corres_data_dict = "total_distance"
        elif selected_category == "Emission":
            corres_data_dict = "total_emission"
        else:
            corres_data_dict = "total_emission_contrails"
        
        # Dictionary of position and calculate the total
        total_position_dict = {}
        for position in self.__position_dict.keys():
            total_position_dict[position] = 0

        # Fill the table for each mode and position
        data_all_mode = 0
        for mode_ind, mode in enumerate(self.__mode_stat_list):
            if mode == "total":
                continue
            data_total_mode = 0
            for pos_ind, position in enumerate(self.__position_stat_list):
                if position == "total":
                    data = str(data_total_mode)
                    data_item = QtWidgets.QTableWidgetItem(data)
                    data_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                    self.__tab_stats.setItem(mode_ind, pos_ind, data_item)
                    continue
                
                data = self.__data_dict["data"][mode]["data"][position][selected_year][corres_data_dict]
                if selected_category == "Missions":
                    data = len(data)
                data_total_mode += data
                total_position_dict[position] += data
                data = str(data)
                data_item = QtWidgets.QTableWidgetItem(data)
                data_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                self.__tab_stats.setItem(mode_ind, pos_ind, data_item)
            data_all_mode += data_total_mode
        
        # Fill the table for each position and the mode is "total"
        index_total_mode = self.__mode_stat_list.index("total")
        data_all_position = 0
        for pos_ind, position in enumerate(self.__position_dict.keys()):
            data_pos = total_position_dict[position]
            data = str(data_pos)
            data_item = QtWidgets.QTableWidgetItem(data)
            data_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.__tab_stats.setItem(index_total_mode, pos_ind, data_item)
            data_all_position += data_pos
        
        # Fill the case of "total", "total"
        index_total_position = self.__position_stat_list.index("total")
        total_item = total_item = QtWidgets.QTableWidgetItem("ERROR" if data_all_position != data_all_mode else str(data_all_mode))  
        total_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)          
        self.__tab_stats.setItem(index_total_mode, index_total_position, total_item)
            

#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def __refill_table(self) -> None:
        """ Refill the table if the user change the year or the choice
        """
        if self.__can_fill:
            self.__fill_table()


    def __open_dialog_export_stat(self):
        """ Open a dialog to export the table in a file
        """
        # Get the header
        header_rows = self.__mode_stat_list
        header_columns = self.__position_stat_list
        
        # Configure data to export it
        data = []
        for mode_ind in range(len(header_rows)):
            l = []
            for position_ind in range(len(header_columns)):
                item = self.__tab_stats.item(mode_ind, position_ind)
                l.append(item.text())
            data.append(l)
            
        # Open and execute the dialog
        export_dialog = ExportStatDialog(data, header_columns, header_rows, self.__controller, self)
        export_dialog.exec()


#######################################################################################################
#  Update                                                                                             #
#######################################################################################################
    def update_widget(self, years_dict, mode_dict, position_dict, data_dict):
        """ Update this widget (from MissionWidget)

        Args:
            years_dict : New dictionary of year
            mode_dict : New dictionary of mode
            position_dict : New dictionary of position
            data_dict : New dictionary of data
        """
        # Remove all item and headers in the table
        self.__tab_stats.clear()
        self.__can_fill = False
        
        # Set dictionary to attribute
        self.__years_dict = years_dict
        self.__mode_dict = mode_dict
        self.__position_dict = position_dict
        self.__data_dict = data_dict
        
        # Hide or show the combobox of year
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
