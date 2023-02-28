import json
import os
import glob
import pandas as pd
import itertools
import Extraction.globalParamettre


# Cette fonction récupère les chemins dans notre arborescence
def construction(chemin_projet, condition=None):
    chemin_liste = []
    for subdir in os.listdir(chemin_projet):
        if os.path.isdir(os.path.join(chemin_projet, str(subdir))):
            if condition is not None:
                if condition == subdir:
                    chemin_liste.append(os.path.join(chemin_projet, subdir))
                else:
                    chemin_liste.append(".")
            else:
                chemin_liste.append(os.path.join(chemin_projet, subdir))
    return chemin_liste


# Cette fonction lit les fichiers .csv dans le dossier donné et retourne la colonne 'abstract'
def lecture(folder_path, jour=None):
    main_dataframe = pd.DataFrame()
    if jour is not None:
        file_list = glob.glob(folder_path + "/" + str(jour) + ".csv")
    else:
        file_list = glob.glob(folder_path + "/*.csv")
    try:
        main_dataframe = pd.DataFrame(pd.read_csv(file_list[0]))
        for i in range(1, len(file_list)):
            data = pd.read_csv(file_list[i])
            df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe, df], axis=1)
        return main_dataframe['abstract']
    except:
        return print("erreur")


# Cette fonction récupère les données selon les paramètres spécifiés
def data(sujet=None, annee=None, mois=None, jour=None):
    anne_path = []
    mois_path = []
    # Cas où sujet est vide
    if sujet is not None:
        sujet_path = construction(Extraction.globalParamettre.cheminProjet, sujet)
    else:
        sujet_path = construction(Extraction.globalParamettre.cheminProjet)
    # Cas des années
    for s in sujet_path:
        if annee is not None:
            anne_path.append(construction(s), annee)
        else:
            anne_path.append(construction(s))
    flat_list = itertools.chain(*anne_path)
    anne_path = list(flat_list)
    for a in anne_path:
        if mois is not None:
            mois_path.append(construction(a), mois)
        else:
            mois_path.append(construction(a))
    flat_list = itertools.chain(*mois_path)
    mois_path = list(flat_list)
    print(mois_path)
    data_liste = []
    for m in mois_path:
        try:
            if jour is not None:
                data_liste.append(lecture(m, jour).to_dict())
            else:
                data_liste.append(lecture(m).to_dict())
        except:
            continue
    return data_liste
