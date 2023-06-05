import pytest
import platform
from GESAnalysis.FC.ReaderData import ReaderData


reader = ReaderData()


# Définition of paths of files depending on the OS
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
# Tests to check when the reading is correct
# ------------------------------------------------------------------------------------------------------------------------
def test_valid_csv_file():
    """ Check the reading of a CSV file
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
    assert correct_data == reader.read_file(people, sep=",")


def test_valid_tsv_file():
    """ Same with a TSV file
    """
    correct_data = {
        "Index": {
            "name": ["Index"],
            "unit": [],
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
    """ Same with a TXT file
    """
    correct_data = {
        "Username": {
            "name": ["Username"],
            "unit": [],
            "data": ['booker12', 'grey07', 'johnson81', 'jenkins46', 'smith79']
        },
        "Registered": {
            "name": ["Registered"],
            "unit": [],
            "data": [True, False, False, True, True]
        },
        "First name": {
            "name": ["First name"],
            "unit": [],
            "data": ['Rachel', 'Laura', 'Craig', 'Mary', 'Jamie']
        },
        "Last name": {
            "name": ["Last name"],
            "unit": [],
            "data": ['Booker', 'Grey', 'Johnson', 'Jenkins', 'Smith']
        } 
    }
    assert correct_data == reader.read_file(username)


def test_valid_xlsx_file_pandas():
    """ Same with a XLSX file and pandas, the reading engine
    """
    correct_data = {
        "0": {
            "name": ["0"],
            "unit": [],
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9]
        },
        "First Name": {
            "name": ["First Name"],
            "unit": [],
            "data": ['Dulce', 'Mara', 'Philip', 'Kathleen', 'Nereida', 'Gaston', 'Etta', 'Earlean', 'Vincenza']
        },
        "Last Name": {
            "name": ["Last Name"],
            "unit": [],
            "data": ['Abril', 'Hashimoto', 'Gent', 'Hanner', 'Magwood', 'Brumm', 'Hurn', 'Melgar', 'Weiland']
        },
        "Gender": {
            "name": ["Gender"],
            "unit": [],
            "data": ['Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female']
        },
        "Country": {
            "name": ["Country"],
            "unit": [],
            "data": ['United States', 'Great Britain', 'France', 'United States', 'United States', 'United States', 'Great Britain', 'United States', 'United States']
        },
        "Age": {
            "name": ["Age"],
            "unit": [],
            "data": [32, 25, 36, 25, 58, 24, 56, 27, 40]
        },
        "Date": {
            "name": ["Date"],
            "unit": [],
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
    """ Same with a XLSX file and openpyxl, the reading engine
    """
    correct_data = {
        "0": {
            "name": ["0"],
            "unit": [],
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9]
        },
        "First Name": {
            "name": ["First Name"],
            "unit": [],
            "data": ['Dulce', 'Mara', 'Philip', 'Kathleen', 'Nereida', 'Gaston', 'Etta', 'Earlean', 'Vincenza']
        },
        "Last Name": {
            "name": ["Last Name"],
            "unit": [],
            "data": ['Abril', 'Hashimoto', 'Gent', 'Hanner', 'Magwood', 'Brumm', 'Hurn', 'Melgar', 'Weiland']
        },
        "Gender": {
            "name": ["Gender"],
            "unit": [],
            "data": ['Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female']
        },
        "Country": {
            "name": ["Country"],
            "unit": [],
            "data": ['United States', 'Great Britain', 'France', 'United States', 'United States', 'United States', 'Great Britain', 'United States', 'United States']
        },
        "Age": {
            "name": ["Age"],
            "unit": [],
            "data": [32, 25, 36, 25, 58, 24, 56, 27, 40]
        },
        "Date": {
            "name": ["Date"],
            "unit": [],
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
# Tests to check if the errors are catched when a file don't exist
# ------------------------------------------------------------------------------------------------------------------------
def test_csv_file_not_exist():
    """ Check a CSV file, who don't exist, gives an error
    """
    with pytest.raises(FileNotFoundError, match="file 'not_exist.csv' not exist"):
        reader.read_file(not_exist + ".csv")
   
    
def test_tsv_file_not_exist():
    """ Same with a TSV file
    """
    with pytest.raises(FileNotFoundError, match="file 'not_exist.tsv' not exist"):
        reader.read_file(not_exist + ".tsv")
   
    
def test_txt_file_not_exist():
    """ Same with a TXT file
    """
    with pytest.raises(FileNotFoundError, match="file 'not_exist.txt' not exist"):
        reader.read_file(not_exist + ".txt")


def test_xlsx_file_not_exist():
    """ Same with a XLSX file
    """
    with pytest.raises(FileNotFoundError, match="file 'not_exist.xlsx' not exist"):
        reader.read_file(not_exist + ".xlsx")
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test to check if the error is catched when the file are not supported by the application
# ------------------------------------------------------------------------------------------------------------------------
def test_unsupported_file():
    """ Check if we catch the corresponding error when a file are not supported by the application
    """
    with pytest.raises(TypeError, match="cannot read data from 'cant_read.py'. Should be a CSV, TSV, TXT or XLSX file"):
        reader.read_file(cant_read)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Tests to check the data during the reading
# ------------------------------------------------------------------------------------------------------------------------
def test_nb_column_diff():
    """ Check a file where some data missing and give an error
    """
    with pytest.raises(ValueError, match="1 elements in line 4 but there is 2 columns"):
        reader.read_file(nb_col_diff)


def test_type_diff():
    """ Check when there are different types in a column give an error
    """
    with pytest.raises(TypeError, match="Element at row 3 and column Word has type int instead of type str"):
        reader.read_file(type_diff)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------
# Test to check if we get an error when we give the wrong engine
# ------------------------------------------------------------------------------------------------------------------------
def test_probleme_read_pandas():
    """ Check when we give a wrong reading engine give an error
    """
    with pytest.raises(ValueError, match="'no_engine' is not an engine to read a file. Use 'pandas' or 'openpyxl'"):
        reader.read_file(excel, engine='no_engine')
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
