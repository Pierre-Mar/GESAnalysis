#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
#######################################################################################################
#  Common methods by different class of differents categories                                         #
#######################################################################################################


from typing import Dict, List, Union, Optional

from GESAnalysis.FC.GESAnalysis import GESAnalysis


def check_value(
    model: GESAnalysis,
    column: str,
) -> str:
    """ Check the unit of a column for each file in the model if it's the same

    Args:
        model (GESAnalysis): Model
        column (str): Column from model

    Raises:
        ValueError: A file has a different unit or the values are not integers or float

    Returns:
        str: Unit
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

######### Name of column #########
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


def get_name_from_columns(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    list_column: List[str]
) -> Optional[List[Union[str, int, float, bool]]]:
    """ Returns the name associated of a column in list_columns in the reader

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionary
        list_column (List[str]): List of columns

    Returns:
        Optional[List[Union[str, int, float, bool]]]: Name associated to a column from list_column
    """
    for col in list_column:
        data_col = get_name_column(reader, col)
        if data_col is not None:
            return data_col
    return None


######### Data of column #########
def get_data(
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


def get_data_from_columns(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    list_column: List[str]
) -> Optional[List[Union[str, int, float, bool]]]:
    """ Returns the data associated of a column in list_columns in the reader

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionary
        list_column (List[str]): List of columns

    Returns:
        Optional[List[Union[str, int, float, bool]]]: Data associated to a column from list_column
    """
    for col in list_column:
        data_col = get_data(reader, col)
        if data_col is not None:
            return data_col
    return None
    

######### Type of column #########
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


def get_type_from_columns(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    list_columns: List[str]
) -> Optional[Union[str, bool, int, float]]:
    """ Returns the type associated of a column in list_columns in the reader

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionary
        list_column (List[str]): List of columns

    Returns:
        Optional[List[Union[str, int, float, bool]]]: Type associated to a column from list_column
    """
    for col in list_columns:
        type = get_type(reader, col)
        if type is not None:
            return type
    return None


######### Unit of column #########
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


def get_unit_from_columns(
    reader: Dict[str, Dict[str, List[Union[str, int, float, bool]]]],
    list_columns: List[str]
) -> Optional[List[str]]:
    """ Returns the unit of a column from a list of columns in the dictionary 'reader'

    Args:
        reader (Dict[str, Dict[str, List[Union[str, int, float, bool]]]]): Dictionary
        list_columns (List[str]): List of columns

    Returns:
        Optional[List[str]]: Unit
    """
    for col in list_columns:
        unit = get_unit(reader, col)
        if unit is not None:
            return unit
    return None
