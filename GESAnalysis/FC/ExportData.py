import os
import platform
from typing import Optional, Union, Dict, List


class ExportData:
    """ Class to export data into a CSV, TSV and TXT file
    """
    __accepted_extension = [".csv", ".tsv", ".txt"]
    
    def __init__(self) -> None:
        """ Initialisation of the class
        """
        pass
    

#######################################################################################################
#  Export the data to a file                                                                          #
#######################################################################################################
    def export_data(
        self,
        data_dict: Optional[Dict[str, Dict[str, List[Union[List[Union[int, float, bool, str]], str]]]]],
        fileout: str
    ) -> bool:
        """ Export the dictionary of data into the file 'fileout'

        Args:
            data_dict (dict | None): Dictionary of data
            fileout (str): Path to the file to write the data

        Raises:
            TypeError: Dictionary of data is None

        Returns:
            bool: True if all the data has been written in the file
        """
        if data_dict is None:
            raise TypeError("Accès impossible au données car le dictionnaire est invalide")
        
        # Check the name of file
        self.__verif_fileout(fileout)
        
        if self.__file_ext == ".csv":
            return self.__write_in_file(data_dict, fileout, ';')
        elif self.__file_ext == ".tsv":
            return self.__write_in_file(data_dict, fileout, '\t')
        else:
            return self.__write_in_file(data_dict, fileout, ';')


    def __verif_fileout(self, fileout: str) -> None:
        """ Check 'fileout' if it's a CSV, TSV or TXT file

        Args:
            fileout (str): Path to the file to write the data

        Raises:
            Exception: 'fileout' is not a CSV, TSV or TXT file
        """
        # Get the extension of the file
        root_filename, self.__file_ext = os.path.splitext(fileout)
        
        # Get the name of the file, remove the path
        # The path is different between OS
        os_name = platform.system()
        sep_path = '/'
        if os_name == "Windows":
            sep_path = '\\'
        path_to_file = root_filename.split(sep_path)
        file = path_to_file[len(path_to_file) - 1]
        
        if not self.__file_ext in self.__accepted_extension:
            raise Exception(f"Exportation impossible de '{file+self.__file_ext}'. Le fichier doit être de type CSV, TSV ou TXT")
    

#######################################################################################################
#  Write the data into the file                                                                       #
#######################################################################################################
    def __write_in_file(
        self,
        data: Dict[str, Dict[str, List[Union[List[Union[int, float, bool, str]], str]]]],
        fileout: str,
        sep: str
    ) -> bool:
        """ Write the dictionary of data into the file 'fileout' where separator between values is 'sep'

        Args:
            data (dict): Dictionary of data
            fileout (str): Path to the file to write the data
            sep (str): Separator between values

        Raises:
            IOError: A problem occur when trying to open the file or writing into it
            ValueError: Number of elements between rows is different

        Returns:
            bool: True if all the data was written into the file
        """
        try:
            with open(fileout, "w") as file_out:
                # Write columns
                columns = list(data.keys())
                nb_columns = len(columns)
                name_columns = sep.join(columns) + '\n'
                
                file_out.write(name_columns)
                
                # Write row
                elems_columns = self.__get_data(data)
                
                # Check number of elements in the line
                self.__verif_number_lines(elems_columns)
                
                nb_lines = len(elems_columns[0])
                for l in range(nb_lines):
                    ph = ""
                    for c in range(nb_columns):
                        # Transform all elements into string
                        elem_col_str = [str(x) for x in elems_columns[c][l]]
                        # Add separator depending on which column
                        if c == nb_columns-1:
                            ph += ','.join(elem_col_str) + '\n'
                        else:
                            ph += ','.join(elem_col_str) + sep
                    
                    file_out.write(ph)
        # if we catch an error, we remove the file
        except IOError:
            os.remove(fileout)
            raise IOError(f"Problème rencontré pendant l'écriture du fichier '{fileout}'")
        except ValueError as v:
            os.remove(fileout)
            raise ValueError(str(v))
        return True
    
    
    def __verif_number_lines(self, elems_col: List[List[Union[bool, str, float, int]]]) -> None:
        """ Check the number of elements of each row is the same

        Args:
            elems_col (list): List where the values of each columns is in a list

        Raises:
            ValueError: This number is not equal for each row
        """
        nb_elements = len(elems_col[0])
        for i in range(1, len(elems_col)):
            nb_elements_line = len(elems_col[i])
            if nb_elements_line != nb_elements:
                raise ValueError(f"La ligne {i+1} a {nb_elements_line} éléments au lieu de {nb_elements} éléments")


#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
    def __get_data(
        self,
        data_dict: Dict[str, Dict[str, List[Union[List[Union[int, float, bool, str]], str]]]]
    ) -> List[List[Union[bool, str, float, int]]]:
        """ Get the data of each column and put it in a list

        Args:
            data_dict (dict): Dictionary of data

        Returns:
            list: List where the values of each columns is in a list
        """
        val = list(data_dict.values())
        list_data = []
        for l in val:
            list_data.append(l["data"])
        return list_data
