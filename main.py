from fastapi import FastAPI
from Extraction.stockage import *
from Traitement.connecteur import *
import Extraction.globalParamettre
from fastapi_amis_admin.admin import *
from fastapi_scheduler import SchedulerAdmin


# Instanciation de l'API
app = FastAPI()


# Création de l'instance "AdminSite"
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
# Création d'une instance du planificateur de tâches "SchedulerAdmin"
scheduler = SchedulerAdmin.bind(site)

# Définition de la tâche planifiée pour la route "/" tous les jours a 18h 00
@scheduler.scheduled_job('cron', hour=18, minute=0)
@app.get("/")
def requette():
    if len(Extraction.globalParamettre.sujet)!=0:
        return stockage_with_many_subject(Extraction.globalParamettre.sujet)
    elif len(Extraction.globalParamettre.sujet)==1:
        return stockage_with_one_subject(Extraction.globalParamettre.sujet)
    else:
        return "Sujet vide"

# Définition de l'événement de démarrage
@app.on_event("startup")
async def startup():
    # Montage du système de gestion en arrière-plan
    site.mount_app(app)
    # Démarrage du planificateur de tâches
    scheduler.start()


# Définition de la route "/getdata"
@app.get("/getdata")
def getdata(sujet: str=None, annee: int = None, mois: int = None, jour: int = None):
    return data(sujet,annee,mois,jour)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, debug=True)
