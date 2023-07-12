from PyQt5 import QtWidgets, QtGui

from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI import common


class OpenFileDialog(QtWidgets.QDialog):
    """ Class to open a dialog to select a file from the user and read it
    """
    
    def __init__(self, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialisation of the dialog

        Args:
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this dialog. Defaults to ....
        """
        super(OpenFileDialog, self).__init__(parent)
        
        self.__controller = controller
        
        self.selected_file = None
        self.selected_year = None
        self.selected_category = None
        
        self.__init_UI()
        
        
    def __init_UI(self) -> None:
        """ Initialise the UI 
        """
        # Set parameters to dialog
        self.setWindowTitle("Ouvrir Fichier")
        self.setFixedWidth(600)
        
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        
        # Create the dialog box and the button 'Ok' and 'Cancel'
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        form_widget = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        # Label and line edit to choose file
        choose_file_label = QtWidgets.QLabel("Localisation :", form_widget)
        self.choose_file = QtWidgets.QLineEdit(form_widget)
        # Add a icon to line edit
        # When we press on it, open a file dialog to choose the file
        action_search_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "open folder", form_widget)
        action_search_file.triggered.connect(self.open_file_dialog)
        
        # Connect this action to line edit
        self.choose_file.setClearButtonEnabled(True)
        self.choose_file.addAction(action_search_file, QtWidgets.QLineEdit.TrailingPosition)
        
        form_layout.addRow(choose_file_label, self.choose_file)
        
        # Line edit to get the year
        choose_year_label = QtWidgets.QLabel("Année :", form_widget)
        self.choose_year = QtWidgets.QLineEdit(form_widget)
        
        form_layout.addRow(choose_year_label, self.choose_year)
        
        # List view for choose a category
        choose_category_label = QtWidgets.QLabel("Catégorie :", form_widget)
        self.choose_category = QtWidgets.QComboBox(form_widget)
        self.choose_category.addItems(common.categories)
        form_layout.addRow(choose_category_label, self.choose_category)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        layout.addWidget(form_widget)
        layout.addWidget(button_box)
        
        
    def open_file_dialog(self) -> None:
        """ Open a file dialog to navigate between folders to select the file
        """
        self.selected_file = QtWidgets.QFileDialog().getOpenFileName(
            self,
            "Selectionner un fichier",
            filter="Tous fichiers (*.*);;CSV, TSV, TXT (*.csv *.tsv *.txt);;Excel (*.xlsx)"
        )[0]
        # If the user cancel the operation, no need to save into the variable
        if self.selected_file:
            self.choose_file.setText(self.selected_file)


    def accept(self) -> None:
        """ When the user click on the button 'OK', send a notification to the controller
            to read the selected file and associate the year and the category
        """
        # Get the values from the input
        self.selected_file = self.choose_file.text()
        self.selected_year = self.choose_year.text()
        self.selected_category = self.choose_category.currentText()

        if self.selected_file == "":
            # Need to choose a file
            common.message_warning("Vous devez entrer un fichier", self)
            return
        elif self.selected_year == "":
            common.message_warning("Vous devez entrer une année", self)
            return
        
        # Send notification to controller to read file
        try:
            self.__controller.open_file(self.selected_file, self.selected_year, self.selected_category)
            # Close dialog if the file was read
            super().accept()
        # In case of error, display a message with the corresponding error
        except Exception as e:
            common.message_error(str(e), self)
            self.clear_input()


    def clear_input(self) -> None:
        """ Clear input from the widgets and delete values
        """
        # Clear the input
        self.choose_file.setText("")
        self.choose_year.setText("")
        
        # Delete values
        self.selected_file = None
        self.selected_year = None