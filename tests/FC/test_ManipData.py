import pytest
import platform
from GESAnalysis.FC.ManipData import ManipData
import os


# Définition of paths of files depending on the OS
os_name = platform.system()
people = "tests/resources/people.csv"
export_invalid = "tests/resources/export_invalid.py"
not_exist = "tests/resources/not_exist"
if os_name == 'Windows':
    people = r"tests\resources\people.csv"
    export_invalid = r"tests\resources\export_invalid.py"



# ------------------------------------------------------------------------------------------------------------------------
# Tests : ManipData(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_initialisation():
    """ Test the initialisation of the class and the reading when we give the file to the contructor
    """
    m = ManipData(people)
    correct_data = {
        'SR': {
            "name": ["SR"],
            "unit": None,
            "data": [1, 2, 3, 4, 5]
        },
        'NAME': {
            "name": ["NAME"],
            "unit": None,
            "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
        },
        'GENDER': {
            "name": ["GENDER"],
            "unit": None,
            "data": ['Male', 'Female', 'Male', 'Female', 'Male']
        },
        'AGE': {
            "name": ["AGE"],
            "unit": None,
            "data": [18, 19, 20, 21, 22]
        },
        'DATE': {
            "name": ["DATE"],
            "unit": None,
            "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
        }
    }
    assert people == m.get_filename()
    assert correct_data == m.get_data()
    assert None == m.get_error()
    
    
def test_initialisation_incorrect():
    """ Test when the initialisation is incorrect
    """
    m = ManipData(export_invalid)
    assert export_invalid == m.get_filename()
    assert None == m.get_data()
    assert "Erreur : Le fichier 'export_invalid.py' n'est pas pris en charge par l'application" == m.get_error()
    


# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename, sep, engine)
# ------------------------------------------------------------------------------------------------------------------------
def test_read_file():
    """ Test the reading of the file 'filename'
    """
    m = ManipData()
    correct_data = {
        'SR': {
            "name": ["SR"],
            "unit": None,
            "data": [1, 2, 3, 4, 5]
        },
        'NAME': {
            "name": ["NAME"],
            "unit": None,
            "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
        },
        'GENDER': {
            "name": ["GENDER"],
            "unit": None,
            "data": ['Male', 'Female', 'Male', 'Female', 'Male']
        },
        'AGE': {
            "name": ["AGE"],
            "unit": None,
            "data": [18, 19, 20, 21, 22]
        },
        'DATE': {
            "name": ["DATE"],
            "unit": None,
            "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
        }
    }
    m.read_file(people)
    assert people == m.get_filename()
    assert correct_data == m.get_data()
    assert None == m.get_error()
    

def test_read_file_incorrect():
    """ Test the reading of the file when there is an error
    """
    m = ManipData()
    m.read_file(export_invalid)
    assert "Erreur : Le fichier 'export_invalid.py' n'est pas pris en charge par l'application" == m.get_error()
    

# ------------------------------------------------------------------------------------------------------------------------
# Tests : export(fileout)
# ------------------------------------------------------------------------------------------------------------------------
def test_export():
    """ Test the exporation of data to a file
    """
    m = ManipData(people)
    m.export("tmp.csv")
    assert None == m.get_error()
    os.remove("tmp.csv")
    

def test_export_incorrect():
    """ Test the exportation of a file when there is an error
    """
    m = ManipData()
    m.export("tmp.txt")
    assert "Erreur : les données ne peuvent pas être lues" == m.get_error()