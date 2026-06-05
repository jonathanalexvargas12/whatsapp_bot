import json
import logging
from datetime import datetime, timedelta
from database.connection import DatabaseManager
from database.models import Historial
from flows.steps import Estado, get_mensaje_estado, validar_dato, obtener_siguiente_estado

logger = logging.getLogger(__name__)
TIEMPO_EXPIRACION = timedelta(minutes=30)

class Sesion:
    @staticmethod
    def crear_tabla():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sesiones (
                    numero_telefono VARCHAR(20) PRIMARY KEY,
                    estado_actual VARCHAR(50) DEFAULT 'INICIO',
                    datos_contexto JSON,
                    actualizado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Tabla 'sesiones' creada o ya existe.")
        except Exception as err:
            print(f"❌ Error al crear tabla sesiones: {err}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_estado(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT estado_actual, datos_contexto, actualizado_el FROM sesiones WHERE numero_telefono = %s", (numero_telefono,))
            row = cursor.fetchone()
            if row:
                estado_str = row['estado_actual']
                estado = Estado[estado_str]
                if estado not in (Estado.INICIO, Estado.COMPLETADO):
                    ahora = datetime.now()
                    ultima_act = row['actualizado_el']
                    if isinstance(ultima_act, datetime) and (ahora - ultima_act) > TIEMPO_EXPIRACION:
                        print(f"⏰ Sesión expirada para {numero_telefono}, reiniciando...")
                        Sesion.eliminar(numero_telefono)
                        return Estado.INICIO, {}
                contexto = json.loads(row['datos_contexto']) if row['datos_contexto'] else {}
                return estado, contexto
            return Estado.INICIO, {}
        except Exception as err:
            print(f"❌ Error al obtener estado: {err}")
            return Estado.INICIO, {}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def guardar_estado(numero_telefono, estado, contexto=None):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO sesiones (numero_telefono, estado_actual, datos_contexto)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    estado_actual = VALUES(estado_actual),
                    datos_contexto = VALUES(datos_contexto)
            """, (numero_telefono, estado.value, json.dumps(contexto) if contexto else None))
            conn.commit()
            return True
        except Exception as err:
            print(f"❌ Error al guardar estado: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reiniciar(numero_telefono):
        return Sesion.guardar_estado(numero_telefono, Estado.INICIO, {})

    @staticmethod
    def eliminar(numero_telefono):
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sesiones WHERE numero_telefono = %s", (numero_telefono,))
            conn.commit()
            return True
        except Exception as err:
            print(f"❌ Error al eliminar sesión: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

def obtener_telefono(event):
    try:
        if hasattr(event, 'Info'):
            info = event.Info
            if hasattr(info, 'MessageSource'):
                msg_source = info.MessageSource
                if hasattr(msg_source, 'Chat'):
                    chat = msg_source.Chat
                    user = chat.User if hasattr(chat, 'User') else ""
                    if hasattr(msg_source, 'SenderAlt') and msg_source.SenderAlt:
                        sender_alt = msg_source.SenderAlt
                        if hasattr(sender_alt, 'User') and sender_alt.User:
                            return sender_alt.User
                    if user:
                        return user
    except Exception as e:
        print(f"Error en obtener_telefono: {e}")
    return ""

def procesar_mensaje(telefono, mensaje):
    mensaje = mensaje.strip()
    mensaje_lower = mensaje.lower()
    print(f"[procesar_mensaje] telefono={telefono}, mensaje={mensaje}")

    estado_actual, contexto = Sesion.obtener_estado(telefono)
    print(f"[procesar_mensaje] estado_actual={estado_actual}, contexto={contexto}")

    usuario_existe = Historial.existe(telefono)
    print(f"[procesar_mensaje] usuario_existe={usuario_existe}")

    if mensaje_lower == "repetir":
        Sesion.guardar_estado(telefono, Estado.NOMBRE_APELLIDO, {})
        return get_mensaje_estado(Estado.NOMBRE_APELLIDO)

    if mensaje_lower == "encuesta":
        Sesion.guardar_estado(telefono, Estado.NOMBRE_APELLIDO, {})
        return get_mensaje_estado(Estado.NOMBRE_APELLIDO)

    if estado_actual == Estado.INICIO:
        return None

    if estado_actual == Estado.COMPLETADO:
        return None

    if not validar_dato(estado_actual, mensaje):
        return get_mensaje_estado(estado_actual) + "\n\n⚠️ *Dato inválido.* Intenta de nuevo."

    contexto = contexto or {}

    if estado_actual == Estado.NOMBRE_APELLIDO:
        contexto['nombre_apellido'] = mensaje.strip()
    elif estado_actual == Estado.CEDULA:
        contexto['cedula'] = mensaje.strip()
    elif estado_actual == Estado.COMUNA:
        contexto['comuna'] = mensaje.strip()
    elif estado_actual == Estado.PARROQUIA:
        contexto['parroquia'] = mensaje.strip()
    elif estado_actual == Estado.CORREO:
        contexto['correo'] = mensaje.strip()
    elif estado_actual == Estado.TELEFONO:
        contexto['telefono'] = mensaje.strip()

    siguiente_estado = obtener_siguiente_estado(estado_actual)
    print(f"[procesar_mensaje] guardando estado: {siguiente_estado}")
    Sesion.guardar_estado(telefono, siguiente_estado, contexto)

    if siguiente_estado == Estado.COMPLETADO:
        Historial.guardar(
            telefono,
            contexto.get('nombre_apellido'),
            contexto.get('cedula'),
            contexto.get('comuna'),
            contexto.get('parroquia'),
            contexto.get('correo'),
            contexto.get('telefono')
        )
        return get_mensaje_estado(Estado.COMPLETADO)

    return get_mensaje_estado(siguiente_estado)