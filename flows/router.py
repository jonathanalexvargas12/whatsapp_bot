import json
import logging
from database.connection import DatabaseManager
from database.models import Usuario
from flows.steps import Estado, get_mensaje_estado, validar_dato, obtener_siguiente_estado, obtener_nacionalidad, BIENVENIDA_MSG, RECORDATORIO

logger = logging.getLogger(__name__)

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
            cursor.execute("SELECT estado_actual, datos_contexto FROM sesiones WHERE numero_telefono = %s", (numero_telefono,))
            row = cursor.fetchone()
            if row:
                estado_str = row['estado_actual']
                contexto = json.loads(row['datos_contexto']) if row['datos_contexto'] else {}
                return Estado[estado_str], contexto
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
        # event.Info.MessageSource.Chat.User
        if hasattr(event, 'Info'):
            info = event.Info
            if hasattr(info, 'MessageSource'):
                msg_source = info.MessageSource
                if hasattr(msg_source, 'Chat'):
                    chat = msg_source.Chat
                    user = chat.User if hasattr(chat, 'User') else ""
                    # También puede haber un campo SenderAlt que tiene el número real con @s.whatsapp.net
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
    
    if mensaje_lower == "nuevamente":
        Sesion.eliminar(telefono)
        from database.models import Usuario as UsuarioModel
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE numero_telefono = %s", (telefono,))
            conn.commit()
        except:
            pass
        finally:
            cursor.close()
            conn.close()
        return "Encuesta reiniciada. Escribe 'encuesta' para comenzar." + RECORDATORIO
    
    estado_actual, contexto = Sesion.obtener_estado(telefono)
    print(f"[procesar_mensaje] estado_actual={estado_actual}, contexto={contexto}")
    
    usuario_existe = Usuario.existe(telefono)
    print(f"[procesar_mensaje] usuario_existe={usuario_existe}")
    
    # SIEMPRE permitir repetir para reiniciar la encuesta
    if mensaje_lower == "repetir":
        Sesion.guardar_estado(telefono, Estado.NACIONALIDAD, {})
        return "Bienvenido a nuestro servicio de atención al cliente. Por favor, complete la encuesta:\n\n¿Define su nacionalidad?\n1. Venezolano\n2. Extranjero" + RECORDATORIO
    
    # Si está en INICIO (sin sesión activa)
    if estado_actual == Estado.INICIO:
        if mensaje_lower.strip() == "encuesta":
            Sesion.guardar_estado(telefono, Estado.NACIONALIDAD, {})
            return "Bienvenido a nuestro servicio de atención al cliente. Por favor, complete la encuesta:\n\n¿Define su nacionalidad?\n1. Venezolano\n2. Extranjero" + RECORDATORIO
        return "¡Hola! 👋 Escribe 'encuesta' para comenzar la encuesta." + RECORDATORIO
    
    # Si ya completó la encuesta (estado COMPLETADO)
    if estado_actual == Estado.COMPLETADO:
        return "Ya has completado la encuesta. Usa 'repetir' para volver a empezar o 'nuevamente' para empezar de nuevo."
    
    # Validar y procesar la respuesta según el estado actual
    if not validar_dato(estado_actual, mensaje):
        return get_mensaje_estado(estado_actual) + "\n\n⚠️ Dato inválido. Intente de nuevo."
    
    contexto = contexto or {}
    
    if estado_actual == Estado.NACIONALIDAD:
        contexto['nacionalidad'] = obtener_nacionalidad(mensaje)
    elif estado_actual == Estado.NOMBRE:
        contexto['nombre'] = mensaje.strip()
    elif estado_actual == Estado.APELLIDO:
        contexto['apellido'] = mensaje.strip()
    elif estado_actual == Estado.EDAD:
        contexto['edad'] = int(mensaje.strip())
    elif estado_actual == Estado.DIRECCION:
        contexto['direccion'] = mensaje.strip()
    
    siguiente_estado = obtener_siguiente_estado(estado_actual)
    print(f"[procesar_mensaje] guardando estado: {siguiente_estado}")
    Sesion.guardar_estado(telefono, siguiente_estado, contexto)
    
    if siguiente_estado == Estado.COMPLETADO:
        Usuario.guardar(
            telefono,
            contexto.get('nacionalidad'),
            contexto.get('nombre'),
            contexto.get('apellido'),
            contexto.get('edad'),
            contexto.get('direccion')
        )
        return get_mensaje_estado(Estado.COMPLETADO)
    
    return get_mensaje_estado(siguiente_estado)