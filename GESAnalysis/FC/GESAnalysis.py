import os, platform

from typing import Dict, List, Union
from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.PATTERNS.Observable import Observable
from GESAnalysis.FC.ReaderData import ReaderData


class GESAnalysis(Observable):
    """ Class to manipulate data (Read file, write data)
    """
    
    __reader = ReaderData()
    __export = ExportData()
    
    
    def __init__(self) -> None:
        """ Initialise the class
        """
        super().__init__()
        self.__file_open = {} # Dictionary to associate the name of file and his data
        

#######################################################################################################
#  Read the data from a file                                                                          #
#######################################################################################################
    def read_file(self, filename: str, year:str, category:str, sep: str = None, engine: str = "pandas") -> None:
        """ Read the file 'filename'

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in 'filename'. Defaults to None.
            engine (str, optional): Reading engine for XLSX files. Defaults to "pandas".
        """
        if filename is None:
            raise Exception("Impossible de lire le fichier car le chemin est invalide")
        
        self.__check_year(year)
        
        data_file = self.__reader.read_file(filename, sep, engine)
        name_file = self.get_filename(filename)
        self.__file_open[name_file] = {}
        self.__file_open[name_file]["data"] = data_file
        self.__file_open[name_file]["year"] = year
        self.__file_open[name_file]["category"] = category
        self.__file_open[name_file]["path"] = filename
        self.__sort_by_year()
        
    
    def __sort_by_year(self) -> None:
        """ Sort the dictionary by year
        """
        self.__file_open = dict(sorted(self.__file_open.items(), key=lambda item: item[1]["year"]))
        
    
    def __check_year(self, year: str) -> None:
        """ Check if a year is correct

        Args:
            year (str): Year

        Raises:
            Exception: Year incorrect
        """
        try:
            year_int = int(year)
        except:
            raise Exception(f"'{year}' n'est pas une année")

            
#######################################################################################################
#  Write the data into a file                                                                         #
#######################################################################################################      
    def export(self, filein: str, fileout: str) -> None:
        """ Write the current dictionnary into the file 'fileout'

        Args:
            filein (str): Path to the file to read the data
            fileout (str): Path to the file to write the data
        """
        file = self.get_filename(filein)
        # If the file is already open, then we export the data
        if file in self.__file_open.keys():
            self.__export.export_data(self.__file_open[file]["data"], fileout)
            return
            
        # Else, we read the data and export it
        data_file = self.__reader.read_file(filein)
        self.__export.export_data(data_file, fileout)
        
        
    def export_stat(self, data: List[List[str]], header_column: List[str], header_row: List[str], fileout: str):
        """ Export the stat of data and the headers in the file fileout

        Args:
            data (List[List[str]]): Stats
            header_column (List[str]): Header of columns
            header_row (List[str]): Header of rows
            fileout (str): Path to file to save the stats
        """
        self.__export.export_stat(data, header_column, header_row, fileout)


#######################################################################################################
#  Close a file                                                                                       #
#######################################################################################################  
    def close_file(self, filename: str) -> None:
        """ Remove the data from the dictionary

        Args:
            filename (str): Path to file

        Raises:
            Exception: The data of the file is not in the dictionary
        """
        file = self.get_filename(filename)
        try:
            del self.__file_open[file]
        except:
            raise Exception(f"Le fichier '{file}' n'est pas ouvert")



#######################################################################################################
#  Setters					                                                                          #
#######################################################################################################
    def set_year(self, filename: str, year: str) -> None:
        """ Set the year for the file 'filename'

        Args:
            filename (str): File
            year (str): Year

        Raises:
            Exception: File is not opened or a year is invalid
        """
        file = self.get_filename(filename)
        
        self.__check_year(year)

        try:
            self.__file_open[file]["year"] = year
        except:
            raise Exception(f"Le fichier '{file}' n'est pas ouvert")
        
        
    def set_category(self, filename: str, category: str) -> None:
        """ Set the category for the file 'filename'

        Args:
            filename (str): File
            category (str): Category

        Raises:
            Exception: File is not opened
        """
        file = self.get_filename(filename)
        try:
            self.__file_open[file]["category"] = category
        except:
            raise Exception(f"Le fichier '{file}' n'est pas ouvert")


#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################                   
    def get_data(self) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Get the dictionary of data

        Returns:
            Dict[str, Dict[str, List[Union[str, int, float, bool]]]]: dictionary of data
        """
        return self.__file_open
    
    
    def get_file_open(self) -> List[str]:
        """ Get all the name of file who are open

        Returns:
            List[str]: List of name of file_
        """
        return list(self.__file_open.keys())
    
    
    def get_data_from_file(self, filename:str) -> Dict[str, Dict[str, List[Union[List[Union[int, float, bool, str]], str]]]]:
        """ Return the dictionary of data of the file 'filename'

        Raises:
            Exception: File is not opened
            
        Returns:
            dict: Dictionary of data
        """
        file = self.get_filename(filename)
        try:
            return self.__file_open[file]["data"]
        except:
            raise Exception(f"Le fichier '{file}' n'est pas ouvert")
    

    def get_filename(self, path_file: str) -> str:
        """ Return the name of the file of 'path_file'

        Args:
            path_file (str): path to the file

        Returns:
            str: name of file
        """
        root_filename, file_ext = os.path.splitext(path_file)
        sep_path = '/'
        if platform.system() == "Windows":
            sep_path = '\\'
        split_path = root_filename.split(sep_path)
        return split_path[len(split_path)-1] + file_ext
    
    
    def get_path(self, filename: str) -> str:
        """ Get the path of the file 'filename'

        Args:
            filename (str): File

        Raises:
            Exception: File is not opened

        Returns:
            str: Path
        """
        filename = self.get_filename(filename)
        try:
            return self.__file_open[filename]["path"]
        except:
            raise Exception(f"Le fichier '{filename}' n'est pas ouvert")
    
    
    def get_year(self, filename: str) -> str:
        """ Get the year of the file 'filename'

        Args:
            filename (str): File

        Raises:
            Exception: File is not opened

        Returns:
            str: Year
        """
        filename = self.get_filename(filename)
        try:
            return self.__file_open[filename]["year"]
        except:
            raise Exception(f"Le fichier '{filename}' n'est pas ouvert")
        
    
    def get_category(self, filename: str) -> str:
        """ Get the category of the file 'filename'

        Args:
            filename (str): File

        Raises:
            Exception: File is not opened

        Returns:
            str: Category
        """
        filename = self.get_filename(filename)
        try:
            return self.__file_open[filename]["category"]
        except:
           raise Exception(f"Le fichier '{filename}' n'est pas ouvert")
