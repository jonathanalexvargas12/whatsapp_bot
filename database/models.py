import mysql.connector
from database.connection import DatabaseManager

class Historial:
    @staticmethod
    def crear_tabla():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numero_telefono VARCHAR(20),
                    nombre_apellido VARCHAR(200),
                    cedula VARCHAR(8),
                    comuna VARCHAR(100),
                    parroquia VARCHAR(100),
                    correo VARCHAR(150),
                    telefono VARCHAR(20),
                    creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Tabla 'historial' creada o ya existe.")
        except mysql.connector.Error as err:
            print(f"❌ Error al crear tabla historial: {err}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def guardar(numero_telefono, nombre_apellido, cedula, comuna, parroquia, correo, telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO historial (numero_telefono, nombre_apellido, cedula, comuna, parroquia, correo, telefono)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (numero_telefono, nombre_apellido, cedula, comuna, parroquia, correo, telefono))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error al guardar en historial: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM historial WHERE numero_telefono = %s ORDER BY creado_el DESC", (numero_telefono,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"❌ Error al obtener historial: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM historial WHERE numero_telefono = %s LIMIT 1", (numero_telefono,))
            return cursor.fetchone() is not None
        except mysql.connector.Error as err:
            print(f"❌ Error al verificar historial: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
