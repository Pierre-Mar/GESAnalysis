from PyQt5 import QtWidgets, QtGui
from typing import List
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI import common


class ExportStatDialog(QtWidgets.QDialog):
    """ Dialog to save the stats into a file
    """
    
    def __init__(
        self,
        data: List[List[str]],
        header_columns: List[str],
        header_rows: List[str],
        controller: Controleur,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the class

        Args:
            data (List[List[str]]): 2D list where a value at position (i, j) representing the stat
            of the column header_columns[j] and the row header_rows[i]
            header_columns (List[str]): Header of the columns of data
            header_rows (List[str]): Header of the rows of data
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this dialog. Defaults to ....
        """
        # Initialize the parent class
        super(ExportStatDialog, self).__init__(parent)
        
        # Set parameters to attributes
        self.__data = data
        self.__header_columns = header_columns
        self.__header_rows = header_rows
        self.__controller = controller
        
        # Contains the path of the file where the stats of data are going to be saved
        self.__path_file_save = ""
        
        self.__init_UI()


#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI of the dialog
        """
        # Set parameters to the dialog
        self.setWindowTitle("Exporter Statistiques")
        self.setFixedWidth(600)
        
        # Create the dialog box with the button 'Ok' and 'Cancel'
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        buttons_box = QtWidgets.QDialogButtonBox(buttons)
        buttons_box.accepted.connect(self.accept)
        buttons_box.rejected.connect(self.reject)
        
        # Label and lineedit to the path of the selected file
        localisation_label = QtWidgets.QLabel(self)
        localisation_label.setText("Localisation :")
        self.__localisation_lineedit = QtWidgets.QLineEdit(self)
        # Add a icon to line edit
        # When we press on it, open a file dialog to choose the file
        action_choose_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "open folder", self)
        action_choose_file.triggered.connect(self.__choose_file)
        self.__localisation_lineedit.setClearButtonEnabled(True)
        self.__localisation_lineedit.addAction(action_choose_file, QtWidgets.QLineEdit.TrailingPosition)
        self.__localisation_lineedit.setText(self.__path_file_save)
        
        # Layout of this dialog
        form_layout = QtWidgets.QFormLayout(self)
        self.setLayout(form_layout)
        form_layout.addRow(localisation_label, self.__localisation_lineedit)
        form_layout.addWidget(buttons_box)
        

#######################################################################################################
#  Methods connected to an action                                                                     #
#######################################################################################################
    def __choose_file(self) -> None:
        """ Open a file dialog to select a file and get the path
        """
        select_file = QtWidgets.QFileDialog().getSaveFileName(
            self,
            "Selectionner un fichier",
            filter="Tous Fichiers (*.*);;CSV, TSV, TXT (*.csv, *.tsv, *.txt);;"
        )[0]
        if select_file:
            self.__path_file_save = select_file
            self.__localisation_lineedit.setText(self.__path_file_save)
            

    def accept(self) -> None:
        """ When the user click on the button 'OK', send a notification to the controller
            to save the stat of data in the selected file
        """
        self.__path_file_save = self.__localisation_lineedit.text()
        
        # If there are no file, display a warning to the user
        if self.__path_file_save == "":
            common.message_warning("Vous devez entrer un fichier de sauvegarde", self)
            return
        
        # Else, send notification to the controller and display a message if the save is a success or not
        try:
            self.__controller.export_stat(self.__data, self.__header_columns, self.__header_rows, self.__path_file_save)
            common.message_ok("Exportation réussie !", self)
            super().accept()
        # Display a message in case of an error
        except Exception as e:
            common.message_error(str(e), self)
            self.__clear_input()
            
    
    def __clear_input(self) -> None:
        """ Clear the input from the widget and delete value
        """
        self.__localisation_lineedit.setText("")
        self.__path_file_save = ""
