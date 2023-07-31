#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
from typing import Optional
from PyQt5 import QtWidgets
from GESAnalysis.UI import common


class ChangeNacresCodeDialog(QtWidgets.QDialog):
    """ Dialog to change the NACRES key code
    """
    
    
    def __init__(self, old_code, parent: QtWidgets.QWidget | None = ...) -> None:
        """ Initialise the dialog

        Args:
            parent (QtWidgets.QWidget | None, optional): Parent of this dialog. Defaults to ....
        """
        super(ChangeNacresCodeDialog, self).__init__(parent)
        
        self.selected_code = None # NACRES code
        self.old_code = old_code
        
        self.__init_UI()
        

#######################################################################################################
#  Initialise the UI                                                                                  #
#######################################################################################################
    def __init_UI(self) -> None:
        """ Initialise the UI
        """
        # Set parameters to this dialog
        self.setWindowTitle("Changer code NACRES")
        self.setFixedWidth(600)
        
        # Create the dialog box with the button 'Ok' and 'Cancel'
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        buttons_box = QtWidgets.QDialogButtonBox(buttons)
        buttons_box.accepted.connect(self.accept)
        buttons_box.rejected.connect(self.reject)
        
        # Create a form widget to enter the new code
        form_widget = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout(form_widget)
        form_widget.setLayout(form_layout)
        
        # Label and lineedit to enter the new code
        enter_code_label = QtWidgets.QLabel("Code :", form_widget)
        self.enter_code_lineedit = QtWidgets.QLineEdit(form_widget)
        self.enter_code_lineedit.setPlaceholderText(self.old_code)
        
        form_layout.addRow(enter_code_label, self.enter_code_lineedit)
        
        # Layout of this dialog
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(form_widget)
        layout.addWidget(buttons_box)
        self.setLayout(layout)
        
        
#######################################################################################################
#  Methods connected to an action                                                                     #
#######################################################################################################
    def accept(self) -> None:
        """ When the user click on the button 'Ok', we get the NACRES code in the lineedit.
            After that, we do a lexical and semantic analysis 
        """
        self.selected_code = self.enter_code_lineedit.text()
        
        # Correction of the selected code
        self.__correction_code()
        
        # If the code is the same as the previous code, then no need to analyse this code and update the graph
        if self.selected_code == self.old_code:
            super().reject()
        
        # Lexical analysis
        token_not_accepted = self.__analyse_lexical(self.selected_code)
        if token_not_accepted is not None:
            common.message_error(f"Token '{token_not_accepted}' non-reconnu", self)
            return
        
        # Semantic analysis
        self.selected_code += '/' # Add '/' to notice the end of the string
        if not self.__semantic_analysis(self.selected_code):
            common.message_error("Erreur dans le code lors de l'analyse sémantique", self)
            return
        # Remove '/'
        self.selected_code = self.selected_code.rstrip(self.selected_code[-1])
        
        # The lexical and semantic analysis are correct, so we can close this dialog
        super().accept()
        
    
    def __correction_code(self) -> None:
        """ Correct the code enter by the user by removing " ", '.'. Remove also the last character
        if it's ';'
        """
        # If the lineedit is empty, we get the previous code
        if self.selected_code == "":
            self.selected_code = self.old_code
        self.selected_code = self.selected_code.upper() # Up the minuscule letters
        
        # Remove all the space in the code
        try:
            self.selected_code = self.selected_code.replace(" ", "")
        except:
            pass
        
        # Same with "."
        try:
            self.selected_code = self.selected_code.replace(".", "")
        except:
            pass
        
        # Remove the last character if it's ';'
        if self.selected_code[len(self.selected_code) - 1] == ';':
            self.selected_code = self.selected_code.rstrip(self.selected_code[-1])
        

#######################################################################################################
#  Lexical Analysis                                                                                   #
#######################################################################################################
    def __analyse_lexical(self, code:str) -> Optional[str]:
        """ Do a lexical analyse to the code

        Args:
            code (str): Code

        Returns:
            Optional[str]: A letter if it's not a token, else None
        """
        for c in code:
            if not self.__token_accepted(c):
                return c
        return None


    def __token_accepted(self, letter_code: str) -> bool:
        """ Return True if the letter is a token of the lexical analysis, else False.
            Token accepted = { {'A', ..., 'Z'}, ';', '*', {'0', ..., '9'} }

        Args:
            letter_code (str): letter

        Returns:
            bool: True if the letter is a token of the lexical analysis, else False
        """
        if letter_code == ";" or letter_code == "*":
            return True
        if 'A' <= letter_code and letter_code <= 'Z':
            return True
        if '0' <= letter_code and letter_code <= '9':
            return True
        return False


#######################################################################################################
#  Semantic Analysis                                                                                  #
#######################################################################################################
    def __semantic_analysis(self, code:str) -> bool:
        """ Do the semantic analysis of code and a return a boolean if the analysis is correct or not

        Args:
            code (str): Code

        Returns:
            bool: True if the analyse of code is correct, else False
        """
        return self.__A(code, 0)
    
    #-- Methods uses for the parsing --#
    def __A(self, code: str, index: int) -> bool:
        if 'A' <= code[index] and code[index] <= 'Z':
            return self.__B(code, index + 1)
        elif code[index] == '*':
            return self.__F(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
    
    def __B(self, code: str, index: int) -> bool:
        if 'A' <= code[index] and code[index] <= 'Z':
            return self.__C(code, index + 1)
        elif code[index] == '*':
            return self.__G(code, index + 1)
        else:
            return False
    
    def __C(self, code: str, index: int) -> bool:
        if '0' <= code[index] and code[index] <= '9':
            return self.__D(code, index + 1)
        elif code[index] == '*':
            return self.__J(code, index + 1)
        else:
            return False
    
    def __D(self, code: str, index: int) -> bool:
        if '0' <= code[index] and code[index] <= '9':
            return self.__E(code, index + 1)
        elif code[index] == '*':
            return self.__M(code, index + 1)
        else:
            return False
    
    def __E(self, code: str, index: int) -> bool:
        if code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
    
    def __F(self, code: str, index: int) -> bool:
        if 'A' <= code[index] and code[index] <= 'Z':
            return self.__C(code, index + 1)
        elif '0' <= code[index] and code[index] <= '9':
            if ('0' <= code[index+1] and code[index+1] <= '9') or code[index+1] == '*':
                return self.__D(code, index + 1)
            else:
                return self.__E(code, index + 1)
        elif code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False

    def __G(self, code: str, index: int) -> bool:
        if '0' <= code[index] and code[index] <= '9':
            return self.__H(code, index + 1)
        elif code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
        
    def __H(self, code: str, index: int) -> bool:
        if '0' <= code[index] and code[index] <= '9':
            return self.__I(code, index + 1)
        elif code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
        
    def __I(self, code: str, index: int) -> bool:
        if code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
    
    def __J(self, code: str, index: int) -> bool:
        if '0' <= code[index] and code[index] <= '9':
            return self.__K(code, index + 1)
        elif code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
        
    def __K(self, code: str, index: int) -> bool:
        if code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
        
    def __M(self, code: str, index: int) -> bool:
        if code[index] == ';':
            return self.__A(code, index + 1)
        elif code[index] == '/':
            return self.__T()
        else:
            return False
                    
    def __T(self):
        return True
