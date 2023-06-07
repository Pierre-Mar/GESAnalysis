from PyQt5 import QtWidgets


class OpenFileDialog(QtWidgets.QDialog):
    
    categories = ["Missions"]
    
    def __init__(self, model, controller, parent: QtWidgets.QWidget | None = ...) -> None:
        super(OpenFileDialog, self).__init__(parent)
        self.setWindowTitle("Ouvrir Fichier")
        
        self.__gesanalysis = model
        self.__controller = controller
        
        self.__init_UI()
        
        
    def __init_UI(self):
        self.buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        
        # Buttons for 'Ok' and 'Cancel'
        self.button_box = QtWidgets.QDialogButtonBox(self.buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.form_widget = QtWidgets.QWidget(self)
        self.form_layout = QtWidgets.QFormLayout(self.form_widget)
        
        # Label and line edit to choose file
        choose_file_label = QtWidgets.QLabel("Localisation :", self.form_widget)
        self.choose_file = QtWidgets.QLineEdit(self.form_widget)
        self.form_layout.addRow(choose_file_label, self.choose_file)
        
        # Line edit to get the year
        choose_year_label = QtWidgets.QLabel("Année :", self.form_widget)
        self.choose_year = QtWidgets.QLineEdit(self.form_widget)
        self.form_layout.addRow(choose_year_label, self.choose_year)
        
        # List view for choose a category
        choose_category_label = QtWidgets.QLabel("Catégorie :", self.form_widget)
        self.choose_category = QtWidgets.QComboBox(self.form_widget)
        self.choose_category.addItems(self.categories)
        self.form_layout.addRow(choose_category_label, self.choose_category)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        layout.addWidget(self.form_widget)
        layout.addWidget(self.button_box)
