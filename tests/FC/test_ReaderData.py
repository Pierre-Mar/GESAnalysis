import pytest
from GESAnalysis.FC.ReaderData import ReaderData


reader = ReaderData()

# -----------------------------------------------------------------------------------------------
# Tests : read_file(filename, sep)

def test_valid_csv_file():
    """ Vérifie que la lecture d'un fichier csv se fasse correctement
    """
    correct_data = {
        'SR.': [1, 2, 3, 4, 5],
        'NAME': ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice'],
        'GENDER': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'AGE': [18, 19, 20, 21, 22],
        'DATE': ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
    }
    assert correct_data == reader.read_file("tests/resources/people.csv", sep=",")
    
def test_valid_tsv_file():
    """ Pareil mais avec un fichier tsv
    """
    correct_data = {
        'Index': [1, 2, 3, 4, 5],
        '" Height(Inches)"""': [65.78, 71.52, 69.4, 68.22, 67.79],
        '" ""Weight(Pounds)"""': [112.99, 136.49, 153.03, 142.34, 144.3]
    }
    
    assert correct_data == reader.read_file("tests/resources/hw_5.tsv")
    
def test_valid_txt_file():
    """ Pareil mais avec un fichier txt
    """
    correct_data = {
        'Username': ['booker12', 'grey07', 'johnson81', 'jenkins46', 'smith79'],
        'Registered': [True, False, False, True, True],
        'First name': ['Rachel', 'Laura', 'Craig', 'Mary', 'Jamie'],
        'Last name': ['Booker', 'Grey', 'Johnson', 'Jenkins', 'Smith']
    }
    
    assert correct_data == reader.read_file("tests/resources/username.txt")
    
def test_valid_xlsx_file():
    """ Pareil mais avec un fichier excel
    """
    correct_data = {
        '0': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'First Name': ['Dulce', 'Mara', 'Philip', 'Kathleen', 'Nereida', 'Gaston', 'Etta', 'Earlean', 'Vincenza'],
        'Last Name': ['Abril', 'Hashimoto', 'Gent', 'Hanner', 'Magwood', 'Brumm', 'Hurn', 'Melgar', 'Weiland'],
        'Gender': ['Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female'],
        'Country': ['United States', 'Great Britain', 'France', 'United States', 'United States', 'United States', 'Great Britain', 'United States', 'United States'],
        'Age': [32, 25, 36, 25, 58, 24, 56, 27, 40],
        'Date': ['15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015'],
        'Id': [1562, 1582, 2587, 3549, 2468, 2554, 3598, 2456, 6548]
    }

    assert correct_data == reader.read_file("tests/resources/file_example_XLSX_10.xlsx")


def test_csv_file_not_exist():
    """ Vérifie qu'un fichier csv qui n'existe pas donne None et le bon message d'erreur
    """
    assert None == reader.read_file("tests/resources/not_exist.csv")
    assert "Erreur : Le fichier 'not_exist.csv' n'existe pas" == reader.get_error()
    
def test_tsv_file_not_exist():
    """ Pareil mais avec un fichier tsv
    """
    assert None == reader.read_file("tests/resources/not_exist.tsv")
    assert "Erreur : Le fichier 'not_exist.tsv' n'existe pas" == reader.get_error()
    
def test_txt_file_not_exist():
    """ Pareil mais avec un fichier txt
    """
    assert None == reader.read_file("tests/resources/not_exist.txt")
    assert "Erreur : Le fichier 'not_exist.txt' n'existe pas" == reader.get_error()

def test_xlsx_file_not_exist():
    """ Pareil mais avec un fichier excel
    """
    assert None == reader.read_file("tests/resources/not_exist.xlsx")
    assert "Erreur : Le fichier 'not_exist.xlsx' n'existe pas" == reader.get_error()
    
    
def test_unsupported_file():
    """ Vérifie qu'un fichier qui existe mais qui n'est pas pris en charge par l'outil retourne None
        et vérifie le message d'erreur
    """
    assert None == reader.read_file("tests/resources/cant_read.py")
    assert "Erreur : Le fichier 'cant_read.py' n'est pas pris en charge par l'application" == reader.get_error()
    
def test_nb_column_diff():
    """ Vérifie qu'un fichier où il manque des données dans une colonne donne une erreur
    """
    assert None == reader.read_file("tests/resources/nb_col_diff.txt")
    assert "Erreur : le nombre d'éléments à la ligne 3 est différent du nombre de colonnes 2"
    
def test_type_diff():
    """ Vérifie que les différents types de données d'une colonne donne une erreur
    """
    assert None == reader.read_file("tests/resources/type_diff.txt")
    assert "Erreur : L'élément de la colonne Word et de la ligne 2 est différent des éléments de cette colonne" == reader.get_error()
