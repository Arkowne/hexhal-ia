<?php
function ajouter_message($texte) {
    // Charger le fichier JSON
    $conversation = json_decode(file_get_contents('conversation.json'), true);
    
    // Ajouter le nouveau message de l'utilisateur
    $nouveau_message_utilisateur = array("role" => "user", "content" => $texte);
    $conversation["messages"][] = $nouveau_message_utilisateur;
    
    // Écrire le fichier JSON mis à jour (avec le nouveau message utilisateur)
    file_put_contents('conversation.json', json_encode($conversation, JSON_PRETTY_PRINT));
    
    // Faire la requête CURL
    $url = 'http://localhost:11434/api/chat';
    $headers = array(
        'Content-Type: application/json'
    );
    $data = file_get_contents('conversation.json');
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    // Vérifier la réponse de la requête
    if ($http_code == 200) {
        // Imprimer la réponse de la requête pour voir sa structure
        echo "Réponse de la requête CURL :\n";
        echo $response;
        
        // Extraire la réponse JSON de la requête
        $reponse_json = json_decode($response, true);
        
        // Ajouter la réponse de l'assistant au fichier JSON
        // Extraire le contenu du message de l'assistant
        $contenu_message_assistant = array("role" => "assistant", "content" => $reponse_json["message"]);
        
        // Ajouter le message de l'assistant à la conversation
        $conversation["messages"][] = $contenu_message_assistant;
        
        // Écrire le fichier JSON mis à jour (avec la réponse de l'assistant)
        file_put_contents('conversation.json', json_encode($conversation, JSON_PRETTY_PRINT));
        
        echo "Réponse ajoutée au fichier JSON avec succès !\n";
    } else {
        echo "Erreur lors de l'envoi de la requête : $http_code\n";
    }

    return $response;
}

// Exemple d'utilisation
// $texte_recu = readline("Entrez le texte reçu : ");
// ajouter_message($texte_recu);
?>
