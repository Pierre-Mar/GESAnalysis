import pytest
import platform
from GESAnalysis.FC.GESAnalysis import GESAnalysis
import os


# Définition of paths of files depending on the OS
os_name = platform.system()
path_file = "tests/resources/"
if os_name == "Windows":
    path_file = "tests\\resources\\"
people = path_file + "people.csv"
export_invalid = path_file + "export_invalid.py"
not_exist = path_file + "not_exist"


m = GESAnalysis()

# ------------------------------------------------------------------------------------------------------------------------
# Tests : read_file(filename)
# ------------------------------------------------------------------------------------------------------------------------
def test_read_file():
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
    m.read_file(people)
    assert correct_data == m.get_data(people)
    
    
def test_read_file_incorrect():    
    with pytest.raises(Exception, match="cannot read data from 'export_invalid.py'. Should be a CSV, TSV, TXT or XLSX file"):
        m.read_file(export_invalid)


def test_read_file_path_null():
    with pytest.raises(Exception, match="cannot read file because the path is null"):
        m.read_file(None)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

# def test_initialisation_incorrect():
#     """ Test when the initialisation is incorrect
#     """
#     with pytest.raises(TypeError, match="cannot read data from 'export_invalid.py'. Should be a CSV, TSV, TXT or XLSX file"):
#         m = ManipData(export_invalid)
# # ------------------------------------------------------------------------------------------------------------------------
# # ------------------------------------------------------------------------------------------------------------------------



# # ------------------------------------------------------------------------------------------------------------------------
# # Tests : read_file(filename, sep, engine)
# # ------------------------------------------------------------------------------------------------------------------------
# def test_read_file():
#     """ Test the reading of the file 'filename'
#     """
#     m = ManipData()
#     correct_data = {
#         'SR': {
#             "name": ["SR"],
#             "unit": [],
#             "data": [1, 2, 3, 4, 5]
#         },
#         'NAME': {
#             "name": ["NAME"],
#             "unit": [],
#             "data": ['Dett', 'Nern', 'Kallsie', 'Siuau', 'Shennice']
#         },
#         'GENDER': {
#             "name": ["GENDER"],
#             "unit": [],
#             "data": ['Male', 'Female', 'Male', 'Female', 'Male']
#         },
#         'AGE': {
#             "name": ["AGE"],
#             "unit": [],
#             "data": [18, 19, 20, 21, 22]
#         },
#         'DATE': {
#             "name": ["DATE"],
#             "unit": [],
#             "data": ['21/05/2015', '15/10/2017', '16/08/2016', '21/05/2015', '21/05/2016']
#         }
#     }
#     m.read_file(people)
#     assert people == m.get_filename()
#     assert correct_data == m.get_data()
    

# def test_read_file_incorrect():
#     """ Test the reading of the file when there is an error
#     """
#     m = ManipData()
#     with pytest.raises(TypeError, match="cannot read data from 'export_invalid.py'. Should be a CSV, TSV, TXT or XLSX file"):
#         m.read_file(export_invalid)
# # ------------------------------------------------------------------------------------------------------------------------
# # ------------------------------------------------------------------------------------------------------------------------



# # ------------------------------------------------------------------------------------------------------------------------
# # Tests : export(fileout)
# # ------------------------------------------------------------------------------------------------------------------------
# def test_export():
#     """ Test the exporation of data to a file
#     """
#     m = ManipData(people)
#     m.export("tmp.csv")
#     os.remove("tmp.csv")
    

# def test_export_incorrect():
#     """ Test the exportation of a file when there is an error
#     """
#     m = ManipData()
#     with pytest.raises(TypeError, match="cannot access to values because the dictionary is null"):
#         m.export("tmp.txt")
# # ------------------------------------------------------------------------------------------------------------------------
# # ------------------------------------------------------------------------------------------------------------------------