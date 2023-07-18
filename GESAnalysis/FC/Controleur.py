from typing import List

from GESAnalysis.FC.GESAnalysis import GESAnalysis

class Controleur:
    """ Class to change the data of the model when
        there is an input from the UI
    """
    
    def __init__(self, model: GESAnalysis) -> None:
        """ Initialise a controller

        Args:
            model (GESAnalysis): Model of the UI, contains the data
        """
        self.__gesanalysis = model
        
        
    def close_files(self, list_file: List[str], category: str) -> None:
        """ Close a list of files from a category

        Args:
            list_file (List[str]): a path to the file
            category (str): Category
        """
        # if the list is empty, no need to update the model
        if not len(list_file):
            return
        
        # Close each file in the model
        for file in list_file:
            self.__gesanalysis.close_file(file)
        
        self.__gesanalysis.update(category)


    def open_file(self, file: str, year: str, category: str) -> None:
        """ Open/read a file and associated a year and a category

        Args:
            file (str): Path to file
            year (str): Year
            category (str): Category
        """
        self.__gesanalysis.read_file(file, year, category)
        self.__gesanalysis.update(category)


    def export_file(self, filein: str, fileout: str) -> None:
        """ Export the data of filein in fileout

        Args:
            filein (str): Path of file to export
            fileout (str): Path of file to save the data
        """
        self.__gesanalysis.export(filein, fileout)


    def export_stat(self, data: List[List[str]], header_column: List[str], header_row: List[str], fileout: str):
        """Export the stat of data whis the header of columns and rows in the file 'fileout'

        Args:
            data (List[List[str]]): Data
            header_column (List[str]): Header of columns
            header_row (List[str]): Header of rows
            fileout (str): Path to file to save data
        """
        self.__gesanalysis.export_stat(data, header_column, header_row, fileout)
        
    
    def set_category_year(self, filename: str, year: str, category: str, old_category: str):
        """ Set the new year and category of a file

        Args:
            filename (str): File
            year (str): New year
            category (str): New category
            old_category (str): Old category
        """
        self.__gesanalysis.set_year(filename, year)
        self.__gesanalysis.set_category(filename, category)
        self.__gesanalysis.update(old_category)
        self.__gesanalysis.update(category)
