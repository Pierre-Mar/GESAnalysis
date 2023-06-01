import os
import platform


class ExportData:
    """ Class to export data into a CSV, TSV and TXT file
    """
    
    __accepted_extension = [".csv", ".tsv", ".txt"]
    
    def __init__(self):
        """ Initialisation of the class
        """
        self.__error_msg = None
        pass
    

    def export_data(self, data_dict, fileout):
        """ Export the dictionary of data into the file 'fileout'

        Args:
            data_dict (dict): Dictionary of data
            fileout (str): Path to the file to write the data

        Returns:
            bool: True if all the data has been written in the file, else False
        """
        if data_dict is None:
            self.__error_msg = "Erreur : les données ne peuvent pas être lues"
            return False
        
        
        # Check the name of file
        if not self.__verif_fileout(fileout):
            return False
        
        match self.__file_ext:
            case ".csv":
                return self.__write_in_file(data_dict, fileout, ',')
            case ".tsv":
                return self.__write_in_file(data_dict, fileout, '\t')
            case _:
                return self.__write_in_file(data_dict, fileout, ',')
    
    
    def __verif_fileout(self, fileout):
        """ Check 'fileout' if it's a CSV, TSV or TXT file

        Args:
            fileout (str): Path to the file to write the data

        Returns:
            bool: True if the file is a CSV, TSV or TXT file, else False
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
            self.__error_msg = "Erreur : le fichier '{0}' doit être un fichier CSV, TSV ou TXT pour l'exportation".format(
                file + self.__file_ext)
            return False
        
        return True
    
    
    def __write_in_file(self, data, fileout, sep):
        """ Write the dictionary of data into the file 'fileout' where separator between values is 'sep'

        Args:
            data (dict): Dictionary of data
            fileout (str): Path to the file to write the data
            sep (str): Separator between values

        Returns:
            bool: True if the data is write into the file, else False
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
                print(elems_columns)
                if not self.__verif_number_lines(elems_columns):
                    file_out.close()
                    os.remove(fileout)
                    return False
                
                nb_lines = len(elems_columns[0])
                for l in range(nb_lines):
                    ph = ""
                    for c in range(nb_columns):
                        if c == nb_columns-1:
                            ph += str(elems_columns[c][l]) + '\n'
                        else:
                            ph += str(elems_columns[c][l]) + sep
                    
                    file_out.write(ph)
        except:
            self.__error_msg = "Erreur : problème rencontré pendant l'exportation"
            os.remove(fileout)
            return False
            
        return True
    
    
    def __verif_number_lines(self, elems_col):
        """ Check that the number of elements of each row is the same

        Args:
            elems_col (list): List where the values of each columns is in a list

        Returns:
            bool: True if this number is equal, else False
        """
        nb_elements = len(elems_col[0])
        for i in range(1, len(elems_col)):
            if len(elems_col[i]) != nb_elements:
                self.__error_msg = "Erreur : Le nombre d'éléments de la ligne {0} est différent".format(i+1)
                return False
            
        return True


    def __get_data(self, data_dict):
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
    
    
    def get_error(self):
        """ Return the last error message

        Returns:
            str: Error message
        """
        return self.__error_msg
