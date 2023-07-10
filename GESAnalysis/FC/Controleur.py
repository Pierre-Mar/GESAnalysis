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
        
        for file in list_file:
            self.__gesanalysis.close_file(file)
        
        self.__gesanalysis.update(category)


    def open_file(self, file: str, year: str, category: str) -> None:
        """ Open/read a file and associated a year and a category

        Args:
            file (str): Path to file
            year (str): Year
            category (str): Category

        Raises:
            Exception: Exception from read_file
        """
        try:
            self.__gesanalysis.read_file(file, year, category)
            self.__gesanalysis.update(category)
        except Exception as e:
            raise Exception(str(e))


    def export_file(self, filein, fileout):
        try:
            self.__gesanalysis.export(filein, fileout)
        except Exception as e:
            raise Exception(str(e))
        
    
    def set_category_year(self, filename, year, category, old_category):
        try:
            self.__gesanalysis.set_year(filename, year)
            self.__gesanalysis.set_category(filename, category)
            self.__gesanalysis.update(old_category)
            self.__gesanalysis.update(category)
        except Exception as e:
            raise Exception(str(e))