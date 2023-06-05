# GESAnalysis
Outil permettant l'analyse des bilans de gaz à effet de serre

## Table of Contents
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Fonctionnalités](#fonctionnalités)

## Prérequis
Avant de pouvoir utiliser l'application sur votre poste, vous devez d'abord installer au minimum :
* [python3](https://www.python.org/downloads/)
* pip (voir [Documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/))


Si vous le souhaitez, vous pouvez installer et utiliser un environnement virtuel tel que :
* venv (voir [Documentation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/))
* conda (voir [Documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))

## Installation
Une fois que vous avez les prérequis, vous allez devoir installer les paquets nécessaires à l'exécution du programme. Pour cela, vous allez exécuter les instructions suivantes :

1. Ouvrir un terminal


2. Si vous utilisez venv comme environnement virtuel, vous devez activer cet environnement :
    * Sous Unix/MacOS : `source env/bin/activate`
    * Sous Windows : `.\env\Scripts\activate`


3. Installer les paquets avec pip :
    * pip : `pip install -r requirements.txt`


4. Setup python path
    * Sous Unix/MacOS : `export PYTHONPATH=$(pwd)`
    * Sous Windows : `set PYTHONPATH=%cd%`


NB : Lorsque vous ouvrez un nouveau terminal, si vous voulez lancer le programme, vous devez setup python path

## Fonctionnalités

### Lecture de données
L'application peut lire des données depuis un fichier csv, tsv, txt et excel (xlsx).
Vous allez devoir créer une instance de ManipData d'abord :
```python
from GESAnalysis.FC.ManipData import ManipData
data = ManipData()
```

Pour lire les données, vous devez utiliser la méthode read_file(). Vous avez plusieurs choix possibles :

En spécifiant le chemin du fichier à lire
```python
d = data.read_file("file.ext")
```

En spécifiant le chemin du fichier à lire et le délimiteur dans le fichier (utile pour les fichiers csv, tsv et txt)
```python
d = data.read_file("file.ext", sep='sep')
```

En spécifiant le chemin du fichier à lire et le moteur de lecture pour les fichiers excel. Les moteurs de lecture sont **pandas** et **openpyxl**
```python
d = data.read_file("file.ext", engine='engine')
```

### Exportation des données
L'application peut écrire les données lues d'un fichier dans un fichier csv, tsv et txt.
Pour cela, vous devez utiliser la méthode export().

Vous devez spécifier le chemin du fichier dans lequel vous devez écrire
```python
data.export("file_to_write.ext")
```

### Erreurs
Si une erreur s'est produite pendant l'exécution du programme, vous pouvez voir quelle erreur s'est produite avec la méthode get_error()
```python
data.get_error()
```