import pytest
import platform
from GESAnalysis.FC.ReaderData import ReaderData


reader = ReaderData()


# Définition des chemins de fichiers selon l'OS
os_name = platform.system()
people = "tests/resources/people.csv"
hw_5 = "tests/resources/hw_5.tsv"
username = "tests/resources/username.txt"
excel = "tests/resources/file_example_XLSX_10.xlsx"
export_invalid = "tests/resources/export_invalid.py"
not_exist = "tests/resources/not_exist"
cant_read = "tests/resources/cant_read.py"
nb_col_diff = "tests/resources/nb_col_diff.txt"
type_diff = "tests/resources/type_diff.txt"
if os_name == 'Windows':
    people = r"tests\resources\people.csv"
    hw_5 = r"tests\resources\hw_5.tsv"
    username = r"tests\resources\username.txt"
    excel = r"tests\resources\file_example_XLSX_10.xlsx"
    export_invalid = r"tests\resources\export_invalid.py"
    not_exist = r"tests\resources\not_exist"
    cant_read = r"tests\resources\cant_read.py"
    nb_col_diff = r"tests\resources\nb_col_diff.txt"
    type_diff = r"tests\resources\type_diff.txt"


# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename, sep)
# ------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que la lecture est correcte
# ------------------------------------------------------------------------------------------------------------------------
def test_valid_csv_file():
    """ Vérifie que la lecture d'un fichier csv se fasse correctement
    """
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
    assert correct_data == reader.read_file(people, sep=",")


def test_valid_tsv_file():
    """ Pareil mais avec un fichier tsv
    """
    correct_data = {
        "Index": {
            "name": ["Index"],
            "unit": None,
            "data": [1, 2, 3, 4, 5]
        },
        "height.cm": {
            "name": ["height"],
            "unit": ["cm"],
            "data": [165.1, 180.49, 175.26, 172.72, 170.18]
        },
        "weight.kg": {
            "name": ["weight"],
            "unit": ["kg"],
            "data": [50.80, 61.69, 69.4, 64.41, 65.32]
        }
    }
    assert correct_data == reader.read_file(hw_5)


def test_valid_txt_file():
    """ Pareil mais avec un fichier txt
    """
    correct_data = {
        "Username": {
            "name": ["Username"],
            "unit": None,
            "data": ['booker12', 'grey07', 'johnson81', 'jenkins46', 'smith79']
        },
        "Registered": {
            "name": ["Registered"],
            "unit": None,
            "data": [True, False, False, True, True]
        },
        "First name": {
            "name": ["First name"],
            "unit": None,
            "data": ['Rachel', 'Laura', 'Craig', 'Mary', 'Jamie']
        },
        "Last name": {
            "name": ["Last name"],
            "unit": None,
            "data": ['Booker', 'Grey', 'Johnson', 'Jenkins', 'Smith']
        } 
    }
    assert correct_data == reader.read_file(username)


def test_valid_xlsx_file_pandas():
    """ Pareil mais avec un fichier excel et avec pandas
    """
    correct_data = {
        "0": {
            "name": ["0"],
            "unit": None,
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9]
        },
        "First Name": {
            "name": ["First Name"],
            "unit": None,
            "data": ['Dulce', 'Mara', 'Philip', 'Kathleen', 'Nereida', 'Gaston', 'Etta', 'Earlean', 'Vincenza']
        },
        "Last Name": {
            "name": ["Last Name"],
            "unit": None,
            "data": ['Abril', 'Hashimoto', 'Gent', 'Hanner', 'Magwood', 'Brumm', 'Hurn', 'Melgar', 'Weiland']
        },
        "Gender": {
            "name": ["Gender"],
            "unit": None,
            "data": ['Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female']
        },
        "Country": {
            "name": ["Country"],
            "unit": None,
            "data": ['United States', 'Great Britain', 'France', 'United States', 'United States', 'United States', 'Great Britain', 'United States', 'United States']
        },
        "Age": {
            "name": ["Age"],
            "unit": None,
            "data": [32, 25, 36, 25, 58, 24, 56, 27, 40]
        },
        "Date": {
            "name": ["Date"],
            "unit": None,
            "data": ['15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015']
        },
        "Height.cm": {
            "name": ["Height"],
            "unit": ["cm"],
            "data": [156.2, 158.25, 158.74, 154.92, 146.89, 155.46, 159.87, 145.61, 154.8]
        }
    }
    assert correct_data == reader.read_file(excel)


