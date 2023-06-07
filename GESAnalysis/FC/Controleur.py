class Controleur:
    """ Class to change the data from the model when
        there is an input from the UI
    """
    
    def __init__(self, model) -> None:
        self.__gesanalysis = model
        
        
    def close_files(self, list_file):
        for file in list_file:
            self.__gesanalysis.close_file(file)
        
        self.__gesanalysis.update()