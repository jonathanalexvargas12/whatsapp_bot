import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "wa_bot_db")

class DatabaseManager:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            cls._pool = cls._crear_pool()
        return cls._pool

    @classmethod
    def _crear_pool(cls):
        try:
            pool = pooling.MySQLConnectionPool(
                pool_name="wa_bot_pool",
                pool_size=5,
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            print(f"✅ Pool de conexiones MariaDB creado.")
            cls._inspect_database(pool)
            return pool
        except mysql.connector.Error as err:
            if err.errno == 1049:
                print(f"⚠️  La base de datos '{DB_NAME}' no existe. Creándola...")
                cls._crear_base_datos()
                pool = pooling.MySQLConnectionPool(
                    pool_name="wa_bot_pool",
                    pool_size=5,
                    host=DB_HOST,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    port=DB_PORT
                )
                print(f"✅ Base de datos '{DB_NAME}' creada exitosamente.")
                print(f"📦 Tablas disponibles:")
                cls._inspect_database(pool)
                return pool
            print(f"❌ Error al crear el pool: {err}")
            return None

    @classmethod
    def _crear_base_datos(cls):
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def _inspect_database(cls, pool=None):
        if pool is None:
            pool = cls._pool
        if pool is None:
            return
        conn = pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                for (table_name,) in tables:
                    print(f"   📄 {table_name}")
            else:
                print("   (vacía — se crearán al iniciar el bot)")
        except mysql.connector.Error as err:
            print(f"❌ Error al inspeccionar tablas: {err}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_connection(cls):
        pool = cls.get_pool()
        if pool is None:
            return None
        return pool.get_connection()
