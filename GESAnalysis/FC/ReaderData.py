import os
import csv
import pandas
import openpyxl


class ReaderData:
    """ Classe permettant la lecture des données depuis un fichier csv, tsv, txt et xlsx
    """
    
    __accepted_extension = [".csv", ".txt", ".tsv", ".xlsx"]
    
    def __init__(self):
        self.__error_msg = None

        
    def read_file(self, filename, sep=None, engine='pandas'):
        """ Lecture du fichier filename avec ou sans délimiteur

        Args:
            filename (str): chemin vers le fichier
            sep (str, optional): délimiteur pour les fichiers csv, tsv et txt. Par défaut None.
            engine (str, optional): Moteur pour la lecture des fichiers excel (pandas, openpyxl). Par défaut pandas

        Returns:
            dict | None: Dictionnaire avec les données du fichier si la lecture est correcte, sinon None
        """
        # Vérification du fichier
        if not self.__verify_file(filename):
            return None
        
        # Lecture du fichier csv, tsv ou txt avec le délimiteur
        if self.__ext in [".csv", ".tsv", ".txt"]:
            # Si le delimiteur n'est pas indiqué, on le détectes automatiquement
            delimiter = sep
            if delimiter is None:
                delimiter = self.__detect_delimiter(filename)
            return self.__read_csv_tsv_txt(filename, delimiter)
        
        # Si ce n'est aucun des 3 extensions, alors on lit le fichier xlsx
        return self.__read_xlsx(filename, engine)
        
    
    def __verify_file(self, filename):
        """ Vérifie que le fichier existe et qu'il peut être lu

        Args:
            filename (str): chemin vers le fichier

        Returns:
            bool: retourne Vrai si le fichier existe et qu'il peut être lu, sinon Faux
        """
        root_filename, self.__ext = os.path.splitext(filename)
        
        # Récupère le nom du fichier, en enlevant son chemin
        path_to_file = root_filename.split('/')
        file = path_to_file[len(path_to_file) - 1]
        
        # Vérifie que le fichier existe
        if not os.path.isfile(filename):
            self.__error_msg = "Erreur : Le fichier '{0}' n'existe pas".format(file + self.__ext)
            return False
        
        # Vérifie que le fichier soit supportable
        root_filename, self.__ext = os.path.splitext(filename)
        if not self.__ext in self.__accepted_extension:
            self.__error_msg = "Erreur : Le fichier '{0}' n'est pas pris en charge par l'application".format(file + self.__ext)
            return False
        return True
    
    
    def __detect_delimiter(self, filename):
        """ Détectes le délimiteur qui se trouve dans le fichier filename

        Args:
            filename (str): chemin vers le fichier

        Returns:
            str: le délimiteur dans le fichier filename
        """
        sniffer = csv.Sniffer()
        
        # Récupère la 1ère ligne (nom des colonnes)
        # pour trouver le délimiteur
        head_line = None
        with open(filename, "r") as f:
            head_line = f.readline()
        
        dialect = sniffer.sniff(head_line)
        return dialect.delimiter
    

    def __read_csv_tsv_txt(self, filename, sep=','):
        """ Lecture des données depuis un fichier csv, tsv ou txt et un délimiteur

        Args:
            filename (str): chemin vers le fichier
            sep (str, optional): un délimiteur dans le fichier filename. Par défaut ','.

        Returns:
            dict | None: Dictionnaire avec les données du fichier si la lecture est correcte, sinon None
        """
        data = {}
        with open(filename, "r") as file:
            # Lecture de la 1ère ligne (contient le nom des colonnes)
            column = file.readline()
            
            # Enlève les caractères inutiles
            column = column.strip("\ufeff") 
            column = column.strip("\n")
            name_column = column.split(sep)
            nb_column = len(name_column) # Nombre de colonnes
            
            # Ajout dans data
            # Chaque clé correspond au nom d'une colonne
            for i in range(nb_column):
                data[name_column[i]] = []
            
            # Lecture du reste des lignes
            lines = file.readline()
            lines = lines.strip('\n')
            lines_iter = 1
            while lines != "":
                list_lines = lines.split(sep)
                
                # Vérifie que le nombre d'éléments de la ligne est égal au nombre de colonnes
                if len(list_lines) != nb_column:
                    self.__error_msg = "Erreur : le nombre d'éléments à la ligne {0} est différent du nombre de colonnes {1}".format(
                        lines_iter, nb_column
                    )
                    return None
                
                # Ajout des éléments d'une ligne dans data
                # Les éléments se trouvent dans une liste où la clé est le nom de la colonne
                for elem_index in range(len(list_lines)):
                    new_elem = self.__convert_element(list_lines[elem_index])
                    
                    # Vérifie que l'élément est du bon type
                    # Si c'est le 1er élément, on le saute
                    if lines_iter != 1 and type(new_elem) != type(data[name_column[elem_index]][0]):
                        self.__error_msg = "Erreur : L'élément de la colonne {0} et de la ligne {1} est différent des éléments de cette colonne".format(
                            name_column[elem_index], lines_iter
                        )
                        return None
                    
                    # Ajout dans data
                    data[name_column[elem_index]].append(new_elem)
                    
                # Ligne suivante
                lines = file.readline()
                lines = lines.strip('\n')
                lines_iter += 1
                
        return data
    
    def __convert_element(self, elem):
        """ Convertit l'élément elem dans son bon type

        Args:
            elem (str): élément à convertir

        Returns:
            bool | int | float | str : l'élément dans son bon type
        """
        # Vérifie d'abord si elemn est un booléen
        if elem.lower() == "true":
            return True
        elif elem.lower() == "false":
            return False

        # Test chaque type pour trouver le bon type
        contructors = [int, float, str]
        for c in contructors:
            try:
                return c(elem)
            except ValueError:
                pass


    def __read_xlsx(self, filename, engine='pandas'):
        """ Lecture d'un fichier excel avec comme moteur pandas ou openpyxl

        Args:
            filename (str): chemin vers le fichier
            engine (str, optional): Moteur de lecture, soit pandas, soit openpyxl. Defaults to 'pandas'.

        Returns:
            dict | None: Dictionnaire avec les données du fichier si la lecture est correcte, sinon None
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
        """ Lecture d'un fichier excel avec pandas

        Args:
            filename (str): chemin vers le fichier

        Returns:
            dict | None: Dictionnaire avec les données du fichier si la lecture est correcte, sinon None
        """
        try:
            # Lecture du fichier
            data = pandas.read_excel(filename)
            # retourne un dictionnaire de la même forme qu'avec des fichiers csv, tsv et txt
            return self.__transform_data_pandas(data.to_dict('split'))       
        except:
            self.__error_msg = "Erreur : Problème rencontré. Impossibilité de charger le fichier excel avec pandas.\n Essayez avec un autre moteur"
            return None
    
    
    def __read_xlsx_openpyxl(self, filename):
        """ Lecture d'un fichier excel avec openpyxl

        Args:
            filename (str): chemin vers le fichier

        Returns:
            dict | None: Dictionnaire avec les données du fichier si la lecture est correcte, sinon None
        """
        try:
            # Ouverture du fichier et activation de la feuille de calcul
            wb = openpyxl.load_workbook(filename=filename)
            sheet = wb.active
            
            # On récupère le nombre de lignes et de colonnes du fichier
            nb_columns = sheet.max_column
            nb_rows = sheet.max_row
            
            data = {}
            name_column = []
            # Lit la 1ère ligne pour déterminer le nom des colonnes
            # et des clés pour data
            for col in range(1, nb_columns+1):
                # On récupère la valeur dans la cellule de la ligne 1 et de colonne col
                cell = sheet.cell(row=1, column=col)
                data[str(cell.value)] = []
                name_column.append(str(cell.value))
                
            # Lecture des données
            for row in range(2, nb_rows+1):
                # On récupère la valeur dans la cellule de la ligne row et de colonne col
                for col in range(1, nb_columns+1):
                    cell = sheet.cell(row=row, column=col)
                    data[name_column[col-1]].append(cell.value)

            return data
        except:
            self.__error_msg = "Erreur : Problème rencontré. Impossibilité de charger le fichier excel avec openpyxl.\n Essayez avec un autre moteur"
            return None
        
        
    def __transform_data_pandas(self, data):
        """ Transforme un dataframe vers notre format de dictionnaire
        Dictionnaire pandas :
        {
            'index': [noms des lignes],
            'columns: [noms des colonnes],
            'data': [liste de données pour chaque ligne]
        }

        Args:
            data (dict): Dictionnaire du dataframe

        Returns:
            dict: dictionnaire du bon format
        """
        columns = data['columns']
        values_columns = data['data']
        data_transform = {}
        for c in range(len(columns)):
            data_transform[str(columns[c])] = []
            for l in range(len(values_columns)):
                data_transform[str(columns[c])].append(values_columns[l][c])
        return data_transform

    
    def get_error(self):
        """ Retourne le message d'erreur

        Returns:
            str: le message d'erreur
        """
        return self.__error_msg
