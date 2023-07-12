from PyQt5 import QtWidgets
from GESAnalysis.UI import common


class ChangeYearCateDialog(QtWidgets.QDialog):
    """ Open a dialog to change the year and the category of a file in the model
    """
    
    
    def __init__(self, file, year_file, category_file, controller, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialize the class and the UI

        Args:
            file (str): The file to moodify
            model (GESAnalysis): Model
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this widget. Defaults to ....
        """
        super(ChangeYearCateDialog, self).__init__(parent)
        
        self.__controleur = controller
        self.__modify_file = file
        self.__year_file = year_file
        self.__category_file = category_file
        
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
        self.choose_year.setPlaceholderText(self.__year_file)
        
        form_layout.addRow(choose_year_label, self.choose_year)
        
        # List view for choose the category
        choose_category_label = QtWidgets.QLabel("Catégorie :", form_widget)
        self.choose_category = QtWidgets.QComboBox(form_widget)
        self.choose_category.addItems(common.categories)
        self.choose_category.setCurrentText(self.__category_file)
        
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
        
        if selected_year == '':
            selected_year = self.__year_file
        
        # Compare values, if there are no change, we skip directly
        if selected_year == self.__year_file and selected_category == self.__category_file:
            super().accept()
            
        try:
            self.__controleur.set_category_year(self.__modify_file, selected_year, selected_category, self.__category_file)
            super().accept()
        except Exception as e:
            common.message_error(str(e), self)
        
    
    def clear_input(self) -> None:
        """ Clear input from the widgets and delete values
        """
        # Clear the input
        self.choose_year.setText("")
        self.choose_category.setCurrentText(self.__category_file)