#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
import pytest
import platform
import os
from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData


export = ExportData()
reader = ReaderData()
tmp_file = "tmp" # For each function, add the extension

# Definition of paths of files depending on the OS
os_name = platform.system()
path = "tests/resources/"
if os_name == "Windows":
    path = "tests\\resources\\"
people = path + "people.csv"
hw_5 = path + "hw_5.tsv"
username = path + "username.txt"
excel = path + "file_example_XLSX_10.xlsx"
export_invalid = path + "export_invalid.py"


# ------------------------------------------------------------------------------------------------------------------------
# Tests : export_data(data, fileout)
# ------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------
# Tests to check if the exportation is valid
# ------------------------------------------------------------------------------------------------------------------------
def test_export_csv_file():
    """ Check that the exportation to a CSV file works
    """
    d = reader.read_file(people)
    assert True == export.export_data(d, tmp_file+".csv")
    assert d == reader.read_file(tmp_file+".csv")
    os.remove(tmp_file+".csv")


def test_export_tsv_file():
    """ Same with a TSV file
    """
    d = reader.read_file(hw_5)
    assert True == export.export_data(d, tmp_file+".tsv")
    assert d == reader.read_file(tmp_file+".tsv")
    os.remove(tmp_file+".tsv")


def test_export_txt_file():
    """ Same with a TXT file
    """
    d = reader.read_file(username)
    assert True == export.export_data(d, tmp_file+".txt")
    assert d == reader.read_file(tmp_file+".txt")
    os.remove(tmp_file+".txt")


def test_export_xlsx_to_csv():
    """ Check the exportation of a XLSX file to a CSV file works
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".csv")
    assert d == reader.read_file(tmp_file+".csv")
    os.remove(tmp_file+".csv")


def test_export_xlsx_to_tsv():
    """ Same with a TSV file
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".tsv")
    assert d == reader.read_file(tmp_file+".tsv")
    os.remove(tmp_file+".tsv")
    

def test_export_xlsx_to_txt():
    """ Same with a TXT file
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".txt")
    assert d == reader.read_file(tmp_file+".txt")
    os.remove(tmp_file+".txt")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests to check if we get the corresponding error when we have a problem
# ------------------------------------------------------------------------------------------------------------------------
def test_invalid_file_export():
    """ Check the exportation to an invalid file gives an error
    """
    data = {
        "Langage": {
            "name": ["Langage"],
            "unit": [],
            "data": [["Français"], ["Anglais"]],
            "type": str
        },
        "Mot": {
            "name": ["Mot"],
            "unit": [],
            "data": [["Bonjour"], ["Hello"]],
            "type": str
        }
    }
    with pytest.raises(Exception, match="Exportation impossible de 'export_invalid.py'. Le fichier doit être de type CSV, TSV ou TX"):
        export.export_data(data, export_invalid)


def test_invalid_data():
    """ Check if a dictionary of data is None, then we catch the error
    """
    with pytest.raises(TypeError, match="Accès impossible au données car le dictionnaire est invalide"):
        export.export_data(None, tmp_file+".txt")


def test_nb_elem_col_diff_data():
    """ Check that an incorrect data gives an error
    """
    data = {
        "Langage": {
            "name": ["Langage"],
            "unit": [],
            "data": [["Français"], ["Anglais"]],
            "type": str
        },
        "Mot": {
            "name": ["Mot"],
            "unit": [],
            "data": [["Bonjour"]],
            "type": str
        }
    }
    with pytest.raises(ValueError, match="La ligne 2 a 1 éléments au lieu de 2 éléments"):
        export.export_data(data, tmp_file+".txt")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : export_stat(self, data: List[List[str]], header_column: List[str], header_row: List[str], fileout: str)
# ------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------
# Tests to check if the exportation of stats is valid
# ------------------------------------------------------------------------------------------------------------------------
def test_export_stat_valid_csv():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    header_columns = ["Zero", "Un", "Deux"]
    header_rows = ["Dix", "Vingt", "Trente"]
    data_dict = {
        'header_row': {
            'name': ['header_row'],
            'unit': [],
            'data': [['Dix'], ['Vingt'], ['Trente']],
            'type': str
        },
        'Zero': {
            'name': ['Zero'],
            'unit': [],
            'data': [[10], [20], [30]],
            'type': int
        },
        'Un': {
            'name': ['Un'],
            'unit': [],
            'data': [[11], [21], [31]],
            'type': int
        },
        'Deux': {
            'name': ['Deux'],
            'unit': [],
            'data': [[12], [22], [32]],
            'type': int
        }
    }
    export.export_stat(data, header_columns, header_rows, tmp_file+".csv")
    assert data_dict == reader.read_file(tmp_file + ".csv")
    os.remove(tmp_file + ".csv")


def test_export_stat_valid_tsv():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    
    header_columns = ["Zero", "Un", "Deux"]
    header_rows = ["Dix", "Vingt", "Trente"]
    data_dict = {
        'header_row': {
            'name': ['header_row'],
            'unit': [],
            'data': [['Dix'], ['Vingt'], ['Trente']],
            'type': str
        },
        'Zero': {
            'name': ['Zero'],
            'unit': [],
            'data': [[10], [20], [30]],
            'type': int
        },
        'Un': {
            'name': ['Un'],
            'unit': [],
            'data': [[11], [21], [31]],
            'type': int
        },
        'Deux': {
            'name': ['Deux'],
            'unit': [],
            'data': [[12], [22], [32]],
            'type': int
        }
    }
    export.export_stat(data, header_columns, header_rows, tmp_file+".tsv")
    assert data_dict == reader.read_file(tmp_file + ".tsv")
    os.remove(tmp_file + ".tsv")
    
    
def test_export_stat_valid_txt():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    header_columns = ["Zero", "Un", "Deux"]
    header_rows = ["Dix", "Vingt", "Trente"]
    data_dict = {
        'header_row': {
            'name': ['header_row'],
            'unit': [],
            'data': [['Dix'], ['Vingt'], ['Trente']],
            'type': str
        },
        'Zero': {
            'name': ['Zero'],
            'unit': [],
            'data': [[10], [20], [30]],
            'type': int
        },
        'Un': {
            'name': ['Un'],
            'unit': [],
            'data': [[11], [21], [31]],
            'type': int
        },
        'Deux': {
            'name': ['Deux'],
            'unit': [],
            'data': [[12], [22], [32]],
            'type': int
        }
    }
    export.export_stat(data, header_columns, header_rows, tmp_file+".txt")
    assert data_dict == reader.read_file(tmp_file + ".txt")
    os.remove(tmp_file + ".txt")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

    
# ------------------------------------------------------------------------------------------------------------------------
# Tests to check if we get the correct error
# ------------------------------------------------------------------------------------------------------------------------
def test_invalid_number_columns_elem():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    header_columns = ["Zero", "Un"]
    header_rows = ["Dix", "Vingt", "Trente"]
    with pytest.raises(ValueError, match="Il y a 3 éléments alors qu'il y a 2 colonnes"):
        export.export_stat(data, header_columns, header_rows, tmp_file + ".csv")


def test_inalid_number_row_elem():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    header_columns = ["Zero", "Un", "Deux"]
    header_rows = ["Dix", "Vingt"]
    with pytest.raises(ValueError, match="Il y a 3 lignes d'éléments alors qu'il y a 2 en-têtes de lignes"):
        export.export_stat(data, header_columns, header_rows, tmp_file + ".tsv")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
