
from clases.conector import Conector

class Usuarios:
    def __init__(self):
        self.db = Conector()

    def validar_usuario(self, username, clave):
        sql = "SELECT * FROM usuarios WHERE username = %s AND clave = %s"
        values = (username, clave) 
        resultado = self.db.select(sql, values)
        return resultado[0] if resultado else None

    def registrar_usuario(self, nombre, apellido, email, username, clave, rol):
        sql = "INSERT INTO usuarios (nombre, apellido, email, username, clave, rol) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (nombre, apellido, email, username, clave, rol)
        return self.db.execute_query(sql, values)