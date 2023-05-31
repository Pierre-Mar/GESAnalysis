import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class DistanceMode:
    """ Classe permettant de représenter graphiquement
        la distance selon le mode de transport selon les années
    """
    
    
    def __init__(self, readerData_year_list):
        self.__mode_ind = {} # Dictionnaire contenant le mode et son index associé
        self.__years_dist = {} # Dictionnaire contenant l'année et la distance
        self.__error_msg = None
        
        self.__fig, self.__ax = plt.subplots()
        self.__check_unit(readerData_year_list)
        self.__configure_data(readerData_year_list)
        
        # Creer une animation pour mettre à jour le graphe
        self.__ani = animation.FuncAnimation(
            self.__fig, self.__draw, interval=1000,cache_frame_data=False
        )
        plt.show()
    
    
    def add_data(self, readerData_year):
        """ Permet de rajouter des données pour les afficher sur le graphe

        Args:
            readerData_year (list): Liste de tuple contenant le dictionnaire de données et l'année
        """
        self.__check_unit(readerData_year)
        self.__configure_data(readerData_year)
        
        
    def remove_data(self, year_list):
        """ Supprimes les données des années

        Args:
            year_list (list): Liste de string contenant les années où nous voulons supprimer les données
        """
        for year in year_list:
            try:
                del self.__years_dist[year]
            except:
                pass
            
        
    def __configure_data(self, readerData_year):
        """ Crée le format de données nécessaires pour dessiner le graphe

        Args:
            readerData_year (list): Liste de tuple contenant un dictionnaire de données et l'année
        """
        # X-axis : clés (mode de transport)
        # Y-axis : année + distance
        ind_mode = 0
        for reader, year in readerData_year:
            # Récupères les données du reader pour le mode et la distance
            mode = self.__get_column(reader, "mode")
            if mode is None:
                continue
            
            distance = self.__get_column(reader, "distance")
            if distance is None:
                continue
            
            # On regarde le nombre de mode qu'il y a en associant un index
            for i in range(len(mode)):
                if mode[i] not in self.__mode_ind.keys():
                    self.__mode_ind[mode[i]] = ind_mode
                    ind_mode += 1
                    
            # On construit une liste avec où la valeur est la distance
            # du mode où l'index est associé dans le dictionnaire
            self.__years_dist[year] = [0 for i in range(len(list(self.__mode_ind.keys())))]
            
            # On calcule la distance pour chaque mode
            for i in range(len(distance)):
                   self.__years_dist[year][self.__mode_ind[mode[i]]] += distance[i]


    def __check_unit(self, readerData_year):
        """ Vérifie que l'unité de chaque distance par année est la même

        Args:
            readerData_year (list): liste de tuple contenant les données et l'année
        """
        self.__unit = ""
        for reader, year in readerData_year:
            unit_reader = self.__get_unit(reader, "distance")
            if unit_reader is None:
                self.__error_msg = "Erreur : l'unité de la distance pour l'année {0} n'est pas définie".format(year)
                break
            
            if self.__unit == "":
                self.__unit = "/".join(unit_reader)
                
            unit_reader = "/".join(unit_reader)
                
            if unit_reader != self.__unit:
                self.__error_msg = "Erreur : l'unité de la distance pour l'année {0} ({1}) est différent des autres unités ({2})".format(
                    year, unit_reader, self.__unit
                )
                break
              
 
    def __draw(self, i):
        """ Permets de dessiner le graphe avec matplotlib
        """
        self.__ax.clear()
        x = np.arange(len(list(self.__mode_ind.keys())))
        width = 0.3
        multiplier = 0
        
        for year, dist_mode in self.__years_dist.items():
            offset = width * multiplier
            self.__ax.bar(x+offset, dist_mode, width, label=year)
            multiplier += 1
                
        self.__ax.set_ylabel("Distance ({0})".format(self.__unit))
        self.__ax.set_xticks(x, list(self.__mode_ind.keys()))
        plt.legend()

        
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
    
    def __get_unit(self, reader, column):
        """ Retourne l'unité de la colonne 'column' se trouvant dans le dictionnaire
        

        Args:
            reader (dict): Dictionnaire de données
            column (str): Nom de colonne

        Returns:
            list | None: Liste contenant l'unité de la colonne 'column' s'il a trouvé. Sinon None
        """
        name_col = list(reader.keys())
        for c in name_col:
            if column == " ".join(reader[c]["name"]):
                return reader[c]["unit"]
        return None
    
    def get_data(self):
        return self.__data
    
    
    def get_error(self):
        return self.__error_msg