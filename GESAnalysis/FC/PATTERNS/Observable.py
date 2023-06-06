from GESAnalysis.FC.PATTERNS.Observer import Observer
from typing import List

class Observable:
    
    """ Class to notify to update the UI when the data
        change
    """
    
    def __init__(self) -> None:
        self.__observer: List[Observer] = []


    def add_observer(self, o: Observer) -> None:
        self.__observer.append(o)


    def remove_observer(self, o: Observer):
        try:
            self.__observer.remove(o)
        except ValueError:
            pass


    def update(self):
        for observer in self.__observer:
            observer.update()