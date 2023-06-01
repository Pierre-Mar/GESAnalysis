from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData

class ManipData:
    """ Class to manipulate data (Read file, write data)
    """
    
    __reader = ReaderData()
    __export = ExportData()

    
    def __init__(self, filename=None):
        """ Initialisation of the class and read the file 'filename'

        Args:
            filename (str, optional): Path to file to read if he is not equal to None. Defaults to None.
        """
        self.__filename = filename
        self.__error_msg = None
        self.__data_dict = None
        
        if filename is None:
            return
        
        # Read the file if it's given
        self.__data_dict = self.__reader.read_file(self.__filename)
        if self.__data_dict == None:
            self.__error_msg = self.__reader.get_error()
            

    def read_file(self, filename, sep=None, engine="pandas"):
        """ Read the file 'filename'

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in 'filename'. Defaults to None.
            engine (str, optional): Reading engine for XLSX files. Defaults to "pandas".
        """
        self.__filename = filename
        self.__data_dict = self.__reader.read_file(filename, sep, engine)
        if self.__data_dict == None:
            self.__error_msg = self.__reader.get_error()
            
            
    def export(self, fileout):
        """ Write the current dictionnary into the file 'fileout'

        Args:
            fileout (str): Path to the file to write the data
        """
        if not self.__export.export_data(self.__data_dict, fileout):
            self.__error_msg = self.__export.get_error()
            
            
    def get_error(self):
        """ Return the last error message

        Returns:
            str: Error message
        """
        return self.__error_msg
    
    def get_data(self):
        """ Return the dictionary of data of the last file who was read

        Returns:
            dict: Dictionary of data
        """
        return self.__data_dict
    
    def get_filename(self):
        """ Return the last file who was read

        Returns:
            str: Path to file
        """
        return self.__filename