from PyQt5 import QtWidgets
import GESAnalysis.UI.common as common


class ChangeYearCateDialog(QtWidgets.QDialog):
    """ Open a dialog to change the year and the category of a file in the model
    """
    
    
    def __init__(self, file, model, controller, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class and the UI

        Args:
            file (str): The file to moodify
            model (GESAnalysis): Model
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this widget. Defaults to ....
        """
        super(ChangeYearCateDialog, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controleur = controller
        self.__modify_file = file
        
        self.__init_UI()
        
        
    def __init_UI(self) -> None:
        """ Initialize the UI
        """
        # Set parameters to dialog
        self.setWindowTitle("Modifier Fichier")
        self.setFixedWidth(600)
        
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        
        # Create the dialog box and the button 'Ok' and 'Cancel'
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Label to indicate to the user to modify the year and the category of the file
        label_file = QtWidgets.QLabel(self)
        label_file.setText(f"Modifier l'année ou la catégorie du fichier '{self.__modify_file}'")
        
        # Create a form widget to modify these informations
        form_widget = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        # Label and line edit to modify the year
        choose_year_label = QtWidgets.QLabel("Année :", form_widget)
        self.choose_year = QtWidgets.QLineEdit(form_widget)
        self.choose_year.setPlaceholderText(self.__gesanalysis.get_year(self.__modify_file))
        
        form_layout.addRow(choose_year_label, self.choose_year)
        
        # List view for choose the category
        choose_category_label = QtWidgets.QLabel("Catégorie :", form_widget)
        self.choose_category = QtWidgets.QComboBox(form_widget)
        self.choose_category.addItems(common.categories)
        self.choose_category.setCurrentText(self.__gesanalysis.get_category(self.__modify_file))
        
        form_layout.addRow(choose_category_label, self.choose_category)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label_file)
        layout.addWidget(form_widget)
        layout.addWidget(button_box)
        
        
    def accept(self) -> None:
        """ When the user click on the button 'OK', send to the controller
            to change the year and the category the the file
        """
        selected_year = self.choose_year.text()
        selected_category = self.choose_category.currentText()
        
        old_year = self.__gesanalysis.get_year(self.__modify_file)
        if selected_year == '':
            selected_year = old_year
        old_category = self.__gesanalysis.get_category(self.__modify_file)
        
        # Compare values, if there are no change, we skip directly
        if selected_year == old_year and selected_category == old_category:
            super().accept()
            
        try:
            self.__controleur.set_category_year(self.__modify_file, selected_year, selected_category)
            super().accept()
        except Exception as e:
            self.message_error(str(e))
        
        
        
    def message_error(self, string: str) -> None:
        """ Display a error box to the user

        Args:
            string (str): The message
        """
        dlg = QtWidgets.QMessageBox.critical(
            self,
            "Erreur",
            string
        )
        
    
    def clear_input(self) -> None:
        """ Clear input from the widgets and delete values
        """
        # Clear the input
        self.choose_year.setText("")
        self.choose_category.setCurrentText(self.__gesanalysis.get_category(self.__modify_file))