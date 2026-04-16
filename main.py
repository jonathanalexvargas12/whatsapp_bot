import os
import logging
import time
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, LoggedOutEv, event
from neonize.utils import build_jid
from dotenv import load_dotenv

from security import validar_licencia, integrity_check
from database.connection import DatabaseManager
from database.models import Usuario, MensajeProcesado
from flows.router import Sesion, procesar_mensaje, obtener_telefono
from flows.steps import BIENVENIDA_MSG

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = NewClient(name="whatsapp_bot")
conexion_timestamp = None

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    global conexion_timestamp
    conexion_timestamp = time.time()
    print(f"✅ Conectado a WhatsApp (inicio de sincronizacion: {conexion_timestamp})")

@client.event(LoggedOutEv)
def on_logged_out(client: NewClient, event: LoggedOutEv):
    print("⚠️ Sesión cerrada. Escaneá el nuevo QR code para conectar.")

def obtener_chat_jid(event):
    try:
        # Primero intentar obtener el número real del remitente (SenderAlt)
        if hasattr(event, 'Info'):
            info = event.Info
            if hasattr(info, 'MessageSource'):
                msg_source = info.MessageSource
                
                # Usar el número real del usuario (SenderAlt)
                if hasattr(msg_source, 'SenderAlt') and msg_source.SenderAlt:
                    sender_alt = msg_source.SenderAlt
                    if hasattr(sender_alt, 'User') and sender_alt.User:
                        numero = sender_alt.User
                        print(f"Chat JID obtenido (SenderAlt): {numero}")
                        return numero
                
                # Si no hay SenderAlt, usar Chat
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
        
        mensaje_id = None
        is_group = False
        is_broadcast = False
        is_status = False
        chat_server = ""
        
        if hasattr(event, 'Info') and hasattr(event.Info, 'MessageSource'):
            msg_source = event.Info.MessageSource
            if hasattr(msg_source, 'ID') and msg_source.ID:
                mensaje_id = str(msg_source.ID)
            if hasattr(msg_source, 'IsGroup') and msg_source.IsGroup:
                is_group = True
            if hasattr(msg_source, 'IsBroadcast') and msg_source.IsBroadcast:
                is_broadcast = True
            if hasattr(msg_source, 'Chat') and hasattr(msg_source.Chat, 'Server'):
                chat_server = msg_source.Chat.Server
                if chat_server == "broadcast":
                    is_status = True
        
        print(f"==> Mensaje info - ID: {mensaje_id}, IsGroup: {is_group}, IsBroadcast: {is_broadcast}, Server: {chat_server}")
        
        if is_group or is_broadcast or is_status:
            print(f"==> Mensaje de grupo/broadcast/status, ignorando")
            return
        
        # Ignorar mensajes multimedia (imágenes, videos, audio, stickers, documentos)
        if hasattr(event.Message, 'imageMessage') or \
           hasattr(event.Message, 'videoMessage') or \
           hasattr(event.Message, 'audioMessage') or \
           hasattr(event.Message, 'stickerMessage') or \
           hasattr(event.Message, 'documentMessage') or \
           hasattr(event.Message, 'voiceMessage'):
            print("==> Mensaje multimedia detectado, ignorando")
            return
        
        # Ignorar mensajes que llegan muy rapido despues de conectar (sincronizacion)
        if conexion_timestamp:
            tiempo_desde_conexion = time.time() - conexion_timestamp
            if tiempo_desde_conexion < 30:
                print(f"==> Mensaje durante sincronizacion ({tiempo_desde_conexion:.1f}s), ignorando")
                return
        
        if mensaje_id and MensajeProcesado.ya_procesado(mensaje_id):
            print(f"==> Mensaje ya procesado, ignorando: {mensaje_id}")
            return
        
        # Marcar mensaje como procesado inmediatamente al recibirlo (con telefono conocido)
        telefono = obtener_telefono(event)
        if mensaje_id:
            MensajeProcesado.marcar_procesado(mensaje_id, telefono)
        
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
    Usuario.crear_tabla()
    MensajeProcesado.crear_tabla()
    print("✅ Base de datos lista.")

def main():
    print("🤖 Iniciando Bot de WhatsApp...")
    
    print("🔐 Verificando licencia...")
    validar_licencia()
    
    print("🔒 Verificando integridad del código...")
    integrity_check()
    
    inicializar_base_datos()
    
    print("📱 Conectando al servidor de WhatsApp...")
    client.connect()
    
    print("✅ Bot listo. Esperando mensajes...")
    event.wait()

if __name__ == "__main__":
    main()