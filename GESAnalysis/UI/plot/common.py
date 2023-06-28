from typing import Dict, List, Union, Optional


def check_value(
    model,
    column,
) -> str:
    """ Check the unit of distance for each year is the same

    Raises:
        ValueError: A year has a different unit of distance or the values are not integers or float
    """
    unit = ""
    for values_ges in model.get_data().values():
        if values_ges["category"] != "Missions":
            continue
        reader = values_ges["data"]
        year = values_ges["year"]          
        unit_reader = get_unit(reader, column)
        type_reader = get_type(reader, column)
        
        if unit == "":
            unit = "/".join(unit_reader)
            
        unit_reader = "/".join(unit_reader)
            
        if unit_reader != unit:
            raise ValueError(f"unit of distance for year {year} is '{unit_reader} instead of '{unit}'")
        if type_reader not in [int, float]:
            raise ValueError(f"type of distance for year {year} is '{type_reader} instead of int or float")
    
    return unit



#######################################################################################################
#  Getters                                                                                            #
#######################################################################################################
def get_name_column(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    column: str
) -> Optional[str]:
    """ Get the full name (name+unit) of a column

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionary of data
        column (str): a name of column

    Returns:
        Optional[str]: The full name of the column. Else None
    """
    name_col = list(reader.keys())
    for c in name_col:
        if column == " ".join(reader[c]["name"]):
            return c
    return None


def get_column(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    column: str
) -> Optional[List[Union[str, int, float, bool]]]:
    """ Returns the data associated to the column 'column' in the dictionary 'reader'
    
    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]) : the dictionary
        column (str): the column

    Returns:
        List[Union[str, int, float, bool]] | None: The data associated to the column if the column exist, else None
    """
    name_col = list(reader.keys())
    for c in name_col:
        if column == " ".join(reader[c]["name"]):
            return reader[c]["data"]
    return None


def get_type(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    column: str
) -> Optional[Union[str, bool, int, float]]:
    """ Returns the type associated to the column 'column' in the dictionary 'reader'
    
    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]) : the dictionary
        column (str): the column

    Returns:
        Union[str, int, float, bool] | None: The type associated to the column if the column exist, else None
    """
    name_col = list(reader.keys())
    for c in name_col:
        if column == " ".join(reader[c]["name"]):
            return reader[c]["type"]
    return None


def get_unit(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    column: str
) -> Optional[List[str]]:
    """ Return the unit associated to the column 'column' in the dictionary 'reader'

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionnaire de données
        column (str): Nom de colonne
        
    Returns:
        List[str] | None: List of strings if the column was found, else None
    """
    name_col = list(reader.keys())
    for c in name_col:
        if column == " ".join(reader[c]["name"]):
            return reader[c]["unit"]
    return None