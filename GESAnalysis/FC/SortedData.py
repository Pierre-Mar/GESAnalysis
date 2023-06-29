import operator
from typing import Optional, Union, Dict, List


class SortedData:
    """ Class to sort data
    """
    
    def __init__(self) -> None:
        """ Initialisation of class
        """
        pass
    
    
    def sorted_by_column(
        self,
        data_dict: Optional[Dict[str, Dict[str, List[Union[str, int, float, bool]]]]],
        column: str,
        reversed: bool = False
    ) -> List[int]:
        """ Sort data according to the column 'column'

        Args:
            data_dict (dict): Dictionary of data (format from ReaderData)
            column (str): Column name
            reverse (bool, optional): Sort by descending order if reverse is True. Else by acsending order. Defaults to False

        Returns:
            list: List of index indicating the position of the data
        """
        if data_dict is None:
            raise TypeError("Accès impossible au données car le dictionnaire est invalide")
        
        # Check the column name
        check_column = self.__check_column(data_dict, column)
        if check_column is None:
            raise KeyError(f"La colonne '{column}' n'existe pas")

        list_data = data_dict[check_column]["data"].copy()
        for i in range(len(list_data)):
            list_data[i] = sum(list_data[i])
            
        sorted_list_data = [i for i in sorted(enumerate(list_data), key=operator.itemgetter(1), reverse=reversed)]

        # Link between the index of data before and after the sort
        sorted_index_list_data = [0 for i in range(len(sorted_list_data))]
        for i in range(len(sorted_list_data)):
            sorted_index_list_data[sorted_list_data[i][0]] = i

        return sorted_index_list_data
    
    
    def __check_column(
        self,
        data_dict: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
        column: str
    ) -> Optional[str]:
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
