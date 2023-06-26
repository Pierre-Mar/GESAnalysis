from PyQt5 import QtWidgets


class ChangeYearCateDialog(QtWidgets.QDialog):
    
    
    def __init__(self, file, model, controller, parent: QtWidgets.QWidget | None = ...) -> None:
        super(ChangeYearCateDialog, self).__init__(parent)
        
        self.__gesanalysis = model
        self.__controleur = controller
        self.__modify_file = file
        
        self.__init_UI()
        
        
    def __init_UI(self):
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
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label_file)
        layout.addWidget(form_widget)
        layout.addWidget(button_box)