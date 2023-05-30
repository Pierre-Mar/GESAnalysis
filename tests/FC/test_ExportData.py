import pytest
import platform
import os
from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData


export = ExportData()
reader = ReaderData()
tmp_file = "tmp" # Dans chaque fonction, ajoutez l'extension

# Définition des chemins de fichiers selon l'OS
os_name = platform.system()
people = "tests/resources/people.csv"
hw_5 = "tests/resources/hw_5.tsv"
username = "tests/resources/username.txt"
excel = "tests/resources/file_example_XLSX_10.xlsx"
export_invalid = "tests/resources/export_invalid.py"
if os_name == 'Windows':
    people = r"tests\resources\people.csv"
    hw_5 = r"tests\resources\w_5.tsv"
    username = r"tests\resources\username.txt"
    excel = r"tests\resources\file_example_XLSX_10.xlsx"
    export_invalid = r"tests\resources\export_invalid.py"


# ------------------------------------------------------------------------------------------------------------------------
# Tests : export_data(data, fileout)
# ------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que l'exportation est correcte
# ------------------------------------------------------------------------------------------------------------------------
def test_export_csv_file():
    """ Vérifie que l'exportation vers un fichier csv fonctionne
    """
    d = reader.read_file(people)
    assert True == export.export_data(d, tmp_file+".csv")
    assert d == reader.read_file(tmp_file+".csv")
    os.remove(tmp_file+".csv")


def test_export_tsv_file():
    """ Pareil mais vers un fichier tsv
    """
    d = reader.read_file(hw_5)
    assert True == export.export_data(d, tmp_file+".tsv")
    assert d == reader.read_file(tmp_file+".tsv")
    os.remove(tmp_file+".tsv")


def test_export_txt_file():
    """ Pareil mais vers un fichier txt
    """
    d = reader.read_file(username)
    assert True == export.export_data(d, tmp_file+".txt")
    assert d == reader.read_file(tmp_file+".txt")
    os.remove(tmp_file+".txt")


def test_export_xlsx_to_csv():
    """ Vérifie que l'exportation d'un fichier excel vers un fichier csv fonctionne correctement
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".csv")
    assert d == reader.read_file(tmp_file+".csv")
    os.remove(tmp_file+".csv")


def test_export_xlsx_to_tsv():
    """ Pareil mais vers un fichier tsv
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".tsv")
    assert d == reader.read_file(tmp_file+".tsv")
    os.remove(tmp_file+".tsv")
    

def test_export_xlsx_to_txt():
    """ Pareil mais vers un fichier txt
    """
    d = reader.read_file(excel)
    assert True == export.export_data(d, tmp_file+".txt")
    assert d == reader.read_file(tmp_file+".txt")
    os.remove(tmp_file+".txt")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test pour vérifier qu'on obtient les bonnes erreurs en cas de problèmes
# ------------------------------------------------------------------------------------------------------------------------
def test_invalid_file_export():
    """ Vérifie que l'exportation vers un fichier invalide donne une erreur.
    """
    data = {
        "Langage": ["Français", "Anglais"],
        "Mot": ["Bonjour", "Hello"]
    }
    assert False == export.export_data(data, export_invalid)
    assert "Erreur : le fichier 'export_invalid.py' doit être un fichier CSV, TSV ou TXT pour l'exportation" == export.get_error()


def test_invalid_data():
    """ Vérifie que si nous n'avons pas de données, alors on a une erreur
    """
    data = None
    assert False == export.export_data(data, tmp_file+".txt")
    assert "Erreur : les données ne peuvent pas être lues" == export.get_error()


def test_nb_elem_col_diff_data():
    """ Vérifies que les données incorrectes ici, nous renvoie une erreur
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