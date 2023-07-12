from PyQt5 import QtWidgets

categories = ["Achats", "Déplacements domicile-travail", "Fluides", "Matériel Informatique", "Missions", "Total"]

def message_warning(string: str, parent) -> None:
    """ Display a warning box to the user

    Args:
        string (str): The message
    """
    dlg = QtWidgets.QMessageBox.warning(
        parent,
        "Avertissement",
        string
    )
    
def message_error(string: str, parent) -> None:
    """ Display a error box to the user

    Args:
        string (str): The message
    """
    dlg = QtWidgets.QMessageBox.critical(
        parent,
        "Erreur",
        string
    )
    
    
def message_ok(string: str, parent) -> None:
    """ Display a ok box to the user

    Args:
        string (str): The message
    """
    dlg = QtWidgets.QMessageBox.information(
        parent,
        "OK",
        string
    )