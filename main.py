from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.Application import Application


def run():
    gesanalysis = GESAnalysis()

    controleur = Controleur(gesanalysis)
    application = Application(gesanalysis, controleur)
    application.run()

if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()