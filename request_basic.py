import json
import requests
import gradio as gr

def ajouter_message(texte):
    # Charger le fichier JSON
    with open('conversation.json', 'r') as f:
        conversation = json.load(f)
    
    # Ajouter le nouveau message de l'utilisateur
    nouveau_message_utilisateur = {"role": "user", "content": texte}
    conversation["messages"].append(nouveau_message_utilisateur)
    
    # Écrire le fichier JSON mis à jour (avec le nouveau message utilisateur)
    with open('conversation.json', 'w') as f:
        json.dump(conversation, f, indent=2)
    
    # Faire la requête CURL
    url = 'http://localhost:11434/api/chat'
    headers = {'Content-Type': 'application/json'}
    with open('conversation.json', 'r') as f:
        data = f.read()
    response = requests.post(url, data=data, headers=headers)
    
    # Vérifier la réponse de la requête
    if response.status_code == 200:
        # Imprimer la réponse de la requête pour voir sa structure
        print("Réponse de la requête CURL :")
        print(response.text)
        
        # Extraire la réponse JSON de la requête
        reponse_json = response.json()
        
        # Ajouter la réponse de l'assistant au fichier JSON
        # Modifier cette partie en fonction de la structure de la réponse JSON
        # Assurez-vous de remplacer 'reponse_json["response"]' par la clé correcte contenant le contenu souhaité
        # Extraire le contenu du message de l'assistant
        contenu_message_assistant = reponse_json["message"]
        
        # Créer un message pour l'assistant dans le format JSON
        #nouveau_message_assistant = {contenu_message_assistant}
        conversation["messages"].append(contenu_message_assistant)
        
        # Écrire le fichier JSON mis à jour (avec la réponse de l'assistant)
        with open('conversation.json', 'w') as f:
            json.dump(conversation, f, indent=2)
        
        print("Réponse ajoutée au fichier JSON avec succès !")
    else:
        print("Erreur lors de l'envoi de la requête :", response.status_code)

    return response.text

# Exemple d'utilisation
#texte_recu = input("Entrez le texte reçu : ")
#ajouter_message(texte_recu)

iface = gr.Interface(fn=ajouter_message,
                     inputs=[gr.Textbox(label="Question")],
                     outputs="text",
                     title="Document Query",
                     description="Ask Something")
iface.launch()
