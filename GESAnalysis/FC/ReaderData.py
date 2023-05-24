import os
import csv

class ReaderData:
    
    accepted_extension = [".csv", ".txt", ".tsv", ".xlsx"]
    
    def __init__(self):
        self.error_msg = None
    
    
    def verify_file(self, filename):
        """ Vérifie que le fichier existe et qu'il peut être lu

        Args:
            filename (str): un nom de fichier (chemin)

        Returns:
            bool: retourne Vrai si le fichier existe et qu'il peut être lu, sinon Faux
        """
        # Recupère l'extension du fichier
        root_filename, self.ext = os.path.splitext(filename)
        
        return os.path.isfile(filename) and self.ext in self.accepted_extension
    
    def detect_delimiter(self, filename):
        """ Détectes le délimiteur qui se trouve dans filename

        Args:
            filename (str): un nom de fichier

        Returns:
            str: le délimiteur dans le fichier filename
        """
        sniffer = csv.Sniffer()
        
        # Récupère la 1ère ligne (nom des colonnes)
        head_line = None
        with open(filename, "r") as f:
            head_line = f.readline()
        
        dialect = sniffer.sniff(head_line)
        return dialect.delimiter
    

    def read_csv_tsv_txt(self, filename, sep=','):
        """ Lecture des données depuis un fichier csv, txt ou tsv et un délimiteur

        Args:
            filename (str): un nom de fichier
            sep (str, optional): un délimiteur dans le fichier filename. Defaults to ','.

        Returns:
            dict: Dictionnaire contenant les données (clés = nom des colonnes)
        """
        data = {}
        with open(filename, "r") as file:
            # Lecture de la 1ère ligne (contient le nom des colonnes)
            column = file.readline()
            # Enlève les caractères inutiles
            column = column.strip("\ufeff") 
            column = column.strip("\n")
            name_column = column.split(sep)
            nb_column = len(name_column)
            # Ajout dans data
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
                    self.error_msg = "Erreur : le nombre d'éléments à la ligne {0} est différent du nombre de colonnes {1}".format(
                        lines_iter, nb_column
                    )
                    return None
                
                columns_iter = 0
                for elem in list_lines:
                    new_elem = self.convert_element(elem)
                    
                    # Vérifie que l'élément est du bon type
                    # Si c'est le 1er élément, on le saute
                    if lines_iter != 1 and type(new_elem) != type(data[name_column[columns_iter]][0]):
                        self.error_msg = "Erreur : L'élément de la colonne {0} et de la ligne {1} est différent des éléments de cette colonne".format(
                            name_column[columns_iter], lines_iter
                        )
                        return None
                    
                    # Ajout dans data
                    data[name_column[columns_iter]].append(new_elem)
                    
                    columns_iter += 1
                    
                # Ligne suivante
                lines = file.readline()
                lines = lines.strip()
                lines_iter += 1
                
        return data
    
    
    def convert_element(self, elem):
        """ Convertit l'élément elem dans son bon type

        Args:
            elem (str): élément à convertir

        Returns:
            bool | int | float | str : l'élément dans son bon type
        """
        contructors = [int, float, str]
        if elem.lower() == "true":
            return True
        elif elem.lower() == "false":
            return False
    
        for c in contructors:
            try:
                return c(elem)
            except ValueError:
                pass
