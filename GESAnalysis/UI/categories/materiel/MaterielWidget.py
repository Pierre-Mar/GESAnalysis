#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
from typing import List
from PyQt5 import QtWidgets
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.PATTERNS.Observer import Observer
from GESAnalysis.UI.FileOpenUI import FileOpenUI


class MaterielWidget(QtWidgets.QWidget, Observer):
    """ Widget use to regroup the graphs, the files opener and the stats of the category "Materiel"
    """
    
    def __init__(
        self,
        model: GESAnalysis,
        controller: Controleur,
        category: str,
        parent: QtWidgets.QWidget | None = ...
    ) -> None:
        """ Initialise the class

        Args:
            model (GESAnalysis): Model
            controller (Controleur): Controller
            category (str): Category
            parent (QtWidgets.QWidget | None, optional): Parent of this widget. Defaults to ....
        """
        # Initialise the parent class
        super(MaterielWidget, self).__init__(parent)
        
        # Set parameters to attributes
        self.__gesanalysis = model
        self.__controller = controller
        self.__category = category
        
        # Add this widget to the list of observers to update his interface
        self.__gesanalysis.add_observer(self, self.__category)
        
        self.__files = {} # Dictionary where the key is the file in 'category' and a bool if it's read or not
        
        self.__configure_data()
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self):
        """ Initialise the UI for "Materiel"
        """
        # Set parameter of this widget
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Splitter to divide the sections
        splitter = QtWidgets.QSplitter(self)
        
        # Widget for left-splitter (file open + stats)
        splitter_left_widget = QtWidgets.QWidget(splitter)
        splitter_left_layout = QtWidgets.QVBoxLayout(splitter_left_widget)
        self.__file_depl_widget = FileOpenUI(self.__files, self.__category, self.__controller, splitter_left_widget)
        splitter_left_layout.addWidget(self.__file_depl_widget)
        
        # Tab widget for right-splitter (graph)
        self.__tab_graph = QtWidgets.QTabWidget(splitter)
        # TODO : Add graph for "Materiel" here
        
        # Add components to the splitter
        splitter.addWidget(splitter_left_widget)
        splitter.addWidget(self.__tab_graph)
        splitter.setSizes([200, 1000])
        
        # Layout of this widget
        layout_principal = QtWidgets.QHBoxLayout(self)
        layout_principal.addWidget(splitter)
        self.setLayout(layout_principal)
        

#######################################################################################################
#  Configure data                                                                                     #
#######################################################################################################
    def __configure_data(self):
        """ Configure data
        """
        for file, data_file in self.__gesanalysis.get_data().items():
            if data_file["category"] != self.__category:
                continue
            
            # Add file to self.__files and set bool
            self.__files[file] = {"read": True, "warning": [], "year": data_file["year"]}
        

#######################################################################################################
#  Methods associated to an action                                                                    #
#######################################################################################################
    def close_files(self) -> None:
        """ Close files from this widget
        """
        self.__file_depl_widget.close_files()
        

#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def get_selected_files(self) -> List[str]:
        """ Get selected files from FileOpenUI

        Returns:
            List[str]: List of file name's
        """
        return self.__file_depl_widget.get_selected_files()
    

#######################################################################################################
#  Update widgets                                                                                     #
#######################################################################################################   
    def update(self):
        """ Update this widget (from observers)
        """
        self.__files.clear()
        
        self.__configure_data()
        
        # Update FileOpenUI
        self.__file_depl_widget.update_widget(self.__files)
