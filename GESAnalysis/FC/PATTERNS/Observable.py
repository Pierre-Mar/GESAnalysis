from GESAnalysis.FC.PATTERNS.Observer import Observer
from typing import List, Tuple


class Observable:
    """ Update the UI when the model change
    """
    
    def __init__(self) -> None:
        """ Initialise a list of observers
        """
        self.__observer: List[Tuple[Observer, str]] = []


    def add_observer(self, o: Observer, c: str) -> None:
        """ Add an observer to the list

        Args:
            o (Observer): Observer
            c (str): Category of the observer
        """
        self.__observer.append((o, c))


    def remove_observer(self, o: Tuple[Observer, str]) -> None:
        """ Remove an observe from the list

        Args:
            o (Tuple[Observer, str]): Observer
        """
        try:
            self.__observer.remove(o)
        except ValueError:
            pass


    def update(self, c:str) -> None:
        """ Update the observers from the category c

        Args:
            c (str): Category
        """
        for observer, category in self.__observer:
            if category == c:
                observer.update()
