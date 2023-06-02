import pytest
import platform
import os
from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData


export = ExportData()
reader = ReaderData()
tmp_file = "tmp" # For each function, add the extension

# Définition of paths of files depending on the OS
os_name = platform.system()
people = "tests/resources/people.csv"
hw_5 = "tests/resources/hw_5.tsv"
username = "tests/resources/username.txt"
excel = "tests/resources/file_example_XLSX_10.xlsx"
export_invalid = "tests/resources/export_invalid.py"
if os_name == 'Windows':
    people = r"tests\resources\people.csv"
    hw_5 = r"tests\resources\hw_5.tsv"
    username = r"tests\resources\username.txt"
    excel = r"tests\resources\file_example_XLSX_10.xlsx"
    export_invalid = r"tests\resources\export_invalid.py"


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
        "Langage": ["Français", "Anglais"],
        "Mot": ["Bonjour", "Hello"]
    }
    assert False == export.export_data(data, export_invalid)
    assert "Erreur : le fichier 'export_invalid.py' doit être un fichier CSV, TSV ou TXT pour l'exportation" == export.get_error()


def test_invalid_data():
    """ Check if a dictionary of data is None, then we catch the error
    """
    data = None
    assert False == export.export_data(data, tmp_file+".txt")
    assert "Erreur : les données ne peuvent pas être lues" == export.get_error()


def test_nb_elem_col_diff_data():
    """ Check that an incorrect data gives an error
    """
    data = {
        "Langage": {
            "name": ["Langage"],
            "unit": None,
            "data": ["Français", "Anglais"]   
        },
        "Mot": {
            "name": ["Mot"],
            "unit": None,
            "data": ["Bonjour"]
        }
    }
    assert False == export.export_data(data, tmp_file+".txt")
    assert "Erreur : Le nombre d'éléments de la ligne 2 est différent" == export.get_error()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------