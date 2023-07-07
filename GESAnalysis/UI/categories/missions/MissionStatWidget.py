from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QSizePolicy

class MissionStatWidget(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(MissionStatWidget, self).__init__(parent)
        
        self.__years_dict = {}
        self.__mode_dict = {}
        self.__position_dict = {}
        self.__data_dict = {}
        self.__mode_stat_list = {}
        self.__position_stat_list = {}
        
        self.__combobox_choice = QtWidgets.QComboBox(self)
        self.__combobox_year = QtWidgets.QComboBox(self)
        self.__tab_stats = QtWidgets.QTableWidget()
        
        self.__can_fill = False
        
        self.__init_UI()
        
        self.__construct_tab()
        
    def __init_UI(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.setSpacing(0)
        label = QtWidgets.QLabel()
        label.setText("Statistiques")
        label.setFixedHeight(20)
        
        
        self.__combobox_choice.currentTextChanged.connect(self.__refill_table)
        self.__combobox_choice.addItems(["Missions", "Distance", "Emission"])
        
        
        self.__combobox_year.addItems(self.__years_dict.keys())
        self.__combobox_year.currentTextChanged.connect(self.__refill_table)
        if len(self.__years_dict.keys()) == 0:
            self.__combobox_year.hide()
        
        layout_principal.addWidget(label, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        layout_principal.addWidget(self.__combobox_choice)
        layout_principal.addWidget(self.__combobox_year)
        layout_principal.addWidget(self.__tab_stats)
        
        self.setLayout(layout_principal)
        
        
    def __construct_tab(self):
        self.__mode_stat_list = list(self.__mode_dict.keys()) + (['total'] if len(self.__mode_dict.keys()) > 0 else [])
        self.__position_stat_list = list(self.__position_dict.keys()) + (['total'] if len(self.__mode_dict.keys()) > 0 else [])
        
        # Set number of row and columns + labels
        self.__tab_stats.setRowCount(len(self.__mode_stat_list))
        self.__tab_stats.setColumnCount(len(self.__position_stat_list))
        self.__tab_stats.setVerticalHeaderLabels(self.__mode_stat_list)
        self.__tab_stats.setHorizontalHeaderLabels(self.__position_stat_list)
        
        self.__can_fill = True
        self.__fill_table()
        
        
    def __fill_table(self):
        if len(self.__mode_stat_list) == 0 or len(self.__position_stat_list) == 0:
            return
        
        self.__tab_stats.clearContents()
        selected_category = self.__combobox_choice.currentText()
        selected_year = self.__combobox_year.currentText()
        corres_data_dict = ""
        if selected_category == "Missions":
            corres_data_dict = "mission"
        elif selected_category == "Distance":
            corres_data_dict = "total_distance"
        else:
            corres_data_dict = "total_emission"
        
        total_position_dict = {}
        for position in self.__position_dict.keys():
            total_position_dict[position] = 0

        data_all_mode = 0
        for mode_ind, mode in enumerate(self.__mode_stat_list):
            if mode == "total":
                continue
            data_total_mode = 0
            for pos_ind, position in enumerate(self.__position_stat_list):
                if position == "total":
                    data = str(data_total_mode)
                    data_item = QtWidgets.QTableWidgetItem(data)
                    self.__tab_stats.setItem(mode_ind, pos_ind, data_item)
                    continue
                
                data = self.__data_dict["data"][mode]["data"][position][selected_year][corres_data_dict]
                if selected_category == "Missions":
                    data = len(data)
                data_total_mode += data
                total_position_dict[position] += data
                data = str(data)
                data_item = QtWidgets.QTableWidgetItem(data)
                self.__tab_stats.setItem(mode_ind, pos_ind, data_item)
            data_all_mode += data_total_mode
        
        index_total_mode = self.__mode_stat_list.index("total")
        data_all_position = 0
        for pos_ind, position in enumerate(self.__position_dict.keys()):
            data_pos = total_position_dict[position]
            data = str(data_pos)
            data_item = QtWidgets.QTableWidgetItem(data)
            self.__tab_stats.setItem(index_total_mode, pos_ind, data_item)
            data_all_position += data_pos
        
        index_total_position = self.__position_stat_list.index("total")
        total_item = total_item = QtWidgets.QTableWidgetItem("ERROR" if data_all_position != data_all_mode else str(data_all_mode))            
        self.__tab_stats.setItem(index_total_mode, index_total_position, total_item)
            
    
    def __refill_table(self):
        if self.__can_fill:
            self.__fill_table()
        
    def update_widget(self, years_dict, mode_dict, position_dict, data_dict):
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
        else:
            if self.__combobox_year.isHidden():
                self.__combobox_year.show()
                
        self.__construct_tab()
        
    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 500)
    
    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(50, 100)
    
    def sizePolicy(self) -> QtWidgets.QSizePolicy:
        return QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
