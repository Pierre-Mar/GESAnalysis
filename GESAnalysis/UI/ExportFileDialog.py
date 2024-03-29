#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
from typing import List
from PyQt5 import QtWidgets, QtGui
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.UI import common


class ExportFileDialog(QtWidgets.QDialog):
    """ Dialog to export a file to another file
    """
    
    def __init__(
        self,
        selected_files: List[str],
        model: GESAnalysis,
        controller: Controleur, 
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the class

        Args:
            selected_files (List[str]): Files selected from FileOpenUI
            model (GESAnalysis): Model
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent of this dialog. Defaults to ....
        """
        # Intialise the parent class
        super(ExportFileDialog, self).__init__(parent)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        
        self.__path_file_to_export = self.__selected_file(selected_files) # File to export
        self.__path_file_save = ""                                        # File where the data of the file to export is saved
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialize the UI
        """
        # Set parameters to this dialog
        self.setWindowTitle("Exporter Fichier")
        self.setFixedWidth(600)
        
        # Create the dialog box for the buttons 'Ok' and 'Cancel'
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Create the widget to select the file to export and where to save
        form_widget = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout(form_widget)
        
        # Label and lineedit to choose the file to export
        choose_file_label = QtWidgets.QLabel("Localisation :", form_widget)
        self.choose_file = QtWidgets.QLineEdit(form_widget)
        # Set the text and add an icon
        # When we press on the icon, open a file dialog to choose the file
        self.choose_file.setText(self.__path_file_to_export)
        action_choose_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "open folder", form_widget)  
        action_choose_file.triggered.connect(self.choose_file_dialog)      
        # Connect this action to the lineedit
        self.choose_file.setClearButtonEnabled(True)
        self.choose_file.addAction(action_choose_file, QtWidgets.QLineEdit.TrailingPosition)
        
        # New row to get in which file the data needs to be save
        export_file_label = QtWidgets.QLabel("Sauvegarde :", form_widget)
        self.export_file = QtWidgets.QLineEdit(form_widget)
        self.export_file.setText(self.__path_file_save)
        # Add an icon, same above
        action_export_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "get file export", form_widget)
        action_export_file.triggered.connect(self.export_file_dialog)
        # Connect this action to lineedit
        self.export_file.setClearButtonEnabled(True)
        self.export_file.addAction(action_export_file, QtWidgets.QLineEdit.TrailingPosition)
        
        form_layout.addRow(choose_file_label, self.choose_file)
        form_layout.addRow(export_file_label, self.export_file)
        
        # Layout of this dialog
        principal_layout = QtWidgets.QVBoxLayout(self)
        principal_layout.addWidget(form_widget)
        principal_layout.addWidget(button_box)


#######################################################################################################
#  Actions associated to the UI                                                                       #
#######################################################################################################
    def choose_file_dialog(self) -> None:
        """ Open a file dialog to navigate between folders to select the file
        """
        select_file = QtWidgets.QFileDialog().getOpenFileName(
            self,
            "Selectionner un fichier",
            filter="Tous fichiers (*.*);;CSV, TSV, TXT (*.csv *.tsv *.txt);;Excel (*.xlsx)"
        )[0]
        # If the user cancel the operation, no need to save into the variable
        if select_file:
            self.__path_file_to_export = select_file
            self.choose_file.setText(self.__path_file_to_export)
            
    
    def export_file_dialog(self) -> None:
        """ Open a file dialog to get where and what is the file need to be save
        """
        select_file = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Selectionner un fichier",
            filter="Tous fichiers (*.*);;CSV, TSV, TXT (*.csv *.tsv *.txt)"
        )[0]
        if select_file:
            self.__path_file_save = select_file
            self.export_file.setText(self.__path_file_save)
            
    
    def accept(self) -> None:
        """ When the user click of the button 'Ok', send a notification to the controller
            to save the data of a file to another file
        """
        # Get the values from the lineedits
        self.__path_file_to_export = self.choose_file.text()
        self.__path_file_save = self.export_file.text()
        
        # Display a warning a file is not selected (export and save)
        if self.__path_file_to_export == "":
            common.message_warning("Vous devez entrer un fichier à exporter", self)
            return
        if self.__path_file_save == "":
            common.message_warning("Vous devez entrer un fichier de sauvegarde", self)
            return
        
        # Try to export a file to another file
        try:
            self.__controller.export_file(self.__path_file_to_export, self.__path_file_save)
            common.message_ok("Exportation réussie !", self)
            super().accept()
        # Display a message if the export is a success or not
        except Exception as e:
            common.message_error(str(e), self)
            self.clear_input()


    def clear_input(self) -> None:
        """ Clear input from the widgets and delete values
        """
        # Clear the input
        self.choose_file.setText("")
        self.export_file.setText("")
        
        # Delete values
        self.__path_file_to_export = None
        self.__path_file_save = None


#######################################################################################################
#  Method to get a selected file                                                                      #
#######################################################################################################
    def __selected_file(self, selected_files: List[str]) -> str:
        """ Get the path of the first file in selected_files

        Args:
            selected_files (List[str]): list of files

        Returns:
            str: Path to the fistr file if there are one or more, else ""
        """
        # If there are no files, we return ""
        if len(selected_files) == 0:
            return ""
        
        # Else, we need to know if it's already a path or the name of the file
        file = selected_files[0]
        try:
            return self.__gesanalysis.get_path(file)
        except:
            return file
