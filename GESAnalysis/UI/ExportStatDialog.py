from PyQt5 import QtWidgets, QtGui

from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI import common


class ExportStatDialog(QtWidgets.QDialog):
    
    
    def __init__(self, data, header_columns, header_rows, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        super(ExportStatDialog, self).__init__(parent)
        
        self.__data = data
        self.__header_columns = header_columns
        self.__header_rows = header_rows
        self.__controller = controller
        
        self.__path_file_save = ""
        
        self.__init_UI()
    
    
    def __init_UI(self):
        self.setWindowTitle("Exporter Statistiques")
        self.setFixedWidth(600)
        
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        
        buttons_box = QtWidgets.QDialogButtonBox(buttons)
        buttons_box.accepted.connect(self.accept)
        buttons_box.rejected.connect(self.reject)
        
        form_layout = QtWidgets.QFormLayout(self)
        self.setLayout(form_layout)
        
        localisation_label = QtWidgets.QLabel(self)
        localisation_label.setText("Localisation :")
        
        self.__localisation_lineedit = QtWidgets.QLineEdit(self)
        action_choose_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "open folder", self)
        action_choose_file.triggered.connect(self.__choose_file)
        self.__localisation_lineedit.setClearButtonEnabled(True)
        self.__localisation_lineedit.addAction(action_choose_file, QtWidgets.QLineEdit.TrailingPosition)
        self.__localisation_lineedit.setText(self.__path_file_save)
        
        form_layout.addRow(localisation_label, self.__localisation_lineedit)
        form_layout.addWidget(buttons_box)
        
    
    def __choose_file(self):
        select_file = QtWidgets.QFileDialog().getSaveFileName(
            self,
            "Selectionner un fichier",
            filter="Tous Fichiers (*.*);;CSV, TSV, TXT (*.csv, *.tsv, *.txt);;"
        )[0]
        if select_file:
            self.__path_file_save = select_file
            self.__localisation_lineedit.setText(self.__path_file_save)
            
            
    def accept(self):
        self.__path_file_save = self.__localisation_lineedit.text()
        
        if self.__path_file_save == "":
            common.message_warning("Vous devez entrer un fichier de sauvegarde", self)
            return
        
        try:
            self.__controller.export_stat(self.__data, self.__header_columns, self.__header_rows, self.__path_file_save)
            common.message_ok("Exportation réussie !", self)
            super().accept()
        except Exception as e:
            common.message_error(str(e), self)
            self.__clear_input()
            
    
    def __clear_input(self):
        self.__localisation_lineedit.setText("")
        
        self.__path_file_save = ""
        