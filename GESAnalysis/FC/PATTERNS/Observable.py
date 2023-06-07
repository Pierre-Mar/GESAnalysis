from GESAnalysis.FC.PATTERNS.Observer import Observer
from typing import List

class Observable:
    
    """ Class to notify to update the UI when the data
        change
    """
    
    def __init__(self) -> None:
        """ Initialise a list of observers
        """
        self.__observer: List[Observer] = []


    def add_observer(self, o: Observer) -> None:
        """ Add an observer to the list

        Args:
            o (Observer): An observer
        """
        self.__observer.append(o)


    def remove_observer(self, o: Observer) -> None:
        """ Remove an observer

        Args:
            o (Observer): An Observer
        """
        try:
            self.__observer.remove(o)
        except ValueError:
            pass


    def update(self) -> None:
        """ Update all the observers
        """
        for observer in self.__observer:
            observer.update()