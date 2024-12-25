import requests

def chatbot(bot, data):
    # Vérifie si une question est fournie
    if not data.args:
        return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Please provide a question for the chatbot.")
    
    user_question = " ".join(data.args)  # Combine les arguments en une seule question
    api_url = "https://kaiz-apis.gleeze.com/api/gpt-4o"
    params = {
        "q": user_question,  # La question de l'utilisateur
        "uid": 1  # Identifiant utilisateur
    }

    # Envoi d'un message temporaire pour indiquer que le bot réfléchit
    loading = bot.sendMessage(":icon[fa-solid fa-circle-notch fa-spin] Thinking, please wait...")

    try:
        # Requête à l'API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        api_data = response.json()

        # Vérifie si la réponse de l'API contient le champ attendu
        if "response" not in api_data:
            bot.unsendMessage(loading['id'])
            return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] The API did not return a valid response.")

        # Construction de la réponse à partir des données de l'API
        message = f":bold[:icon[fa-solid fa-robot] Chatbot Response]:\n{api_data['response']}"
        bot.unsendMessage(loading['id'])
        bot.sendMessage(message, data.messageId)

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
