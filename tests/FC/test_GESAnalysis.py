#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
import pytest
import os
import platform
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.ReaderData import ReaderData



# Définition of paths of files depending on the OS
os_name = platform.system()
path_file = "tests/resources/"
if os_name == "Windows":
    path_file = "tests\\resources\\"
people = path_file + "people.csv"
hw = path_file + "hw_5.tsv"
export_invalid = path_file + "export_invalid.py"
not_exist = path_file + "not_exist"


m = GESAnalysis()

# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_read_file():
    """ Test to read file when the path is correct
    """
    correct_data = {
        'SR': {
            'name': ['SR'],
            'unit': [],
            'data': [[1], [2], [3], [4], [5]],
            'type': int
        },
        'NAME': {
            'name': ['NAME'],
            'unit': [],
            'data': [['Dett'], ['Nern'], ['Kallsie'], ['Siuau'], ['Shennice']],
            'type': str
        },
        'GENDER': {
            'name': ['GENDER'],
            'unit': [],
            'data': [['Male'], ['Female'], ['Male'], ['Female'], ['Male']],
            'type': str
        },
        'AGE': {
            'name': ['AGE'],
            'unit': [],
            'data': [[18], [19], [20], [21], [22]],
            'type': int
        },
        'DATE': {
            'name': ['DATE'],
            'unit': [],
            'data': [['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['21/05/2016']],
            'type': str
        }
    }
    m.read_file(people, '2019', 'hello')
    assert correct_data == m.get_data_from_file(people)
    
    
def test_read_file_incorrect():
    """ Test to read file when the file is not supported
    """
    with pytest.raises(Exception, match="Exportation impossible de 'export_invalid.py'. Le fichier doit être de type CSV, TSV, TXT ou XLSX"):
        m.read_file(export_invalid, '2020', 'hello')


def test_read_file_path_null():
    """ Test the file when the path is null
    """
    with pytest.raises(Exception, match="Impossible de lire le fichier car le chemin est invalide"):
        m.read_file(None, '2019', 'hello')
        
        
def test_read_file_year_incorrect():
    """ Test the file when the path is null
    """
    with pytest.raises(Exception, match="'Wrong' n'est pas une année"):
        m.read_file(people, 'Wrong', 'hello')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : export(filein, fileout)
# ------------------------------------------------------------------------------------------------------------------------
def test_export_file():
    """ Test a correct export
    """
    m.export(people, "tmp.txt")
    r = ReaderData()
    d = r.read_file("tmp.txt")
    assert m.get_data_from_file(people) == d
    os.remove("tmp.txt")
    
    
def test_export_close():
    """ Test export a file who are not open
    """
    m.export(hw, "tmp.tsv")
    r = ReaderData()
    d = r.read_file(hw)
    assert d == r.read_file("tmp.tsv")
    os.remove("tmp.tsv")
    
    
def test_export_invalid():
    """ Test an invalid export
    """
    with pytest.raises(Exception, match="Exportation impossible de 'invalid'. Le fichier doit être de type CSV, TSV ou TXT"):
        m.export(people, "invalid")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : export_stat(data, header_column, header_row, fileout)
# ------------------------------------------------------------------------------------------------------------------------
def test_export_stat_valid():
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
    m.export_stat(data, header_columns, header_rows, "tmp.csv")
    m.read_file("tmp.csv", "2019", "Hello")
    assert data_dict == m.get_data_from_file("tmp.csv")
    m.close_file("tmp.csv")
    os.remove("tmp.csv")
    
    
def test_export_stat_invalid():
    data = [["10", "11", "12"],
            ["20", "21", "22"],
            ["30", "31", "32"]]
    header_columns = ["Zero", "Un"]
    header_rows = ["Dix", "Vingt", "Trente"]
    with pytest.raises(ValueError, match="Il y a 3 éléments alors qu'il y a 2 colonnes"):
        m.export_stat(data, header_columns, header_rows, "tmp.csv")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : close_file(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_close_file_correct():
    m.read_file(hw, '2020', 'hola')
    m.close_file(hw)
    # Should raise the exception because not in the dictionary
    with pytest.raises(Exception):
        m.get_data_from_file(hw)
        
        
def test_close_file_not_open():
    with pytest.raises(Exception, match="Le fichier 'export_invalid.py' n'est pas ouvert"):
        m.close_file(export_invalid)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : set_year(filename, year)
# ------------------------------------------------------------------------------------------------------------------------
def test_set_year_correct():
    m.read_file(people, '2019', 'hello')
    m.set_year(people, '2020')
    assert '2020' == m.get_year(people)
    m.close_file(people)
    

def test_set_year_incorrect_year():
    m.read_file(people, '2019', 'hello')
    with pytest.raises(Exception, match="'Wrong' n'est pas une année"):
        m.set_year(people, "Wrong")
    m.close_file(people)
    

def test_set_year_file_close():
    with pytest.raises(Exception, match="Le fichier 'closed_file.txt' n'est pas ouvert"):
        m.set_year("closed_file.txt", '2019')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : set_category(filename, category)
# ------------------------------------------------------------------------------------------------------------------------
def test_set_category_correct():
    m.read_file(people, '2019', 'Hello')
    m.set_category(people, 'Hola')
    assert 'Hola' == m.get_category(people)
    m.close_file(people)
    

def test_set_category_incorrect():
    with pytest.raises(Exception, match="Le fichier 'closed_file.txt' n'est pas ouvert"):   
        m.set_category("closed_file.txt", 'Wrong')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_data(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_data():
    m.read_file(people, '2019', 'hello')
    correct_data = {
        "people.csv": {
            "data": {
                'SR': {
                    'name': ['SR'],
                    'unit': [],
                    'data': [[1], [2], [3], [4], [5]],
                    'type': int
                },
                'NAME': {
                    'name': ['NAME'],
                    'unit': [],
                    'data': [['Dett'], ['Nern'], ['Kallsie'], ['Siuau'], ['Shennice']],
                    'type': str
                },
                'GENDER': {
                    'name': ['GENDER'],
                    'unit': [],
                    'data': [['Male'], ['Female'], ['Male'], ['Female'], ['Male']],
                    'type': str
                },
                'AGE': {
                    'name': ['AGE'],
                    'unit': [],
                    'data': [[18], [19], [20], [21], [22]],
                    'type': int
                },
                'DATE': {
                    'name': ['DATE'],
                    'unit': [],
                    'data': [['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['21/05/2016']],
                    'type': str
                }
            },
            "year": '2019',
            "category": 'hello',
            "path": "tests/resources/people.csv"
        }
    }
    assert correct_data == m.get_data()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_file_open(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_file_open():
    m.read_file(people, '2019', 'people')
    m.read_file(hw, '2020', 'hw')
    correct_list = ["people.csv", "hw_5.tsv"]
    assert correct_list == m.get_file_open()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_data_from_file(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_data_from_file_correct():
    correct_data = {
        'SR': {
            'name': ['SR'],
            'unit': [],
            'data': [[1], [2], [3], [4], [5]],
            'type': int
        },
        'NAME': {
            'name': ['NAME'],
            'unit': [],
            'data': [['Dett'], ['Nern'], ['Kallsie'], ['Siuau'], ['Shennice']],
            'type': str
        },
        'GENDER': {
            'name': ['GENDER'],
            'unit': [],
            'data': [['Male'], ['Female'], ['Male'], ['Female'], ['Male']],
            'type': str
        },
        'AGE': {
            'name': ['AGE'],
            'unit': [],
            'data': [[18], [19], [20], [21], [22]],
            'type': int
        },
        'DATE': {
            'name': ['DATE'],
            'unit': [],
            'data': [['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['21/05/2016']],
            'type': str
        }
    }
    assert correct_data == m.get_data_from_file(people)


def test_get_data_file_not_open():
    with pytest.raises(Exception, match="Le fichier 'not_open.csv' n'est pas ouvert"):
        m.get_data_from_file("not_open.csv")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_filename(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_filename():
    assert "people.csv" == m.get_filename(people)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_path(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_path():
    m.read_file(people, "2019", "Missions")
    assert people == m.get_path(people)
    m.close_file(people)
    
    
def test_get_path_incorrect():
    with pytest.raises(Exception, match="Le fichier 'people.csv' n'est pas ouvert"):
        m.get_path(people)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_year(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_year():
    m.read_file(people, "2019", "Missions")
    assert "2019" == m.get_year(people)
    m.close_file(people)
    
    
def test_get_year_incorrect():
    with pytest.raises(Exception, match="Le fichier 'people.csv' n'est pas ouvert"):
        m.get_year(people)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests : get_category(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_get_category():
    m.read_file(people, "2019", "Missions")
    assert "Missions" == m.get_category(people)
    m.close_file(people)
    
    
def test_get_category_incorrect():
    with pytest.raises(Exception, match="Le fichier 'people.csv' n'est pas ouvert"):
        m.get_category(people)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
