import requests

def chatbot(bot, data):
    if not data.args:  # Vérifie si une question a été posée
        return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Vous devez poser une question après la commande.")

    user_question = " ".join(data.args)  # La question posée par l'utilisateur
    api_url = "https://kaiz-apis.gleeze.com/api/gpt-4o"
    params = {
        "q": user_question,  # La question utilisateur envoyée à l'API
        "uid": 1  # Identifiant utilisateur si nécessaire
    }

    # Envoi de la requête à l'API
    try:
        loading = bot.sendMessage(":icon[fa-solid fa-circle-notch fa-spin] Je réfléchis, veuillez patienter...")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()
        bot.unsendMessage(loading['id'])

        if "response" not in data:
            return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Une erreur s'est produite. Aucune réponse trouvée.")

        # Construction de la réponse
        message = ":bold[:icon[fa-solid fa-robot] Réponse du Chatbot]\n"
        message += data["response"]  # La réponse de l'API
        bot.sendMessage(message, data.messageId)

    except Exception as e:
        bot.unsendMessage(loading['id'])
        return bot.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] Une erreur est survenue : {str(e)}", data.messageId)

config = {
    "name": 'chatbot',
    "credits": "Greegmon",
    "description": "Répond à vos questions grâce à une API de chatbot",
    "def": chatbot
}
