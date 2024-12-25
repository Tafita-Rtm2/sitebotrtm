import requests

def chatbot(bot, data):
    # Vérifie si l'utilisateur a posé une question
    if not data.args:
        return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Please provide a question for the chatbot.")

    user_question = " ".join(data.args)  # Combine les arguments en une seule question
    api_url = "https://kaiz-apis.gleeze.com/api/gpt-4o"
    params = {
        "q": user_question,  # La question de l'utilisateur
        "uid": 1  # Identifiant utilisateur, si nécessaire
    }

    # Indique que le bot réfléchit
    loading = bot.sendMessage(":icon[fa-solid fa-circle-notch fa-spin] Thinking, please wait...")

    try:
        # Requête à l'API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()

        # Vérifie si la réponse contient un champ valide
        if "response" not in data:
            bot.unsendMessage(loading['id'])
            return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] The API did not return a valid response.")

        # Crée le message de réponse
        message = {
            "body": f":bold[:icon[fa-solid fa-robot] Chatbot Response]:\n{data['response']}"
        }
        bot.unsendMessage(loading['id'])
        bot.sendMessage(message)

    except Exception as e:
        # Gère les erreurs API ou autres
        bot.unsendMessage(loading['id'])
        return bot.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] An error occurred: {str(e)}")

# Configuration de la commande
config = {
    "name": 'chatbot',
    "def": chatbot,
    "usage": "{p}chatbot <question>",
    "description": "Answers user questions via an AI-powered chatbot API",
    "credits": 'Greegmon'
}
