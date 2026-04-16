import mysql.connector
from database.connection import DatabaseManager

class Usuario:
    @staticmethod
    def crear_tabla():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    numero_telefono VARCHAR(20) PRIMARY KEY,
                    nacionalidad VARCHAR(20),
                    nombre VARCHAR(100),
                    apellido VARCHAR(100),
                    edad INT,
                    direccion VARCHAR(255),
                    encuesta_completada BOOLEAN DEFAULT FALSE,
                    creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actualizado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Tabla 'usuarios' creada o ya existe.")
        except mysql.connector.Error as err:
            print(f"❌ Error al crear tabla usuarios: {err}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def guardar(numero_telefono, nacionalidad, nombre, apellido, edad, direccion):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (numero_telefono, nacionalidad, nombre, apellido, edad, direccion, encuesta_completada)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                ON DUPLICATE KEY UPDATE
                    nacionalidad = VALUES(nacionalidad),
                    nombre = VALUES(nombre),
                    apellido = VALUES(apellido),
                    edad = VALUES(edad),
                    direccion = VALUES(direccion),
                    encuesta_completada = TRUE
            """, (numero_telefono, nacionalidad, nombre, apellido, edad, direccion))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error al guardar usuario: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE numero_telefono = %s", (numero_telefono,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"❌ Error al obtener usuario: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM usuarios WHERE numero_telefono = %s AND encuesta_completada = TRUE", (numero_telefono,))
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"❌ Error al verificar usuario: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

class MensajeProcesado:
    @staticmethod
    def crear_tabla():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes_procesados (
                    mensaje_id VARCHAR(100) PRIMARY KEY,
                    numero_telefono VARCHAR(20),
                    procesado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Tabla 'mensajes_procesados' creada o ya existe.")
        except mysql.connector.Error as err:
            print(f"❌ Error al crear tabla mensajes_procesados: {err}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def ya_procesado(mensaje_id):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM mensajes_procesados WHERE mensaje_id = %s", (mensaje_id,))
            return cursor.fetchone() is not None
        except mysql.connector.Error as err:
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def marcar_procesado(mensaje_id, numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT IGNORE INTO mensajes_procesados (mensaje_id, numero_telefono)
                VALUES (%s, %s)
            """, (mensaje_id, numero_telefono))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"❌ Error al marcar mensaje: {err}")
        finally:
            cursor.close()
            conn.close()