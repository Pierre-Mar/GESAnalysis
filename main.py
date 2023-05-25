from GESAnalysis.FC.ReaderData import ReaderData
from GESAnalysis.FC.ExportData import ExportData

def run():
    r = ReaderData()
    e = ExportData()
    d = r.read_file("tests/resources/file_example_XLSX_10.xlsx")
    if d is None:
        print(r.get_error())
    else:
        if not e.export_data(d, "here.tsv"):
            print(e.get_error_msg())
        else:
            print(r.read_file("here.tsv", '\t'))


if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()