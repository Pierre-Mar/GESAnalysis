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
    print(d)
    
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
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------