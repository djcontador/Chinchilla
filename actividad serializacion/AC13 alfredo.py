from datetime import datetime
from os import listdir, makedirs
import json
import pickle


class Usuario:
    def __init__(self, phone_number, name, contacts):
        self.phone = phone_number
        self.name = name
        self.contacts = contacts

    def __repr__(self):
        return "{} - {} - {}".format(self.phone, self.name, self.contacts)


class Mensaje:
    def __init__(self, _id, last_view_date, date, content, send_to, send_by):
        self.last_view_date = last_view_date
        self.date = date
        self.content = content
        self.send_to = send_to
        self.send_by = send_by
        self.id = _id

    def __getstate__(self):
        new = self.__dict__.copy()
        new.update({"content": self.encode()})
        del new["id"]
        return new

    def __setstate__(self, state):
        state.update({"last_view_date": datetime.now()})
        self.__dict__ = state

    def encode(self):
        n = self.send_by
        content = self.content
        new = ""
        for letra in content:
            if letra != " ":
                aux = ord(letra) - 97  # a es 97 en ascii
                aux = (aux + n) % 26
                new += chr(aux + 97)
            else:
                new += " "
        return new


def decode_users(folder="db/usr"):
    users = []
    for user in listdir(folder):
        with open("{}/{}".format(folder, user)) as user_file:
            _user = json.load(user_file,
                              object_hook=lambda json_obj: Usuario(**json_obj))
        users.append(_user)
    return users


def decode_msgs(folder="db/msg"):
    messages = []
    for msg in listdir(folder):
        with open("{}/{}".format(folder, msg)) as message_file:
            _msg = json.load(message_file,
                             object_hook=lambda json_obj: Mensaje(msg,
                                                                  **json_obj))
        messages.append(_msg)
    return messages


def fill_contacts(users, messages):
    _users = {usuario.phone: usuario for usuario in users}
    for mensaje in messages:
        _users[mensaje.send_by].contacts.append(mensaje.send_to)
    for user in users:
        user.contacts = list(set(user.contacts))


def create_secure_folders(secure_db_directory="secure_db"):
    if secure_db_directory not in listdir():
        makedirs(secure_db_directory)
        makedirs("{}/msg".format(secure_db_directory))
        makedirs("{}/usr".format(secure_db_directory))
    if "msg" not in listdir(secure_db_directory):
        makedirs("{}/msg".format(secure_db_directory))
    if "usr" not in listdir(secure_db_directory):
        makedirs("{}/usr".format(secure_db_directory))


def save_users(users, folder="secure_db/usr", ):
    for user in users:
        pth = "{}/{}.json".format(folder, user.phone)
        with open(pth, "w") as _fp:
            json.dump(user.__dict__, _fp)


def save_messages(messages, folder="secure_db/msg"):
    for message in messages:
        with open("{}/{}".format(folder, message.id), "wb") as file:
            pickle.dump(message, file)


# Esto no se pide, pero lo dejo para poder chequear la deserealizacion y
# facilitar correccion
def deserializar_mensajes(folder="secure_db/msg"):
    msgs = []
    for msg in listdir(folder):
        with open("{}/{}".format(folder, msg), "rb") as message_file:
            if not msg == ".DS_Store":
                _msg = pickle.load(message_file)
                msgs.append(_msg)
    return msgs


if __name__ == "__main__":

    # --- Serializacion ---

    usuarios = decode_users()
    mensajes = decode_msgs()
    fill_contacts(usuarios, mensajes)

    # --- Encriptación ---

    # Creamos, en caso que no existan, las carpetas para secure_db
    create_secure_folders()
    save_users(usuarios)
    save_messages(mensajes)

    # No se pide, pero lo dejo igual:
    mensajes_deserializados = deserializar_mensajes()
    if len(mensajes_deserializados) > 0:
        print(mensajes_deserializados[0].last_view_date)
    print(deserializar_mensajes())
