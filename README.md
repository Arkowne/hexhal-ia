Ce projet est le regroupement de plusieurs morceaux de code dédiés a l'infrastructure de hexhal.ai, cette partie regroupera majoritairement le back-end.
Fonctions:
-avoir une interface permetant de se connecter avec un compte entreprise et d'avoir automatiquement la liste de outes les conversations avec le model de l'entreprise, 
infos stockées dans des fichiers json pour les conversations et informations de connexions dans une base de données Sql externe pour le moment. les infos de connexions a la base sql sont egalement stockées dans un fichiers json, récupéré par les differents progammes php. 
La gestion serveurs se fait avec de un Ollama et son API intégrée pour la partie conversation clasique et de 2 avec gradio (voir pour une migration vers une api custom en python) pour la partie embeding.
Les fichiers d'embeding devront etre stockées sur une page web externe, url qui sera récupérée par embeding.py et interprétée en vecteur par nomic-embed-text, un model ollama d'embeding

A faire:
-géré dynamiquement l'ip du serveur Ollama depuis un fichier society_info.json
-essayer de stocker les vecteurs d'embeding dans un fichier appart, pour reduire le temps de lancement du serveur externe
-Faire l'interface app.hexhal.com
-trouver un hebergeur web qui accepte le python, le sql, le php, le json, le html et le css, ainsi que le javascript
-commencer a lister les differents models et les hebergeurs propices a l'hebergement des differentes instances de serveur
