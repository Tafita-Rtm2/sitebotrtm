import os
import config
import secrets
import mimetypes
import requests
from dataclasses import dataclass

class Bot:
    def __init__(self, room: str):
        self.__io = config.io
        self.__room = room

        self.prefix = config.PREFIX
        self.commands = config.COMMANDS
        self.developer = config.DEVELOPER

    def __file(self, file_path: str) -> str:
        mime_type, encoding = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type.split('/')[0]
        else:
            return 'invalid'

    def sendMessage(self, datos, reply_to=None) -> dict:
        messageID = f"MSG-{secrets.token_hex(20)}"
        data = {
            "id": messageID,
            "data": {},
            "reply": reply_to
        }
        if type(datos) == str:
            data["data"] = {"body": datos}
        if type(datos) == dict:
            if "body" in datos:
                data["data"]["body"] = datos["body"]
            base = datos["attachment"]
            if type(base) == dict:
                house1 = list()
                house2 = base
                if 'type' not in base:
                    house2['type'] = self.__file(base['src'])
                house1.append(house2)
                data["data"]["attachment"] = house1
            if type(base) == list:
                bahay1 = list()
                for attch in base:
                    bahay2 = attch
                    if 'type' not in attch:
                        bahay2['type'] = self.__file(attch['src'])
                    bahay1.append(bahay2)
                data["data"]["attachment"] = bahay1
            print(data)
        self.__io.emit('sendMessage', data, to=self.__room)
        return {
            "id": messageID,
            "data": datos
        }

    def replyMessage(self, data: dict, id=None) -> None:
        if not id:
            print("ERROR: No message ID provided")
        return self.sendMessage(data, id)

    def unsendMessage(self, messageID):
        self.__io.emit('unsendMessage', {
            "id": messageID
        }, to=self.__room)

    def errorMessage(self, message, id=None):
        self.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] {message}", reply_to=id)

@dataclass
class Data:
    cmd: str
    pretty_args: str
    args: str
    messageId: str
    reply_to: dict
    prefix: str = config.PREFIX
    developer: str = config.DEVELOPER

def chatgpt4_response(question):
    api_url = "https://kaiz-apis.gleeze.com/api/gpt-4o"
    params = {"q": question, "uid": 1}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json().get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        return f"An error occurred: {str(e)}"

def messageHandler(datos, roam):
    bot = Bot(roam)
    txt = datos['text']

    # Si le message commence par un préfixe
    if txt.startswith(config.PREFIX):
        if len(txt) == 1:
            return

        text = txt[1:].split(' ', 1)
        cmd = text[0]
        pretty_args = text[1] if len(text) > 1 else ''
        args = " ".join(pretty_args.split()) if pretty_args else ''
        if cmd.lower() not in config.COMMANDS:
            return bot.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] Command '{cmd.lower()}' not found.")

        function = config.COMMANDS[cmd.lower()]["def"]
        data = Data(
            cmd=cmd.lower(),
            pretty_args=pretty_args,
            args=args,
            messageId=datos["id"],
            reply_to=datos['reply_to'] if datos['reply_to'] else {}
        )
        function(bot, data)
    else:
        # Si le message n'a pas de préfixe, répondre automatiquement avec ChatGPT-4
        bot.sendMessage(":icon[fa-solid fa-circle-notch fa-spin] Thinking, please wait...")
        response = chatgpt4_response(txt)
        bot.sendMessage(response, datos["id"])
