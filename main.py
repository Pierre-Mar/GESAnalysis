#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
from GESAnalysis.FC.GESAnalysis import GESAnalysis
from GESAnalysis.FC.Controleur import Controleur
from GESAnalysis.UI.Application import Application


def run() -> None:
    """ Create all the instance and run the application
    """
    gesanalysis = GESAnalysis()

    controleur = Controleur(gesanalysis)
    application = Application(gesanalysis, controleur)
    application.run()

if __name__ == "__main__":
    # Print a simple "Hello World !"
    # need to change it !
    run()
