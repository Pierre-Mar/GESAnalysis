import operator


class SortedData:
    """ Class to sort data
    """
    
    def __init__(self):
        """ Initialisation of class
        """
        self.__error_msg = None
        pass
    
    
    def sorted_by_column(self, data_dict, column, reversed=False):
        """ Sort data according to the column 'column'

        Args:
            data_dict (dict): Dictionary of data (format from ReaderData)
            column (str): Column name
            reverse (bool, optional): Sort by descending order if reverse is True. Else by acsending order. Defaults to False

        Returns:
            list | None: List of index indicating the position of the data. None if there are no column 'column' in data
        """
        check_column = self.__check_column(data_dict, column)
        if check_column is None:
            self.__error_msg = "Erreur : il n'y a pas de colonne '{0}'".format(column)
            return None
        
        list_data = data_dict[check_column]["data"]

        sorted_list_data = [i for i in sorted(enumerate(list_data), key=operator.itemgetter(1), reverse=reversed)]
        
        # Link between the index of data before and after the sort
        sorted_index_list_data = [0 for i in range(len(sorted_list_data))]
        for i in range(len(sorted_list_data)):
            sorted_index_list_data[sorted_list_data[i][0]] = i
        return sorted_index_list_data
    
    
    def __check_column(self, data_dict, column):
        """ Check if 'column' is a column of the dictionary 'data'

        Args:
            data_dict (dict): Dictionary of data (format from ReaderData)
            column (str): Column name where each word is separated by a space

        Returns:
            str | None: Returns the key if 'column' is a column of 'data'. Else None
        """
        name_col = list(data_dict.keys())
        for c in name_col:
            if column == " ".join(data_dict[c]["name"]):
                return c
        return None
    
    
    def get_error(self):
        """ Returns the last error message

        Returns:
            str: Error message
        """
        return self.__error_msg
