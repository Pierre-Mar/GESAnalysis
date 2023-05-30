import matplotlib.pyplot as plt
import numpy as np
from GESAnalysis.FC.SortedData import SortedData

class DistanceMode:
    """ Classe permettant de représenter graphiquement
        la distance selon le mode de transport selon les années
    """
    
    __sorted_data = SortedData()
    
    def __init__(self, readerData_year_list):
        self.__configure_data(readerData_year_list)
        
        
    def __configure_data(self, readerData_list):
        self.__data = {}
        self.__year = []
        for reader, year in readerData_list:
            self.__year.append(year)
            # Récuperes les données du reader pour le mode et la distance
            mode = self.__get_column(reader, "mode")
            if mode is None:
                continue
            distance = self.__get_column(reader, "distance")
            if distance is None:
                continue
            
            for i in range(len(distance)):
                # Si le mode de transport n'est pas dans la structure,
                # on l'ajoute
                if mode[i] not in self.__data.keys():
                    self.__data[mode[i]] = {}
                    
                # Si l'année du mode n'est pas dans la structure,
                # on l'ajoute
                if year not in self.__data[mode[i]].keys():
                    self.__data[mode[i]][year] = 0
                
                self.__data[mode[i]][year] += distance[i]
            
               
    def draw(self):
        x = np.arange(len(list(self.__data.keys())))
        width = 0.25
        multiplier = 0
        
        for mode in self.__data.keys():
            for year, dist in self.__data[mode].items():
                print(year, dist)
                offset = width * multiplier
                # rect = self.__ax.bar(x+offset, dist, width, label=year)
                # self.__ax.bar_label(rect, padding=3)
                multiplier += 1
                print("-----")
                

        plt.show()

        
    def __get_column(self, reader, column):
        """ Retourne la colonne 'column' se trouvant dans le dictionnaire
        

        Args:
            reader (dict): Dictionnaire de données
            column (str): Nom de colonne

        Returns:
            list | None: Liste de données de la colonne 'column' s'il a trouvé. Sinon None
        """
        name_col = list(reader.keys())
        for c in name_col:
            if column == " ".join(reader[c]["name"]):
                return reader[c]["data"]
        return None
    
    def get_data(self):
        return self.__data