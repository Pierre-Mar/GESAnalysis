from GESAnalysis.FC.ReaderData import ReaderData
from GESAnalysis.UI.plot.DistanceMode import DistanceMode

def run():
    r = ReaderData()
    d = r.read_file("/home/pierre/Documents/python/files_gesanalyser/files/2019_missions.txt")
    
    dist = DistanceMode([(d, "2019")])
    dist = DistanceMode([(d, "2019"), (d, '2020')])
    dist = DistanceMode([(d, "2019"), (d, '2020'), (d, '2021')])
    dist = DistanceMode([(d, "2019"), (d, '2020'), (d, '2021'), (d, '2022')])

if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()