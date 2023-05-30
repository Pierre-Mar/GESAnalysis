import pytest
from GESAnalysis.FC.ManipData import ManipData
import os


# ------------------------------------------------------------------------------------------------------------------------
# Tests : ManipData(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_initialisation():
    """ Test l'initialisation de la classe et la lecture du fichier
    """
    m = ManipData("tests/resources/people.csv")
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
    assert "tests/resources/people.csv" == m.get_filename()
    assert correct_data == m.get_data()
    assert None == m.get_error()
    
    
def test_initialisation_incorrect():
    """ Test quand l'initialisation est incorrect
    """
    m = ManipData("tests/resources/export_invalid.py")
    assert "tests/resources/export_invalid.py" == m.get_filename()
    assert None == m.get_data()
    assert "Erreur : Le fichier 'export_invalid.py' n'est pas pris en charge par l'application" == m.get_error()
    


# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename, sep, engine)
# ------------------------------------------------------------------------------------------------------------------------

def test_read_file():
    """ Test la lecture du fichier 'filename'
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
    m.read_file("tests/resources/people.csv")
    assert "tests/resources/people.csv" == m.get_filename()
    assert correct_data == m.get_data()
    assert None == m.get_error()
    

def test_read_file_incorrect():
    """ Test la lecture du fichier quand il y a une erreur
    """
    m = ManipData()
    m.read_file("tests/resources/export_invalid.py")
    assert "Erreur : Le fichier 'export_invalid.py' n'est pas pris en charge par l'application" == m.get_error()
    

# ------------------------------------------------------------------------------------------------------------------------
# Tests : export(fileout)
# ------------------------------------------------------------------------------------------------------------------------
def test_export():
    """ Test l'exportation des données vers un fichier
    """
    m = ManipData("tests/resources/people.csv")
    m.export("tmp.csv")
    assert None == m.get_error()
    os.remove("tmp.csv")
    

def test_export_incorrect():
    """ Test l'exportation de fichiers quand il y a un problème
    """
    m = ManipData()
    m.export("tmp.txt")
    assert "Erreur : les données ne peuvent pas être lues" == m.get_error()