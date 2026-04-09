# 🤖 Bot de WhatsApp - Automatizado

Un bot de WhatsApp automatizado con flujo conversacional basado en una máquina de estados finitos (FSM) y persistencia de datos en MariaDB.

## 📋 Características

- **Conexión a WhatsApp** mediante Neonize (wrapper de Python para whatsmeow en Go)
- **Máquina de Estados Finitos (FSM)** para manejar el flujo conversacional
- **Persistencia en MariaDB** para almacenar sesiones y datos de usuarios
- **Encuesta automatizada** que captura: nacionalidad, nombre, apellido, edad y dirección
- **Comandos de control**: `/repetir` y `/reiniciar`

## 🛠️ Tecnologías

- **Python** 3.10+
- **Neonize** - Cliente de WhatsApp
- **MariaDB** - Base de datos
- **python-dotenv** - Variables de entorno

## 📁 Estructura del Proyecto

```
whatsapp_bot/
├── credentials/           # Almacena el archivo .db de la sesión
├── database/
│   ├── connection.py     # Pool de conexiones a MariaDB
│   └── models.py         # Modelos de datos (Usuario)
├── flows/
│   ├── router.py         # Lógica de enrutamiento FSM
│   └── steps.py          # Definición de estados y pasos
├── .env                  # Variables de entorno
├── main.py               # Punto de entrada
└── requirements.txt      # Dependencias
```

## 🚀 Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <repositorio>
   cd whatsapp_bot
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**

   Edita el archivo `.env` con tu configuración:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=whatsapp_bot
   DB_USER=root
   DB_PASSWORD=tu_password
   ```

5. **Inicia MariaDB y crea la base de datos:**
   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS whatsapp_bot;"
   ```

## ▶️ Uso

Ejecuta el bot:
```bash
python main.py
```

El bot mostrará un código QR que debes escanear con tu WhatsApp para vincular el dispositivo.

### Flujo de la Encuesta

1. El usuario escribe `encuesta` para comenzar
2. Responde: Nacionalidad (1: Venezolano, 2: Extranjero)
3. Ingresa: Nombre
4. Ingresa: Apellido
5. Ingresa: Edad (solo números)
6. Ingresa: Dirección
7. Al completar, los datos se guardan en la base de datos

### Comandos

- `encuesta` - Iniciar la encuesta
- `/repetir` - Reiniciar la encuesta sin borrar datos
- `/reiniciar` - Reiniciar completamente (borra sesión y datos)

## 📊 Base de Datos

### Tabla: `usuarios`
Almacena los datos de los usuarios que completan la encuesta.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| numero_telefono | VARCHAR(20) | Clave primaria |
| nacionalidad | VARCHAR(20) | Venezolano/Extranjero |
| nombre | VARCHAR(100) | Nombre del usuario |
| apellido | VARCHAR(100) | Apellido del usuario |
| edad | INT | Edad del usuario |
| direccion | VARCHAR(255) | Dirección del usuario |
| encuesta_completada | BOOLEAN | Estado de la encuesta |
| creado_el | TIMESTAMP | Fecha de creación |
| actualizado_el | TIMESTAMP | Última actualización |

### Tabla: `sesiones`
Almacena el estado actual de cada conversación.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| numero_telefono | VARCHAR(20) | Clave primaria |
| estado_actual | VARCHAR(50) | Estado FSM actual |
| datos_contexto | JSON | Datos recopilados |
| actualizado_el | TIMESTAMP | Última actualización |

## 🐛 Solución de Problemas

Si el bot no responde:
1. Verifica que MariaDB esté corriendo
2. Revisa que el archivo `.env` esté configurado correctamente
3. Asegúrate de haber escaneado el código QR
4. Verifica los logs en la consola

## 📝 Licencia

Este proyecto es de uso EULA (presto para su uso libre pero no su distribucion, de no cumplir dicha regla, puede enfrentarse a cargos legales).

---

**Creador:** Jonathan Alexander Vargas