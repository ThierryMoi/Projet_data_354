
import os
import pandas as pd
from datetime import datetime
from multiprocessing import Pool, cpu_count
from Extraction.globalParamettre import cheminProjet
from Extraction.requettage import requete_api


# Cette fonction va créer l'arborescence en fonction du sujet qui lui est transmis.
def chemin(sujet):
    path_sujet = os.path.join(cheminProjet, sujet)
    path_annee = os.path.join(path_sujet, str(datetime.now().year))
    path_mois = os.path.join(path_annee, str(datetime.now().month))
    return path_mois


# Lorsque l'on a un seul sujet à faire des recherches dessus,
# on récupère les données et ensuite nous les stockons dans un répertoire spécifique.
def stockage_with_one_subject(sujet):
    base_current = requete_api(sujet)
    path = chemin(sujet)
    os.makedirs(path, exist_ok=True)
    path_jour = os.path.join(path, str(datetime.now().day))
    pd.DataFrame(base_current).to_csv(path_jour + ".csv")
    return "success"


# Lorsque nous désirons effectuer des recherches sur plusieurs sujets,
# cette fonction nous permet de paralléliser le processus en tenant compte du nombre de CPU de notre machine hôte.
def stockage_with_many_subject(sujets):
    path_list = [chemin(i) for i in sujets]
    pool = Pool(processes=min(cpu_count(), len(sujets)))
    result_list = pool.map(requete_api, sujets)
    pool.close()
    pool.join()
    for i in range(len(result_list)):
        os.makedirs(path_list[i], exist_ok=True)
        path_jour = os.path.join(path_list[i], str(datetime.now().day))
        pd.DataFrame(result_list[i]).to_csv(path_jour + ".csv")
    return "success"
    

