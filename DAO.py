from connection import * 

class Datos:
    def __init__(self, personaje, raza, habilidad, equipamiento, id=None):
        self.id = id
        self.personaje = personaje
        self.raza = raza
        self.habilidad = habilidad
        self.equipamiento = equipamiento

class PersonajeDAO:
    def __init__(self):
        self.db = DataBase()

    def ingreso(self, Datos):
        sql = "INSERT INTO datos (personaje, raza, habilidad, equipamiento) VALUES (%s, %s, %s, %s)"
        values = (Datos.personaje,Datos.raza,Datos.habilidad,Datos.equipamiento)
        self.db.cursor.execute(sql, values)
        self.db.connection.commit()

    def llenado(self):
        sql = "SELECT * FROM datos"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()


    def actualizar_personaje(self, id, personaje, raza, habilidad, equipamiento):
        sql = "UPDATE datos SET personaje=%s, raza=%s, habilidad=%s, equipamiento=%s WHERE id=%s"
        values = (personaje, raza, habilidad, equipamiento, id)
        self.db.cursor.execute(sql, values)
        self.db.connection.commit()

    def borrar_personaje(self, id):
        sql = "DELETE FROM datos WHERE id=%s"
        self.db.cursor.execute(sql, (id,))
        self.db.connection.commit()

    def buscar_personaje(self, nombre):
        sql = "SELECT * FROM datos WHERE personaje = %s"
        self.db.cursor.execute(sql, (nombre,))
        return self.db.cursor.fetchall()
    
class UsuarioDAO:
    def __init__(self):
        self.db = DataBase()

    def registrar_usuario(self, usuario, contraseña):
        sql = "SELECT * FROM log WHERE usuario = %s"
        self.db.cursor.execute(sql, (usuario,))
        usuario_existente = self.db.cursor.fetchone()

        if usuario_existente:
            return False
        else:
            sql = "INSERT INTO log (usuario, contraseña) VALUES (%s, %s)"
            self.db.cursor.execute(sql, (usuario, contraseña))
            self.db.connection.commit()
            return True

    def login_usuario(self, usuario, contraseña):
        sql = "SELECT * FROM log WHERE usuario = %s AND contraseña = %s"
        self.db.cursor.execute(sql, (usuario, contraseña))
        usuario = self.db.cursor.fetchone()

        if usuario:
            return True
        else:
            return False