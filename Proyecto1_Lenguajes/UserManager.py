import json
import re

class User:
    def __init__(self, email, password, partner):
        self.email = email
        self.password = password
        self.partner = partner  # Este campo puede ser "admin" o "visor"

    def __repr__(self):
        return f"User(email={self.email}, partner={self.partner})"


class UserManager:
    def __init__(self, file_name="usuarios.json"):
        self.file_name = file_name
        self.users = self.load_users()

    def load_users(self):
        """ Cargar usuarios desde el archivo JSON """
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
                users = [User(u["email"], u["password"], u["partner"]) for u in data["users"]]
                return users
        except FileNotFoundError:
            return []

    def save_users(self):
        """ Guardar los usuarios en el archivo JSON """
        data = {"users": [{"email": u.email, "password": u.password, "partner": u.partner} for u in self.users]}
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def add_user(self, email, password, partner):
        """ Agregar un nuevo usuario """
        new_user = User(email, password, partner)
        self.users.append(new_user)
        self.save_users()

    def verify_user(self, email, password):
        """ Verificar si el usuario existe y si la contraseña es correcta """
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None
