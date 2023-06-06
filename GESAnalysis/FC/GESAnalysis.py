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
        super().__init__()
        self.__file_open = {} # Dictionary to associate the name of file and his data
        

    def read_file(self, filename: str, year:str, category:str, sep: str = None, engine: str = "pandas") -> None:
        """ Read the file 'filename'

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in 'filename'. Defaults to None.
            engine (str, optional): Reading engine for XLSX files. Defaults to "pandas".
        """
        if filename is None:
            raise Exception("cannot read file because the path is null")
        try:
            data_file = self.__reader.read_file(filename, sep, engine)
            name_file = self.get_filename(filename)
            self.__file_open[name_file] = {}
            self.__file_open[name_file]["data"] = data_file
            self.__file_open[name_file]["year"] = year
            self.__file_open[name_file]["category"] = category
        except Exception as e:
            raise Exception(str(e))
            
            
    def export(self, filein: str, fileout: str) -> None:
        """ Write the current dictionnary into the file 'fileout'

        Args:
            filein (str): Path to the file to read the data
            fileout (str): Path to the file to write the data
        """
        file = self.get_filename(filein)
        # If the file is already open, then we export the data
        if file in self.__file_open.keys():
            try:
                self.__export.export_data(self.__file_open[file]["data"], fileout)
                return
            except Exception as e:
                raise Exception(str(e))
            
        # Else, we read the data and export it
        try:
            data_file = self.__reader.read_file(filein)
            self.__export.export_data(data_file, fileout)
        except Exception as e:
            raise Exception(str(e))
        
        
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
            raise Exception(f"the file '{file}' is not open yet")
        
        
    def get_data(self):
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
    
    
    def get_data_from_file(self, filename:str) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Return the dictionary of data of the last file who was read

        Returns:
            dict: Dictionary of data
        """
        file = self.get_filename(filename)
        try:
            return self.__file_open[file]["data"]
        except:
            raise Exception(f"there is no file '{file}' open")
    

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