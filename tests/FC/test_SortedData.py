import pytest
from GESAnalysis.FC.ReaderData import ReaderData
from GESAnalysis.FC.SortedData import SortedData

reader = ReaderData()
sort = SortedData()


def test_correct_column():
    d = reader.read_file("tests/resources/hw_5.tsv")
    correct_sort = [0, 4, 3, 2, 1]
    assert correct_sort == sort.sorted_by_column(d,"height")
    

def test_incorrect_column():
    d = reader.read_file("tests/resources/hw_5.tsv")
    assert None == sort.sorted_by_column(d, "not a column")
    
    
def test_correct_column_reverse():
    d = reader.read_file("tests/resources/hw_5.tsv")
    correct_sort = [4, 3, 0, 2, 1]
    assert correct_sort == sort.sorted_by_column(d, "weight", reversed=False)