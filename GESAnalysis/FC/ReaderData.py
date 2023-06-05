import os
import platform
import csv
import pandas
import openpyxl
from typing import Union, Dict, List, Tuple, Optional


class ReaderData:
    """ Class to read data from a CSV, TSV, TXT or XLSX file
    """
    
    __accepted_extension = [".csv", ".txt", ".tsv", ".xlsx"]
    
    
    # Units accepted for data
    __units = ["t", "kg", "g", "mg",                    # Units for mass
              "km", "hm", "dam", "m", "dm", "cm", "mm", # Units for length
              "co2e"                                    # Unit for CO2
            ]
    
    
    def __init__(self) -> None:
        """ Initialisation of the class
        """
        pass


    def read_file(self, filename: str, sep: str = None, engine: str ='pandas') -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Read the file 'filename' with or without a separator, for CSV, TSV and TXT files, and
            a reading engine, for XLSX files

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in a CSV, TSV and TXT files. Defaults to None
            engine (str, optional): Reading engine for XLSX file (pandas, openpyxl). Defaults to pandas

        Returns:
            dict: Dictionary with the name, unit and data of each column in the file if the reading is correct
            
            Exemple : File format :
                nom_col1,nom_col2.unite,nom_col3.suite_nom.unite,nom_col4.suite_nom.unite.suite_unite
                d11,d12,d13,d14,
                d21,d22,d23,d24
                
            The dictionary will be :
            {
                "nom_col1": { "name": ["nom_col1"], "unit": [], "data": [d11, d21] },
                "nom_col2.unite": { "name": ["nom_col2"], "unit": ["unite"], "data": [d12, d22] },
                "nom_col3.suite_nom.unite": { "name": ["nom_col3", "suite_nom"], "unit": ["unite"], "data": [d13, d23] },
                "nom_col4.suite_nom.unite.suite_unite": { "name": ["nom_col4", "suite_nom"], "unit": ["unite", "suite_unite"], "data": [d14, d24] },
            }
        """
        # Verification of the file
        self.__verify_file(filename)
        
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
        
    
    def __verify_file(self, filename: str) -> None:        
        """ Check if the file 'filename' exists and it can be read

        Args:
            filename (str): Path to file

        Raises:
            FileNotFoundError: 'filename' was not found
            TypeError: 'filename' is not a CSV, TSV, TXT or XLSX file
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
            raise FileNotFoundError(f"file '{file+self.__ext}' not exist")
        
        # Check if the file is supported by the application
        if not self.__ext in self.__accepted_extension:
            raise TypeError(f"cannot read data from '{file+self.__ext}'. Should be a CSV, TSV, TXT or XLSX file")
    
    
    def __detect_delimiter(self, filename: str) -> str:
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
    

    def __read_csv_tsv_txt(self, filename: str, sep:str = ',') -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Reading the data from a CSV, TSV or TXT file and the separator between values

        Args:
            filename (str): Path to file
            sep (str, optional): Separator between values in the file. Defaults to ','

        Raises:
            ValueError: Number of elements in a row is different from the number of columns
            TypeError: the type of an element is different from the element of his column

        Returns:
            dict: Dictionary with the data of file if the reading is correct
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
                
                nb_elems_line = len(list_lines)
                # Check that the number of elements of a row is equal to the number of columns
                if nb_elems_line != nb_column:
                    raise ValueError(f"{nb_elems_line} elements in line {lines_iter+1} but there is {nb_column} columns")
                
                # Add the row elements into data
                # The elements are in a list where the key is the name of the column
                for elem_index in range(len(list_lines)):
                    new_elem = self.__convert_element(list_lines[elem_index])
                    
                    # Check that the element is the same type
                    # If it's the 1st element, we skip it
                    type_new_elem = type(new_elem)
                    type_new_elem_str = str(type_new_elem).split("'")[1]
                    if lines_iter != 1 and not isinstance(data[name_column[elem_index]]["data"][0], type_new_elem):
                        type_elem_ref = type(data[name_column[elem_index]]["data"][0])
                        type_elem_ref_str = str(type_elem_ref).split("'")[1]
                        print(str(type_elem_ref))
                        raise TypeError(f"Element at row {lines_iter+1} and column {'.'.join(data[name_column[elem_index]]['name'])} has type {type_new_elem_str} instead of type {type_elem_ref_str}")
                    
                    # Add into data
                    data[name_column[elem_index]]["data"].append(new_elem)
                    
                # Next line
                lines = file.readline()
                lines = lines.strip('\n')
                lines_iter += 1
                
        return data
    
    
    def __convert_element(self, elem: str) -> Union[bool, str, int, float]:
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
            
    
    def __parser_name_unit(self, name_col: str) -> Tuple[List[str], List[str]]:
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
                - 'distance'            -> (['distance'], [])
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
            return (name_list, [])
        
        return (name_list[0:index_spe_name_unit], name_list[index_spe_name_unit:len(name_list)])


    def __read_xlsx(self, filename: str, engine: str = 'pandas') -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Read a XLSX file with the engine 'pandas' or 'openpyxl'
        Lecture d'un fichier excel avec comme moteur pandas ou openpyxl

        Args:
            filename (str): Path to file
            engine (str, optional): Reading engine ('pandas', 'openpyxl'). Defaults to 'pandas'.

        Raises:
            ValueError: A reading engine different from 'pandas' and 'openpyxl'

        Returns:
            dict: Dictionary with the data of the file if the reading is correct
        """
        match engine:
            case 'pandas':
                return self.__read_xlsx_pandas(filename)
            case 'openpyxl':
                return self.__read_xlsx_openpyxl(filename)
            case _:
                raise ValueError(f"'{engine}' is not an engine to read a file. Use 'pandas' or 'openpyxl'")
            
       
    def __read_xlsx_pandas(self, filename: str) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Read a XLSX file with pandas

        Args:
            filename (str): Path to file

        Raises:
            IOError: A problem occur with read_excel() of pandas

        Returns:
            dict: Dictionary with the data of the file if the reading is correct
        """
        try:
            # Read the file
            data = pandas.read_excel(filename)
            return self.__transform_data_pandas(data.to_dict('split'))       
        except:
            raise IOError("unexcepted problem. Cannot read the excel file with 'pandas'. Try with 'openpyxl'")
    
    
    def __read_xlsx_openpyxl(self, filename: str) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
        """ Read a XLSX file with openpyxl

        Args:
            filename (str): Path to file

        Raises:
            IOError: A problem occur with the functions used with openpyxl

        Returns:
            dict: Dictionary with the data of the file if the reading is correct
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
            raise IOError("unexcepted problem. Cannot read the excel file with 'openpyxl'. Try with 'pandas'")
        
        
    def __transform_data_pandas(self, data: Dict[str, List[Union[str, bool, int, float]]]) -> Dict[str, Dict[str, List[Union[str, int, float, bool]]]]:
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
