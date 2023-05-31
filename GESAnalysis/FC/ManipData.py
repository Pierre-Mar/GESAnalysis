from GESAnalysis.FC.ExportData import ExportData
from GESAnalysis.FC.ReaderData import ReaderData

class ManipData:
    
    __reader = ReaderData()
    __export = ExportData()

    
    def __init__(self, filename=None):
        """ Initialisation de la classe et lecture du fichier 'filename'

        Args:
            filename (str, optional): lecture du fichier 'filename' si filename est différent de None. Defaults to None.
        """
        # Initialisation de base
        self.__filename = filename
        self.__error_msg = None
        self.__data_dict = None
        
        if filename is None:
            return
        
        # Lecture du fichier si il est précisé
        self.__data_dict = self.__reader.read_file(self.__filename)
        if self.__data_dict == None:
            self.__error_msg = self.__reader.get_error()
            

    def read_file(self, filename, sep=None, engine="pandas"):
        """ Lecture du fichier 'filename'

        Args:
            filename (str): chemin vers le fichier
            sep (str, optional): Séparateur entre les valeurs du fichier. Defaults to None.
            engine (str, optional): Moteur de lecture pour les fichiers xlsx. Defaults to "pandas".
        """
        self.__filename = filename
        self.__data_dict = self.__reader.read_file(filename, sep, engine)
        if self.__data_dict == None:
            self.__error_msg = self.__reader.get_error()
            
            
    def export(self, fileout):
        """ Ecriture des données dans le fichier 'fileout'

        Args:
            fileout (str): chemin vers le fichier
        """
        if not self.__export.export_data(self.__data_dict, fileout):
            self.__error_msg = self.__export.get_error()
            
            
    def get_error(self):
        """ Retourne le message d'erreur

        Returns:
            str: le message d'erreur
        """
        return self.__error_msg
    
    def get_data(self):
        """ Retourne le dictionnaire contenant les données

        Returns:
            dict: dictionnaire de données
        """
        return self.__data_dict
    
    def get_filename(self):
        """ Retourne le nom du fichier qui a été lu

        Returns:
            str: chemin du fichier
        """
        return self.__filename