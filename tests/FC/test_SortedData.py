import pytest
import platform
from GESAnalysis.FC.ReaderData import ReaderData
from GESAnalysis.FC.SortedData import SortedData

reader = ReaderData()
sort = SortedData()

# Définition des chemins de fichiers selon l'OS
hw_5 = "tests/resources/hw_5.tsv"
if platform.system() == "Windows":
    hw_5 = r"tests\resources\hw_5.tsv"

# ------------------------------------------------------------------------------------------------------------------------
# Tests : sorted_by_column(data_dict, name_column, reversed)
# ------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que le tri est correcte
# ------------------------------------------------------------------------------------------------------------------------
def test_correct_column():
    """ Test le tri avec un ordre croissant
    """
    d = reader.read_file(hw_5)
    correct_sort = [0, 4, 3, 2, 1]
    assert correct_sort == sort.sorted_by_column(d,"height")


def test_incorrect_column():
    """ Test le tri avec un ordre décroissant
    """
    d = reader.read_file(hw_5)
    assert None == sort.sorted_by_column(d, "not a column")
    assert "Erreur : il n'y a pas de colonne 'not a column'" == sort.get_error()
    
    
# ------------------------------------------------------------------------------------------------------------------------
# Tests pour vérifier que le tri est incorrecte avec un nom de colonne inexistant
# ------------------------------------------------------------------------------------------------------------------------
def test_correct_column_reverse():
    """ Vérifie que le tri ne se fait pas avec un nom de colonne inexistant
    """
    d = reader.read_file(hw_5)
    correct_sort = [4, 3, 0, 2, 1]
    assert correct_sort == sort.sorted_by_column(d, "weight", reversed=True)
  