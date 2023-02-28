from multiprocessing import Pool, cpu_count
import Extraction.globalParamettre
from datetime import date, datetime
from pynytimes import NYTAPI

# Cette fonction à pour but de recuperer les articles d'un sujet particulier
# sur une période données
# Elle renvoie une liste de dictionnaire 

def requete_api(sujet):
    # Nous utilisons la dépendance de l'API intégrée à Python
    # Initialisation d'une instance de requêtage
    nyt = NYTAPI(key=Extraction.global_paramettre.key_api, parse_dates=True)
    # Essayons d'accéder à la ressource en utilisant article_search qui effectue une requête GET sur le point de terminaison
    try:
        output_requete = nyt.article_search(
            query=str(sujet),
            # Prendre les informations du jour
            dates={"begin": datetime.now().date(), "end": datetime.now().date()},
            options={}
        )
    except:
        output_requete = {"message": "Erreur sur la requête"}
    
    return output_requete




# Cette fonction sera utilisée si l'on a plusieurs sujets à traiter
# Elle va paralléliser la tâche de récupération
def multiprocessing(fonction, liste):
    with Pool(cpu_count()) as p:
        print(cpu_count())
        rec = p.map(fonction, liste)
        p.terminate()
        p.join()

        return rec




