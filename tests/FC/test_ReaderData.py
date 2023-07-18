import pytest
import platform
from GESAnalysis.FC.ReaderData import ReaderData


reader = ReaderData()


# Définition of paths of files depending on the OS
# Configure path to file
os_name = platform.system()
path = "tests/resources/"
if os_name == "Windows":
    path = "tests\\resources\\"
people = path + "people.csv"
hw_5 = path + "hw_5.tsv"
username = path + "username.txt"
excel = path + "file_example_XLSX_10.xlsx"
export_invalid = path + "export_invalid.py"
not_exist = path + "not_exist"
cant_read = path + "cant_read.py"
nb_col_diff = path + "nb_col_diff.txt"
type_diff = path + "type_diff.txt"


# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename, sep)
# ------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------
# Tests to check when the reading is correct
# ------------------------------------------------------------------------------------------------------------------------
def test_valid_csv_file():
    """ Check the reading of a CSV file
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

    assert correct_data == reader.read_file(people, sep=",")


def test_valid_tsv_file():
    """ Same with a TSV file
    """
    correct_data = {
        'Index': {
            'name': ['Index'],
            'unit': [],
            'data': [[1], [2], [3], [4], [5]],
            'type': int
        },
        'height.cm': {
            'name': ['height'],
            'unit': ['cm'],
            'data': [[165], [180.49], [175.26], [172.72], [170.18]],
            'type': float
        },
        'weight.kg': {
            'name': ['weight'],
            'unit': ['kg'],
            'data': [[50.8], [61.69], [69.4], [64.0], [65.32]],
            'type': float
        }
    }
    assert correct_data == reader.read_file(hw_5)


def test_valid_txt_file():
    """ Same with a TXT file
    """
    correct_data = {
        'Username': {
            'name': ['Username'],
            'unit': [],
            'data': [['booker12', 'mandatory45'], ['grey07', '0503'], ['johnson81', 'oklmPerson'], ['jenkins46', '35.2'], ['smith79', 'hihi']],
            'type': str
        },
        'Registered': {
            'name': ['Registered'],
            'unit': [],
            'data': [[True], [False], [False], [True], [True]],
            'type': bool
        },
        'First name': {
            'name': ['First name'],
            'unit': [],
            'data': [['Rachel'], ['Laura'], ['Craig'], ['Mary'], ['Jamie']],
            'type': str
        },
        'Last name': {
            'name': ['Last name'],
            'unit': [],
            'data': [['Booker'], ['Grey'], ['Johnson'], ['Jenkins'], ['Smith']],
            'type': str
        }
    }
    assert correct_data == reader.read_file(username)


def test_valid_xlsx_file_pandas():
    """ Same with a XLSX file and pandas, the reading engine
    """
    correct_data = {
        '0': {
            'name': ['0'],
            'unit': [],
            'data': [[1], [2], [3], [4], [5], [6], [7], [8], [9]],
            'type': int
        }, 
        'First Name': {
            'name': ['First Name'],
            'unit': [],
            'data': [['Dulce'], ['Mara'], ['Philip'], ['Kathleen'], ['Nereida'], ['Gaston'], ['Etta'], ['Earlean'], ['Vincenza']],
            'type': str
        },
        'Last Name': {
            'name': ['Last Name'],
            'unit': [],
            'data': [['Abril'], ['Hashimoto'], ['Gent'], ['Hanner'], ['Magwood'], ['Brumm'], ['Hurn'], ['Melgar'], ['Weiland']], 
            'type': str
        },
        'Gender': {
            'name': ['Gender'],
            'unit': [],
            'data': [['Female'], ['Female'], ['Male'], ['Female'], ['Female'], ['Male'], ['Female'], ['Female'], ['Female']],
            'type': str
        },
        'Country': {
            'name': ['Country'],
            'unit': [],
            'data': [['United States'], ['Great Britain'], ['France'], ['United States'], ['United States'], ['United States'], ['Great Britain'], ['United States'], ['United States']],
            'type': str
        },
        'Age': {
            'name': ['Age'],
            'unit': [],
            'data': [[32], [25], [36], [25], [58], [24], [56], [27], [40]],
            'type': int
        },
        'Date': {
            'name': ['Date'],
            'unit': [],
            'data': [['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015']],
            'type': str
        },
        'Height.cm': {
            'name': ['Height'],
            'unit': ['cm'],
            'data': [[156.2], [158.25], [158.74], [154.92], [146.89], [155.46], [159.87], [145.61], [154.8]],
            'type': float
        }
    }
    assert correct_data == reader.read_file(excel)


def test_valid_xlsx_file_openpyxl():
    """ Same with a XLSX file and openpyxl, the reading engine
    """
    correct_data = {
        '0': {
            'name': ['0'],
            'unit': [],
            'data': [[1], [2], [3], [4], [5], [6], [7], [8], [9]],
            'type': int
        }, 
        'First Name': {
            'name': ['First Name'],
            'unit': [],
            'data': [['Dulce'], ['Mara'], ['Philip'], ['Kathleen'], ['Nereida'], ['Gaston'], ['Etta'], ['Earlean'], ['Vincenza']],
            'type': str
        },
        'Last Name': {
            'name': ['Last Name'],
            'unit': [],
            'data': [['Abril'], ['Hashimoto'], ['Gent'], ['Hanner'], ['Magwood'], ['Brumm'], ['Hurn'], ['Melgar'], ['Weiland']], 
            'type': str
        },
        'Gender': {
            'name': ['Gender'],
            'unit': [],
            'data': [['Female'], ['Female'], ['Male'], ['Female'], ['Female'], ['Male'], ['Female'], ['Female'], ['Female']],
            'type': str
        },
        'Country': {
            'name': ['Country'],
            'unit': [],
            'data': [['United States'], ['Great Britain'], ['France'], ['United States'], ['United States'], ['United States'], ['Great Britain'], ['United States'], ['United States']],
            'type': str
        },
        'Age': {
            'name': ['Age'],
            'unit': [],
            'data': [[32], [25], [36], [25], [58], [24], [56], [27], [40]],
            'type': int
        },
        'Date': {
            'name': ['Date'],
            'unit': [],
            'data': [['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015'], ['15/10/2017'], ['16/08/2016'], ['21/05/2015']],
            'type': str
        },
        'Height.cm': {
            'name': ['Height'],
            'unit': ['cm'],
            'data': [[156.2], [158.25], [158.74], [154.92], [146.89], [155.46], [159.87], [145.61], [154.8]],
            'type': float
        }
    }
    assert correct_data == reader.read_file(excel, engine='openpyxl')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests to check if the errors are catched when a file don't exist
# ------------------------------------------------------------------------------------------------------------------------
def test_csv_file_not_exist():
    """ Check a CSV file, who don't exist, gives an error
    """
    with pytest.raises(FileNotFoundError, match="Le fichier 'not_exist.csv' n'existe pas"):
        reader.read_file(not_exist + ".csv")
   
    
def test_tsv_file_not_exist():
    """ Same with a TSV file
    """
    with pytest.raises(FileNotFoundError, match="Le fichier 'not_exist.tsv' n'existe pas"):
        reader.read_file(not_exist + ".tsv")
   
    
def test_txt_file_not_exist():
    """ Same with a TXT file
    """
    with pytest.raises(FileNotFoundError, match="Le fichier 'not_exist.txt' n'existe pas"):
        reader.read_file(not_exist + ".txt")


def test_xlsx_file_not_exist():
    """ Same with a XLSX file
    """
    with pytest.raises(FileNotFoundError, match="Le fichier 'not_exist.xlsx' n'existe pas"):
        reader.read_file(not_exist + ".xlsx")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test to check if the error is catched when the file are not supported by the application
# ------------------------------------------------------------------------------------------------------------------------
def test_unsupported_file():
    """ Check if we catch the corresponding error when a file are not supported by the application
    """
    with pytest.raises(TypeError, match="Exportation impossible de 'cant_read.py'. Le fichier doit être de type CSV, TSV, TXT ou XLSX"):
        reader.read_file(cant_read)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests to check the data during the reading
# ------------------------------------------------------------------------------------------------------------------------
def test_nb_column_diff():
    """ Check a file where some data missing and give an error
    """
    with pytest.raises(ValueError, match="La ligne 4 a 1 éléments mais il y a 2 colonnes"):
        reader.read_file(nb_col_diff)


def test_type_diff():
    """ Check when there are different types in a column give an error
    """
    with pytest.raises(TypeError, match="L'élément à la ligne 3 et colonne Word est du type int au lieu du type str"):
        reader.read_file(type_diff)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test to check if we get an error when we give the wrong engine
# ------------------------------------------------------------------------------------------------------------------------
def test_probleme_read_pandas():
    """ Check when we give a wrong reading engine give an error
    """
    with pytest.raises(ValueError, match="'no_engine' n'est pas un moteur de lecture. Utilisez 'pandas' ou 'openpyxl'"):
        reader.read_file(excel, engine='no_engine')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
