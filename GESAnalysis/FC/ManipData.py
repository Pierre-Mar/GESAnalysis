from typing import Dict, List, Union
from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData

class ManipData:
    """ Class to manipulate data (Read file, write data)
    """
    
    __reader = ReaderData()
    __export = ExportData()

    
    def __init__(self, filename: str = None) -> None:
        """ Initialisation of the class and read the file 'filename'

        Args:
            filename (str, optional): Path to file to read if he is not equal to None. Defaults to None.
        """
        self.__filename = filename
        self.__data_dict = None
        
        if filename is None:
            return
        
        # Read the file if it's given
        self.__data_dict = self.__reader.read_file(self.__filename)
            

    def read_file(self, filename: str, sep: str = None, engine: str = "pandas") -> None:
        """ Read the file 'filename'

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in 'filename'. Defaults to None.
            engine (str, optional): Reading engine for XLSX files. Defaults to "pandas".
        """
        self.__filename = filename
        self.__data_dict = self.__reader.read_file(filename, sep, engine)
            
            
    def export(self, fileout: str) -> None:
        """ Write the current dictionnary into the file 'fileout'

        Args:
            fileout (str): Path to the file to write the data
        """
        self.__export.export_data(self.__data_dict, fileout)
            
    
    def get_data(self) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Return the dictionary of data of the last file who was read

        Returns:
            dict: Dictionary of data
        """
        return self.__data_dict
    

    def get_filename(self) -> str:
        """ Return the last file who was read

        Returns:
            str: Path to file
        """
        return self.__filename