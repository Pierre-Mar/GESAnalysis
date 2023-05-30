import operator


class SortedData:
    
    def __init__(self):
        self.__error_msg = None
        pass
    
    
    def sorted_by_column(self, data, column, reversed=False):
        """ Trie les données selon une colonne column.

        Args:
            data (dict): Dictionnaire de données (ReaderData)
            column (str): un nom de colonne
            reverse (bool, optional): Ordre décroissant si reverse est vrai. Sinon ordre croissant. Par défaut False.

        Returns:
            list | None: Liste d'index indiquant la position des données si elle était triée
        """
        check_column = self.__check_column(data, column)
        if check_column is None:
            self.__error_msg = "Erreur : il n'y a pas de colonne '{0}'".format(column)
            return None
        
        list_data = data[check_column]["data"]
        
        sorted_list_data = [i for i in sorted(enumerate(list_data), key=operator.itemgetter(1), reverse=reversed)]
        # Correspondance entre l'index de la donnée avant et après le tri
        sorted_index_list_data = [0 for i in range(len(sorted_list_data))]
        for i in range(len(sorted_list_data)):
            sorted_index_list_data[sorted_list_data[i][0]] = i
        return sorted_index_list_data
    
    
    def __check_column(self, data, column):
        """ Vérifie si column est bien le nom d'une colonne de data

        Args:
            data (dict): Dictionnaire de données (ReaderData)
            column (str): Nom de colonnes où chaque mot est séparé par un espace

        Returns:
            str | None: Retourne le nom de la clé si column est une colonne de data. Sinon None
        """
        name_col = list(data.keys())
        for c in name_col:
            if column == " ".join(data[c]["name"]):
                print(c)
                return c
        return None
    
    
    def get_error(self):
        """ Retourne le message d'erreur en cours

        Returns:
            str: Message d'erreur
        """
        return self.__error_msg
