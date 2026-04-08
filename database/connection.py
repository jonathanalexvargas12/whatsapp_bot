import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="wa_bot_pool",
                    pool_size=5,
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS"),
                    port=os.getenv("DB_PORT")
                )
                print("✅ Pool de conexiones MariaDB creado.")
                
                # --- NUEVA SECCIÓN DE INSPECCIÓN ---
                cls._inspect_database()
                # ------------------------------------
                
            except mysql.connector.Error as err:
                print(f"❌ Error al crear el pool: {err}")
        return cls._pool

    @classmethod
    def _inspect_database(cls):
        """Muestra las tablas encontradas en la base de datos actual."""
        conn = cls._pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📊 Tablas encontradas en '{os.getenv('DB_NAME')}':")
                for (table_name,) in tables:
                    print(f"   - {table_name}")
            else:
                print(f"⚠️ La base de datos '{os.getenv('DB_NAME')}' está vacía.")
        except mysql.connector.Error as err:
            print(f"❌ Error al inspeccionar tablas: {err}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_connection(cls):
        return cls.get_pool().get_connection()