import os
import sys
import time
import random
import logging
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, LoggedOutEv, event
from neonize.utils import build_jid
from dotenv import load_dotenv

from database.connection import DatabaseManager
from database.models import Historial
from flows.router import Sesion, procesar_mensaje, obtener_telefono
from flows.steps import BIENVENIDA_MSG
from security import verificar, generar, reparar, verificar_integridad

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = NewClient(name="whatsapp_bot")

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    print(f"✅ Conectado a WhatsApp")

@client.event(LoggedOutEv)
def on_logged_out(client: NewClient, event: LoggedOutEv):
    print("⚠️ Sesión cerrada. Escaneá el nuevo QR code para conectar.")

def obtener_chat_jid(event):
    try:
        if hasattr(event, 'Info'):
            info = event.Info
            if hasattr(info, 'MessageSource'):
                msg_source = info.MessageSource

                if hasattr(msg_source, 'SenderAlt') and msg_source.SenderAlt:
                    sender_alt = msg_source.SenderAlt
                    if hasattr(sender_alt, 'User') and sender_alt.User:
                        numero = sender_alt.User
                        print(f"Chat JID obtenido (SenderAlt): {numero}")
                        return numero

                if hasattr(msg_source, 'Chat'):
                    chat = msg_source.Chat
                    if hasattr(chat, 'User') and chat.User:
                        user = chat.User
                        server = chat.Server if hasattr(chat, 'Server') else "s.whatsapp.net"
                        if user:
                            jid = f"{user}@{server}"
                            print(f"Chat JID obtenido (Chat): {jid}")
                            return jid
    except Exception as e:
        print(f"Error obteniendo chat_jid: {e}")
        import traceback
        traceback.print_exc()
    return None

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    try:
        logger.debug(f"Evento recibido: {event}")

        mensaje = None
        if hasattr(event.Message, 'conversation') and event.Message.conversation:
            mensaje = event.Message.conversation
        elif hasattr(event.Message, 'extendedTextMessage'):
            ext_msg = event.Message.extendedTextMessage
            if ext_msg and hasattr(ext_msg, 'text'):
                mensaje = ext_msg.text

        if not mensaje:
            logger.debug("Mensaje vacío o no texto, ignorado")
            return

        mensaje = str(mensaje)
        telefono = obtener_telefono(event)
        print(f"==> Mensaje de: {telefono}: {mensaje}")

        respuesta = procesar_mensaje(telefono, mensaje)
        print(f"==> Respuesta generada: {respuesta[:100] if respuesta else None}...")

        if respuesta:
            chat_jid = obtener_chat_jid(event)
            print(f"--- chat_jid: {chat_jid} ---")

            if chat_jid:
                if '@' not in str(chat_jid):
                    numero = str(chat_jid)
                else:
                    numero = str(chat_jid).split('@')[0]

                print(f"==> Enviando a numero: {numero}")

                jid_para_enviar = build_jid(numero)
                print(f"==> JID formateado: {jid_para_enviar}")

                demora = random.uniform(1.5, 5.0)
                print(f"⏳ Esperando {demora:.1f}s antes de responder...")
                time.sleep(demora)

                result = client.send_message(jid_para_enviar, respuesta)
                print(f"==> Resultado del send_message: {result}")
                print(f"==> Respuesta enviada a {telefono}")
            else:
                logger.error("No se pudo obtener chat_jid")

    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        logger.error(f"Tipo de error: {type(e).__name__}")
        import traceback
        logger.error(traceback.format_exc())

def inicializar_base_datos():
    print("🔄 Inicializando base de datos...")
    DatabaseManager.get_pool()
    Sesion.crear_tabla()
    Historial.crear_tabla()
    print("✅ Tablas creadas/verificadas.")

def main():
    print("🔒 Verificando integridad del sistema...")
    if not verificar_integridad():
        sys.exit(1)

    print("🤖 Iniciando Bot de WhatsApp...")
    inicializar_base_datos()

    print("📱 Conectando al servidor de WhatsApp...")
    client.connect()

    print("✅ Bot listo. Esperando mensajes...")
    event.wait()

if __name__ == "__main__":
    if "--credencial" in sys.argv:
        if len(sys.argv) > 2 and sys.argv[2] == "generar":
            generar()
        else:
            verificar()
    elif "--reparar" in sys.argv:
        reparar()
    else:
        main()