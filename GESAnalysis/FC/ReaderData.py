import os
import platform
import csv
import pandas
import openpyxl


class ReaderData:
    """ Class to read data from a CSV, TSV, TXT or XLSX file
    """
    
    __accepted_extension = [".csv", ".txt", ".tsv", ".xlsx"]
    
    
    # Units accepted for data
    __units = ["t", "kg", "g", "mg",                    # Units for mass
              "km", "hm", "dam", "m", "dm", "cm", "mm", # Units for length
              "co2e"                                    # Unit for CO2
            ]
    
    
    def __init__(self):
        """ Initialisation of the class
        """
        self.__error_msg = None


    def read_file(self, filename, sep=None, engine='pandas'):
        """ Read the file 'filename' with or without a separator, for CSV, TSV and TXT files, and
            a reading engine, for XLSX files

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in a CSV, TSV and TXT files. Defaults to None
            engine (str, optional): Reading engine for XLSX file (pandas, openpyxl). Defaults to pandas

        Returns:
            dict | None: Dictionary with the name, unit and data of each column in the file if the reading is correct. Else None
            Exemple : File format :
                nom_col1,nom_col2.unite,nom_col3.suite_nom.unite,nom_col4.suite_nom.unite.suite_unite
                d11,d12,d13,d14,
                d21,d22,d23,d24
                
            The dictionary will be :
            {
                "nom_col1": { "name": ["nom_col1"], "unit": None, "data": [d11, d21] },
                "nom_col2.unite": { "name": ["nom_col2"], "unit": ["unite"], "data": [d12, d22] },
                "nom_col3.suite_nom.unite": { "name": ["nom_col3", "suite_nom"], "unit": ["unite"], "data": [d13, d23] },
                "nom_col4.suite_nom.unite.suite_unite": { "name": ["nom_col4", "suite_nom"], "unit": ["unite", "suite_unite"], "data": [d14, d24] },
            }
        """
        # Verification of the file
        if not self.__verify_file(filename):
            return None
        
        # Reading of the CSV, TSV or TXT file with a separator
        if self.__ext in [".csv", ".tsv", ".txt"]:
            # If it's a TSV file, then the separator is '\t'
            if self.__ext == ".tsv":
                delimiter = "\t"
            delimiter = sep
            # If the separator is not given, then it automatically detects
            if delimiter is None:
                delimiter = self.__detect_delimiter(filename)
            return self.__read_csv_tsv_txt(filename, delimiter)
        
        # If it's not a CSV, TSV or TXT file, then it's a XLSX file
        return self.__read_xlsx(filename, engine)
        
    
    def __verify_file(self, filename):
        """ Check if the file 'filename' exists and it can be read

        Args:
            filename (str): Path to file

        Returns:
            bool: Return True if the file exists and it can be read, else False
        """
        root_filename, self.__ext = os.path.splitext(filename)
        
        # Get the name of file and remove the path
        # The path is different between OS
        os_name = platform.system()
        sep_path = '/'
        if os_name == "Windows":
            sep_path = '\\'
        path_to_file = root_filename.split(sep_path)
        file = path_to_file[len(path_to_file) - 1]
        
        # Check if the file exists
        if not os.path.isfile(filename):
            self.__error_msg = "Erreur : Le fichier '{0}' n'existe pas".format(file + self.__ext)
            return False
        
        # Check if the file is supported by the application
        root_filename, self.__ext = os.path.splitext(filename)
        if not self.__ext in self.__accepted_extension:
            self.__error_msg = "Erreur : Le fichier '{0}' n'est pas pris en charge par l'application".format(file + self.__ext)
            return False
        return True
    
    
    def __detect_delimiter(self, filename):
        """ Detects the separator inside the file 'filename'

        Args:
            filename (str): Path to file

        Returns:
            str: The separator inside the file
        """
        sniffer = csv.Sniffer()
        
        # Get the 1st line (column names) to found the separator
        head_line = None
        with open(filename, "r") as f:
            head_line = f.readline()
        
        dialect = sniffer.sniff(head_line)
        return dialect.delimiter
    

    def __read_csv_tsv_txt(self, filename, sep=','):
        """ Reading the data from a CSV, TSV or TXT file and the separator between values

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in the file. Defaults to ','

        Returns:
            dict | None: Dictionary with the data of file if the reading is correct, else None
        """
        data = {}
        with open(filename, "r") as file:
            # Read the 1st line (column names)
            column = file.readline()
            
            # Remove useless caracters (encoding + end of line)
            column = column.strip("\ufeff")
            column = column.strip("ï»¿")
            column = column.strip("\n")
            name_column = column.split(sep)
            nb_column = len(name_column) # Number of columns

            # Add into data (dictionary)
            # Each key correspond to a column
            for i in range(nb_column):
                data[name_column[i]] = {}
                n, u = self.__parser_name_unit(name_column[i])
                data[name_column[i]]["name"] = n
                data[name_column[i]]["unit"] = u
                data[name_column[i]]["data"] = []
            
            # Read the rest of the file
            lines = file.readline()
            lines = lines.strip('\n')
            lines_iter = 1
            while lines != "":
                list_lines = lines.split(sep)
                
                # Check that the number of elements of a row is equal to the number of columns
                if len(list_lines) != nb_column:
                    self.__error_msg = "Erreur : le nombre d'éléments à la ligne {0} est différent du nombre de colonnes {1}".format(
                        lines_iter, nb_column
                    )
                    return None
                
                # Add the row elements into data
                # The elements are in a list where the key is the name of the column
                for elem_index in range(len(list_lines)):
                    new_elem = self.__convert_element(list_lines[elem_index])
                    
                    # Check that the element is the same type
                    # If it's the 1st element, we skip it
                    if lines_iter != 1 and type(new_elem) != type(data[name_column[elem_index]]["data"][0]):
                        self.__error_msg = "Erreur : L'élément de la colonne {0} et de la ligne {1} est différent des éléments de cette colonne".format(
                            name_column[elem_index], lines_iter
                        )
                        return None
                    
                    # Add into data
                    data[name_column[elem_index]]["data"].append(new_elem)
                    
                # Next line
                lines = file.readline()
                lines = lines.strip('\n')
                lines_iter += 1
                
        return data
    
    
    def __convert_element(self, elem):
        """ Convert the element 'elem' in his corresponding type

        Args:
            elem (str): Element to convert

        Returns:
            bool | int | float | str : Element in the good type
        """
        # Check if elem is a boolean
        if elem.lower() == "true":
            return True
        elif elem.lower() == "false":
            return False

        # Check each type to get the good type
        contructors = [int, float, str]
        for c in contructors:
            try:
                return c(elem)
            except ValueError:
                pass
            
    
    def __parser_name_unit(self, name_col):
        """ Parse the 'name' of a column to get the 'original' name and the unit

        Args:
            name_col (str): Format of the column name :
                - nom
                - nom.unite
                - nom.nom.unite
                - nom.unite
                - nom.nom.unite.unite
                etc...

        Returns:
            tuple: Returns a tuple with the name and the unit of 'name_col'.
            For example :
                - 'distance'            -> (['distance'], None)
                - 'distance.km'         -> (['distance'], ['km'])
                - 'vitesse.km.h'        -> (['vitesse'], ['km', 'h'])
                - 'temps.distance.km.h' -> (['temps', 'distance'], ['km', 'h'])
        """
        name_list = name_col.split('.')
        
        # Search the index of the 1st unit
        index_spe_name_unit = -1
        for i in range(len(name_list)):
            if name_list[i] in self.__units:
                index_spe_name_unit = i
                break
        
        # If there are no units, then there is only the name of the column
        if index_spe_name_unit == -1:
            return (name_list, None)
        
        return (name_list[0:index_spe_name_unit], name_list[index_spe_name_unit:len(name_list)])


    def __read_xlsx(self, filename, engine='pandas'):
        """ Read a XLSX file with the engine 'pandas' or 'openpyxl'
        Lecture d'un fichier excel avec comme moteur pandas ou openpyxl

        Args:
            filename (str): Path to file
            engine (str, optional): Reading engine ('pandas', 'openpyxl'). Defaults to 'pandas'.

        Returns:
            dict | None: Dictionary with the data of the file if the reading is correct, else None
        """
        match engine:
            case 'pandas':
                return self.__read_xlsx_pandas(filename)
            case 'openpyxl':
                return self.__read_xlsx_openpyxl(filename)
            case _:
                self.__error_msg = "Erreur : La lecture des fichiers excel se fait soit avec 'pandas', soit 'openpyxl'"
                return None
            
       
    def __read_xlsx_pandas(self, filename):
        """ Read a XLSX file with pandas

        Args:
            filename (str): Path to file

        Returns:
            dict | None: Dictionary with the data of the file if the reading is correct, else None
        """
        try:
            # Read the file
            data = pandas.read_excel(filename)
            return self.__transform_data_pandas(data.to_dict('split'))       
        except:
            self.__error_msg = "Erreur : Problème rencontré. Impossibilité de charger le fichier excel avec pandas.\n Essayez avec un autre moteur"
            return None
    
    
    def __read_xlsx_openpyxl(self, filename):
        """ Read a XLSX file with openpyxl

        Args:
            filename (str): Path to file

        Returns:
            dict | None: Dictionary with the data of the file if the reading is correct, else None
        """
        try:
            # Open the file and activate the sheet
            wb = openpyxl.load_workbook(filename=filename)
            sheet = wb.active
            
            # Get the number of rows and columns
            nb_columns = sheet.max_column
            nb_rows = sheet.max_row
            
            data = {}
            name_column = []
            # Read the 1st line to get the name of columns
            for col in range(1, nb_columns+1):
                # Get the value in the cell of row 1 and column col
                cell = sheet.cell(row=1, column=col)
                data[str(cell.value)] = {}
                n, u = self.__parser_name_unit(str(cell.value))
                data[str(cell.value)]["name"] = n
                data[str(cell.value)]["unit"] = u
                data[str(cell.value)]["data"] = []
                name_column.append(str(cell.value))
                
            # Read data
            for row in range(2, nb_rows+1):
                # Get the value in the cell of row row and column col
                for col in range(1, nb_columns+1):
                    cell = sheet.cell(row=row, column=col)
                    data[name_column[col-1]]["data"].append(cell.value)

            return data
        except:
            self.__error_msg = "Erreur : Problème rencontré. Impossibilité de charger le fichier excel avec openpyxl.\n Essayez avec un autre moteur"
            return None
        
        
    def __transform_data_pandas(self, data):
        """ Transorm a dictionary from pandas to our corresponding dictionary
        Pandas dictionary:
        {
            'index': [rows name],
            'columns: [columns name],
            'data': [list of elements for each row]
        }

        Args:
            data (dict): Pandas dictionary

        Returns:
            dict: Dictionary with the corresponding format
        """
        columns = data['columns']
        values_columns = data['data']
        data_transform = {}
        for c in range(len(columns)):
            data_transform[str(columns[c])] = {}
            n, u = self.__parser_name_unit(str(columns[c]))
            data_transform[str(columns[c])]["name"] = n
            data_transform[str(columns[c])]["unit"] = u
            data_transform[str(columns[c])]["data"] = []
            for l in range(len(values_columns)):
                data_transform[str(columns[c])]["data"].append(values_columns[l][c])
        return data_transform

    
    def get_error(self):
        """ Returns the last error message

        Returns:
            str: Error message
        """
        return self.__error_msg
