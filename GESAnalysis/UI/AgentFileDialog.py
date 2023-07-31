#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
from typing import Dict, Optional
from PyQt5 import QtWidgets, QtGui
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI import common


class AgentFileDialog(QtWidgets.QDialog):
    """ Dialog to read a file with the number of agents
    """
    
    # List used to search if there a row with the name inside the list
    row_total = ["Total", "total", "TOTAL"]
    
    
    def __init__(self, old_path:str, controller: Controleur, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the class

        Args:
            old_path (str): Old path of the file who was read
            controller (Controleur): Controller
            parent (QtWidgets.QWidget | None, optional): Parent to this class. Defaults to ....
        """
        # Initialise the parent class
        super(AgentFileDialog, self).__init__(parent)
        
        # Set parameters to attributes
        self.__old_file = old_path if old_path is not None else ''
        self.__controller = controller
        
        # Attributes used to return from this dialog
        self.selected_file = ''
        self.data_agent_per_year = {}
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI of this dialog
        """
        # Set parameters to this dialog
        self.setWindowTitle("Ajouter fichier agent")
        self.setFixedWidth(600)
        
        # Create the dialog box with the button 'Ok' and 'Cancel'
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        buttons_box = QtWidgets.QDialogButtonBox(buttons)
        buttons_box.accepted.connect(self.accept)
        buttons_box.rejected.connect(self.reject)
        
        # Create a form layout to indicate the path of the file to read
        localisation_widget = QtWidgets.QWidget(self)
        localisation_layout = QtWidgets.QFormLayout(localisation_widget)
        
        # Label and lineedit to indicate the path of the file to read
        choose_file_label = QtWidgets.QLabel("Localisation :", localisation_widget)
        self.choose_file_lineedit = QtWidgets.QLineEdit(localisation_widget)
        self.choose_file_lineedit.setPlaceholderText(self.__old_file)
        
        # Add icon to lineedit to open a dialog to choose the file
        action_search_file = action_search_file = QtWidgets.QAction(QtGui.QIcon("GESAnalysis/UI/assets/folder-horizontal.png"), "open folder", localisation_widget)
        action_search_file.triggered.connect(self.open_file_dialog)
        self.choose_file_lineedit.setClearButtonEnabled(True)
        self.choose_file_lineedit.addAction(action_search_file, QtWidgets.QLineEdit.TrailingPosition)
        
        localisation_layout.addRow(choose_file_label, self.choose_file_lineedit)
        
        localisation_widget.setLayout(localisation_layout)
        
        # Layout of this dialog
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(localisation_widget)
        layout.addWidget(buttons_box)
        self.setLayout(layout)
        
        
#######################################################################################################
#  Methods connected to an action                                                                     #
#######################################################################################################
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
            # Display the file selected by the user in the lineedit
            self.choose_file_lineedit.setText(self.selected_file)
        
        
#######################################################################################################
#  Overwrite method when the user click on 'Ok'                                                       #
#######################################################################################################
    def accept(self) -> None:
        """ When the user click on the button 'Ok', send a notification to the controller to read the file
            in the lineedit and return the file with 
        """
        # Get the path from the lineedit
        self.selected_file = self.choose_file_lineedit.text()
        # If there are no file, we take the old file
        if self.selected_file == "":
            self.selected_file = self.__old_file
            
        # If the file is the same as the old file, then no need to re-read it
        # because we have already the value
        if self.selected_file == self.__old_file:
            super().accept()
            
        # Else, send a notification to the controller to read this file
        try:
            data_file = self.__controller.open_file_agent(self.selected_file)
            self.__get_number_agents(data_file)
            super().accept()
        except Exception as e:
            common.message_error(str(e), self)


#######################################################################################################
#  Method use to get the number of agents per year                                                    #
#######################################################################################################
    def __get_number_agents(self, data_file) -> None:
        """ Returns a dictionary where the key is a year and the value the number of agent of this year
            from the data of the file

        Args:
            data_file (dict): Data of file
        """
        self.data_agent_per_year = {}
        row_index = -1
        for key_index, key in enumerate(data_file.keys()):
            data_key = data_file[key]
            # If it's the first column, we search if there are the row name like 'Total' (row_total)
            # If not, we raised an error
            if key_index == 0:
                row_index = self.__search_total_row(data_key)
                if row_index == -1:
                    raise Exception(f"La ligne 'Total' de la 1ère colonne n'a pas été trouvée")
                continue
            
            # Else, for the rest of the column, we associate the name of the column and the value in total
            if data_key["type"] != int:
                continue
            
            # Add to dictionary
            name_column = '.'.join(data_key['name'])
            self.data_agent_per_year[name_column] = sum(data_key['data'][row_index])
    
    
    def __search_total_row(self, data_column: dict) -> int:
        """ Search the row 'total' in the column data_column

        Args:
            data_column (dict): Data of column

        Returns:
            int: -1 if it's not found, else his index
        """
        data_per_row = data_column["data"]
        for row_index, row_name in enumerate(data_per_row):
            row_name_join = ' '.join(row_name)
            if row_name_join in self.row_total:
                return row_index
        
        return -1
