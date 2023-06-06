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
            "name": ["SR"],
            "unit": [],
            "data": [1, 2, 3, 4, 5]
        },
        'NAME': {
            "name": ["NAME"],
            "unit": [],
            "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
        },
        'GENDER': {
            "name": ["GENDER"],
            "unit": [],
            "data": ['Male', 'Female', 'Male', 'Female', 'Male']
        },
        'AGE': {
            "name": ["AGE"],
            "unit": [],
            "data": [18, 19, 20, 21, 22]
        },
        'DATE': {
            "name": ["DATE"],
            "unit": [],
            "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
        }
    }
    m.read_file(people, '2019', 'hello')
    assert correct_data == m.get_data_from_file(people)
    
    
def test_read_file_incorrect():
    """ Test to read file when the file is not supported
    """
    with pytest.raises(Exception, match="cannot read data from 'export_invalid.py'. Should be a CSV, TSV, TXT or XLSX file"):
        m.read_file(export_invalid, '2020', 'hello')


def test_read_file_path_null():
    """ Test the file when the path is null
    """
    with pytest.raises(Exception, match="cannot read file because the path is null"):
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
    
    
def test_export_invalid():
    """ Test an invalid export
    """
    with pytest.raises(Exception, match="cannot export data to 'invalid'. Should be a CSV, TSV or TXT file"):
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
    with pytest.raises(Exception, match="the file 'export_invalid.py' is not open yet"):
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
                    "name": ["SR"],
                    "unit": [],
                    "data": [1, 2, 3, 4, 5]
                },
                'NAME': {
                    "name": ["NAME"],
                    "unit": [],
                    "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
                },
                'GENDER': {
                    "name": ["GENDER"],
                    "unit": [],
                    "data": ['Male', 'Female', 'Male', 'Female', 'Male']
                },
                'AGE': {
                    "name": ["AGE"],
                    "unit": [],
                    "data": [18, 19, 20, 21, 22]
                },
                'DATE': {
                    "name": ["DATE"],
                    "unit": [],
                    "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
                }
            },
            "year": '2019',
            "category": 'hello'
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
            "name": ["SR"],
            "unit": [],
            "data": [1, 2, 3, 4, 5]
        },
        'NAME': {
            "name": ["NAME"],
            "unit": [],
            "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
        },
        'GENDER': {
            "name": ["GENDER"],
            "unit": [],
            "data": ['Male', 'Female', 'Male', 'Female', 'Male']
        },
        'AGE': {
            "name": ["AGE"],
            "unit": [],
            "data": [18, 19, 20, 21, 22]
        },
        'DATE': {
            "name": ["DATE"],
            "unit": [],
            "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
        }
    }
    assert correct_data == m.get_data_from_file(people)


def test_get_data_file_not_open():
    with pytest.raises(Exception, match="there is no file 'not_open.csv' open"):
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