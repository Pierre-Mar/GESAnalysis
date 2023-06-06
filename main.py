from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.Application import Application


def run():
    gesanalysis = GESAnalysis()
    gesanalysis.read_file("/home/pierre/Documents/python/files_gesanalyser/files/2019_missions.txt", '2019', 'Missions')

    controleur = Controleur(gesanalysis)
    application = Application(gesanalysis, controleur)
    application.run()

if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()