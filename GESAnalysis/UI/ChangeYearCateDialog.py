from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI import common


class ChangeYearCateDialog(QtWidgets.QDialog):
    """ Open a dialog to change the year and the category of a file
    """
    
    def __init__(
        self,
        file: str,
        year_file: str,
        category_file: str,
        controller: Controleur,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the class

        Args:
            file (str): File to change the year and the category
            year_file (str): Year of the file
            category_file (str): Category of the file
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this dialog. Defaults to ....
        """
        # Initialise the parent class
        super(ChangeYearCateDialog, self).__init__(parent)
        
        # Set parameters to attributes
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
        
        # Create the dialog box with the button 'Ok' and 'Cancel'
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Label to indicate to the user to modify the year and the category of the file
        label_file = QtWidgets.QLabel(self)
        label_file.setText(f"Modifier l'année ou la catégorie du fichier '{self.__modify_file}'")
        
        # Create a form widget to modify these informations
        form_widget = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        # Label and lineedit to modify the year
        choose_year_label = QtWidgets.QLabel("Année :", form_widget)
        self.choose_year = QtWidgets.QLineEdit(form_widget)
        self.choose_year.setPlaceholderText(self.__year_file) # Display the current year in grey when the lineedit is empty
        
        form_layout.addRow(choose_year_label, self.choose_year)
        
        # List view to choose the category
        choose_category_label = QtWidgets.QLabel("Catégorie :", form_widget)
        self.choose_category = QtWidgets.QComboBox(form_widget)
        self.choose_category.addItems(common.categories)
        self.choose_category.setCurrentText(self.__category_file)
        
        form_layout.addRow(choose_category_label, self.choose_category)
        
        # Layout of this dialog
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label_file)
        layout.addWidget(form_widget)
        layout.addWidget(button_box)
        

#######################################################################################################
#  Overwrite method when the user click on 'Ok'                                                       #
#######################################################################################################
    def accept(self) -> None:
        """ When the user click on the button 'OK', send a notification to the controller
            to change the year and the category of the file
        """
        # Get parameters of the line edit and list view
        selected_year = self.choose_year.text()
        selected_category = self.choose_category.currentText()
        
        # If the year is not fill in the line edit, get the current year
        if selected_year == '':
            selected_year = self.__year_file
        
        # Compare values, if there are no change, we skip directly
        if selected_year == self.__year_file and selected_category == self.__category_file:
            super().accept()

        # Else, send the notification to the controller
        try:
            self.__controleur.set_category_year(self.__modify_file, selected_year, selected_category, self.__category_file)
            super().accept()
        # Display a message if there an error and clear lineedits
        except Exception as e:
            common.message_error(str(e), self)
            self.clear_input()
        
    
    def clear_input(self) -> None:
        """ Clear input from the widgets and delete values
        """
        # Clear the input
        self.choose_year.setText("")
        self.choose_category.setCurrentText(self.__category_file)