def test_valid_xlsx_file_openpyxl():
    """ Pareil mais avec un fichier excel et avec openpyxl
    """
    correct_data = {
        "0": {
            "name": ["0"],
            "unit": None,
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9]
        },
        "First Name": {
            "name": ["First Name"],
            "unit": None,
            "data": ['Dulce', 'Mara', 'Philip', 'Kathleen', 'Nereida', 'Gaston', 'Etta', 'Earlean', 'Vincenza']
        },
        "Last Name": {
            "name": ["Last Name"],
            "unit": None,
            "data": ['Abril', 'Hashimoto', 'Gent', 'Hanner', 'Magwood', 'Brumm', 'Hurn', 'Melgar', 'Weiland']
        },
        "Gender": {
            "name": ["Gender"],
            "unit": None,
            "data": ['Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female']
        },
        "Country": {
            "name": ["Country"],
            "unit": None,
            "data": ['United States', 'Great Britain', 'France', 'United States', 'United States', 'United States', 'Great Britain', 'United States', 'United States']
        },
        "Age": {
            "name": ["Age"],
            "unit": None,
            "data": [32, 25, 36, 25, 58, 24, 56, 27, 40]
        },
        "Date": {
            "name": ["Date"],
            "unit": None,
            "data": ['15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015']
        },
        "Height.cm": {
            "name": ["Height"],
            "unit": ["cm"],
            "data": [156.2, 158.25, 158.74, 154.92, 146.89, 155.46, 159.87, 145.61, 154.8]
        }
    }
    assert correct_data == reader.read_file(excel, engine='openpyxl')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que les bonnes erreurs sont renvoyées quand un fichier n'existe pas
# ------------------------------------------------------------------------------------------------------------------------
def test_csv_file_not_exist():
    """ Vérifie qu'un fichier csv qui n'existe pas donne None et le bon message d'erreur
    """
    assert None == reader.read_file(not_exist + ".csv")
    assert "Erreur : Le fichier 'not_exist.csv' n'existe pas" == reader.get_error()
   
    
def test_tsv_file_not_exist():
    """ Pareil mais avec un fichier tsv
    """
    assert None == reader.read_file(not_exist + ".tsv")
    assert "Erreur : Le fichier 'not_exist.tsv' n'existe pas" == reader.get_error()
   
    
def test_txt_file_not_exist():
    """ Pareil mais avec un fichier txt
    """
    assert None == reader.read_file(not_exist + ".txt")
    assert "Erreur : Le fichier 'not_exist.txt' n'existe pas" == reader.get_error()


def test_xlsx_file_not_exist():
    """ Pareil mais avec un fichier excel
    """
    assert None == reader.read_file(not_exist + ".xlsx")
    assert "Erreur : Le fichier 'not_exist.xlsx' n'existe pas" == reader.get_error()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test pour vérifier la bonne erreur quand le fichier n'est pas pris en charge par l'outil
# ------------------------------------------------------------------------------------------------------------------------
def test_unsupported_file():
    """ Vérifie qu'un fichier qui existe mais qui n'est pas pris en charge par l'outil retourne None
        et vérifie le message d'erreur
    """
    assert None == reader.read_file(cant_read)
    assert "Erreur : Le fichier 'cant_read.py' n'est pas pris en charge par l'application" == reader.get_error()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que les données sont correctes pendant la lecture
# ------------------------------------------------------------------------------------------------------------------------
def test_nb_column_diff():
    """ Vérifie qu'un fichier où il manque des données dans une colonne donne une erreur
    """
    assert None == reader.read_file(nb_col_diff)
    assert "Erreur : le nombre d'éléments à la ligne 3 est différent du nombre de colonnes 2"


def test_type_diff():
    """ Vérifie que les différents types de données d'une colonne donne une erreur
    """
    assert None == reader.read_file(type_diff)
    assert "Erreur : L'élément de la colonne Word et de la ligne 2 est différent des éléments de cette colonne" == reader.get_error()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que les bonnes erreurs lorsque'on sélectionne un mauvais moteur
# ------------------------------------------------------------------------------------------------------------------------
def test_probleme_read_pandas():
    """ Vérifie que lorsqu'on donne n'importe quel moteur pour la lecture des fichiers excel.
        On obtient une erreur si ce n'est pas les bons moteurs.
    """
    assert None == reader.read_file(excel, engine='no_engine')
    assert "Erreur : La lecture des fichiers excel se fait soit avec 'pandas', soit 'openpyxl'" == reader.get_error()
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
