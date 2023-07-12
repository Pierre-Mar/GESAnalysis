from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from GESAnalysis.FC.Controleur import Controleur

from GESAnalysis.UI.ExportStatDialog import ExportStatDialog


class TotalStatWidget(QtWidgets.QWidget):
    
    def __init__(self, controller: Controleur, parent: QWidget | None = ...) -> None:
        super(TotalStatWidget, self).__init__(parent)
        
        self.__controller = controller

        self.__years_dict = {}
        self.__name_dict = {}
        self.__data_dict = {}
        self.__column_stats = []
        self.__name_stat_list = []

        self.__combobox_year = QtWidgets.QComboBox(self)
        self.__tab_stats = QtWidgets.QTableWidget(self)
        self.__export_stat_button = QtWidgets.QPushButton("Exporter", self)

        self.__can_fill = False

        self.__init_UI()

        self.__construct_tab()


    def __init_UI(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.setSpacing(0)
        label = QtWidgets.QLabel(self)
        label.setText("Statistiques")
        label.setFixedHeight(20)

        self.__combobox_year.addItems(self.__years_dict.keys())
        self.__combobox_year.currentTextChanged.connect(self.__refill_table)
        
        self.__export_stat_button.clicked.connect(self.__open_dialog_export_stat)
        if len(self.__years_dict.keys()) == 0:
            self.__combobox_year.hide()
            self.__export_stat_button.hide()

        layout_principal.addWidget(label, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        layout_principal.addWidget(self.__combobox_year)
        layout_principal.addWidget(self.__tab_stats)
        layout_principal.addWidget(self.__export_stat_button)

        self.setLayout(layout_principal)


    def __construct_tab(self):
        self.__column_stats = ["Empreinte carbone"] if len(self.__name_dict.keys()) > 0 else []
        self.__name_stat_list = list(self.__name_dict.keys()) + (["total"] if len(self.__name_dict.keys()) > 0 else [])

        self.__tab_stats.setRowCount(len(self.__name_stat_list))
        self.__tab_stats.setColumnCount(len(self.__column_stats))
        self.__tab_stats.setVerticalHeaderLabels(self.__name_stat_list)
        self.__tab_stats.setHorizontalHeaderLabels(self.__column_stats)

        self.__can_fill = True
        self.__fill_table()


    def __fill_table(self):
        if len(self.__column_stats) == 0 or len(self.__name_stat_list) == 0:
            return
        
        self.__tab_stats.clearContents()
        selected_year = self.__combobox_year.currentText()

        total = 0
        index_year = self.__years_dict[selected_year]["index"]
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


    def __refill_table(self):
        if self.__can_fill:
            self.__fill_table()


    def update_widget(self, years_dict, name_dict, data_dict):
        self.__tab_stats.clear()
        self.__can_fill = False

        self.__years_dict = years_dict
        self.__name_dict = name_dict
        self.__data_dict = data_dict["data"]

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
        
    
    def __open_dialog_export_stat(self):
        header_columns = self.__column_stats
        header_rows = self.__name_stat_list
        
        data = []
        for row in range(len(header_rows)):
            l = []
            for col in range(len(header_columns)):
                item = self.__tab_stats.item(row, col)
                l.append(item.text())
            data.append(l)
        
        export_dialog = ExportStatDialog(data, header_columns, header_rows, self.__controller, self)
        export_dialog.exec()


    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 500)
    
    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(50, 100)
    
    def sizePolicy(self) -> QtWidgets.QSizePolicy:
        return QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
