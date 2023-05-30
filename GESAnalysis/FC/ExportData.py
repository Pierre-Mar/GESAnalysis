import os


class ExportData:
    """ Classe permettant l'export des données vers un fichier csv, tsv et txt
    """
    
    __accepted_extension = [".csv", ".tsv", ".txt"]
    
    def __init__(self):
        self.__error_msg = None
        pass
    
    @staticmethod
    def export_data(self, data, fileout):
        """ Exporte les données de data dans le fichier fileout

        Args:
            data (dict): Dictionnaire contenant les données
            fileout (str): Chemin vers le fichier

        Returns:
            bool: Retournes Vrai si les données ont été écrits dans le fichiers, sinon Faux
        """
        if data is None:
            self.__error_msg = "Erreur : les données ne peuvent pas être lues"
            return False
        
        
        # Vérification du nom du fichier
        if not self.__verif_fileout(fileout):
            return False
        
        match self.__file_ext:
            case ".csv":
                return self.__write_in_file(data, fileout, ',')
            case ".tsv":
                return self.__write_in_file(data, fileout, '\t')
            case _:
                return self.__write_in_file(data, fileout, ',')
    
    
    def __verif_fileout(self, fileout):
        """ Vérifie que le fichier de sortie est un fichier CSV, TSV ou TXT

        Args:
            fileout (str): chemin vers le fichier

        Returns:
            bool: retourne Vrai si le fichier a la bonn extension sinon Faux
        """
        # Récupère l'extension du fichier
        root_filename, self.__file_ext = os.path.splitext(fileout)
        
        # Récupère le nom du fichier, en enlevant son chemin
        path_to_file = root_filename.split('/')
        file = path_to_file[len(path_to_file) - 1]
        
        if not self.__file_ext in self.__accepted_extension:
            self.__error_msg = "Erreur : le fichier '{0}' doit être un fichier CSV, TSV ou TXT pour l'exportation".format(
                file + self.__file_ext)
            return False
        
        return True
    
    
    def __write_in_file(self, data, fileout, sep):
        """ Ecriture des données data dans le fichier fileout avec sep comme separateur

        Args:
            data (dict): Dictionnaire contenant les données (fait avec ReaderData)
            fileout (str): chemin vers le fichier de sortie
            sep (str): separateur entre les données

        Returns:
            bool: Retourne Vrai si les données sont écrites dans fileout, sinon Faux
        """
        try:
            with open(fileout, "w") as file_out:
                # Ecriture des colonnes
                columns = list(data.keys())
                nb_columns = len(columns)
                name_columns = sep.join(columns) + '\n'
                
                file_out.write(name_columns)
                
                # Ecriture des lignes
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
        except Exception as e:
            print(e)
            self.__error_msg = "Erreur : problème rencontré pendant l'exportation"
            os.remove(fileout)
            return False
            
        return True
    
    
    def __verif_number_lines(self, elems_col):
        """ Vérifie que le nombre d'éléments de chaque colonne est égal

        Args:
            elems_col (list): une liste de liste avec les données de chaque colonnes dans une liste

        Returns:
            bool: retourne Vrai si ce nombre est égal, sinon Faux
        """
        nb_elements = len(elems_col[0])
        for i in range(1, len(elems_col)):
            if len(elems_col[i]) != nb_elements:
                self.__error_msg = "Erreur : Le nombre d'éléments de la ligne {0} est différent".format(i+1)
                return False
            
        return True


    def __get_data(self, data_dict):
        """ Récupères les données de chaque colonne et les mets dans une liste

        Args:
            data_dict (dict): Dictionnaire de données (ReaderData)

        Returns:
            list: liste des données
        """
        val = list(data_dict.values())
        list_data = []
        for l in val:
            list_data.append(l["data"])
        return list_data
    
    
    def get_error(self):
        """ Retournes le dernier message d'erreur

        Returns:
            str: message d'erreur
        """
        return self.__error_msg
