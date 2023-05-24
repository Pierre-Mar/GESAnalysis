import os
import csv

class ReaderData:
    
    accepted_extension = [".csv", ".txt", ".tsv", ".xlsx"]
    
    def __init__(self):
        pass
    
    
    def verify_file(self, filename):
        """ Vérifie que le fichier existe et qu'il peut être lu

        Args:
            filename (str): un nom de fichier (chemin)

        Returns:
            bool: retourne Vrai si le fichier existe et qu'il peut être lu, sinon Faux
        """
        # Recupère l'extension du fichier
        root_filename, self.ext = os.path.splitext(filename)
        
        return os.path.isfile(filename) and self.ext in self.accepted_extension
    
    def detect_delimiter(self, filename):
        """ Détectes le délimiteur qui se trouve dans filename

        Args:
            filename (str): un nom de fichier

        Returns:
            str: le délimiteur dans le fichier filename
        """
        sniffer = csv.Sniffer()
        
        # Récupère la 1ère ligne (nom des colonnes)
        head_line = None
        with open(filename, "r") as f:
            head_line = f.readline()
        
        dialect = sniffer.sniff(head_line)
        return dialect.delimiter