## Ce projet a pour but de mettre en place un ETL
Pour ce faire j'ai mis en place une architecture basé sur l'extraction ,le stockage et le traitement de données,sans 
outils particulier.
Nous avons dans notre architecture le module d'extraction de données a travers API du New-york-times mise à notre disposition

    
    I-module extraction

1.fonction de requettage celle qui se connecte via une cle sur l'API et recupere les données sur un sujet données
2-fonction de multiprocessing ,elle permettra de faire du parralélisme lors du requettage si on a plusieurs fichier

            II-module de stockage
Nous avons definis une arborescence Database/sujet/annee/mois/jour pour stockage de le données en tenant compte du multiprocessing

III-module main
dans cette partie nous creons un end-point avvec url localhost:8000/ et  lancer un job chaque jour sur cet API 
afin de recolter les données

IV- module connecteur(ODBC)
vue que nous avons une arborescence de stockage assez complexe nous avons mis en place un autre end-point pour recuperer les 
données stocker il nous suffit de specifier le sujet,l'annee,le mois et le jour que l'on desir ou rien (va tous recuperer) via 
une requete http.get

V-module traitement et enrichissement des données
Nous avons utilisés le transformer NLTK.sentiment afin de determiner le sentiment d'un post


DEMARRAGE
1-Installer le fichier requirements
2- faire une git pull
3- acceder au repertoire /stage
-ouvrir le fichier globalParametre pour configurer les sujets de recherche et le chemin de stockage des données
4-executer python3 main.py
    -le serveur fast API se lancera
5-acceder au localhost:8000/admin pour voir la liste des jobs en cours
6-acceder au localhost:8000/docs pour avoir la documentation de l'API
7- controle C pour arreter les service
