<<<<<<< HEAD
# 🤖 Bot de WhatsApp 

**Creador:** Ingeniero Jonathan Alexander Vargas
**Contacto:** contactoconexiatech@gmail.com

---

Bot de WhatsApp automatizado con flujo conversacional basado en una máquina de estados finitos (FSM). Persiste reportes en MariaDB y permite a proveedores enviar reportes periódicos (diarios, semanales, etc.) de forma sencilla.

---
=======
# 🤖 Bot de WhatsApp - Automatizado

Un bot de WhatsApp automatizado con flujo conversacional basado en una máquina de estados finitos (FSM) y persistencia de datos en MariaDB.
>>>>>>> 3ea514dd5db3340e63003e713ee6a3f78f3ceec6

## 📋 Características

- **Conexión a WhatsApp** mediante Neonize (wrapper de Python para whatsmeow en Go)
- **Máquina de Estados Finitos (FSM)** para manejar el flujo conversacional
<<<<<<< HEAD
- **Persistencia en MariaDB** con dos tablas: `sesiones` (estado transitorio) e `historial` (reportes completados)
- **Reportes periódicos**: cada envío se guarda como un registro independiente, sin sobrescribir anteriores
- **Demora realista** entre respuestas para evitar detección de spam
- **Creación automática** de la base de datos al iniciar si no existe
=======
- **Persistencia en MariaDB** para almacenar sesiones y datos de usuarios
- **Encuesta automatizada** que captura: nacionalidad, nombre, apellido, edad y dirección
- **Comandos de control**: `/repetir` y `/reiniciar`
>>>>>>> 3ea514dd5db3340e63003e713ee6a3f78f3ceec6

## 🛠️ Tecnologías

- **Python** 3.10+
- **Neonize** - Cliente de WhatsApp
- **MariaDB** - Base de datos
- **python-dotenv** - Variables de entorno

## 📁 Estructura del Proyecto

```
whatsapp_bot/
<<<<<<< HEAD
├── credentials/           # Almacena la sesión de WhatsApp
├── database/
│   ├── connection.py     # Pool de conexiones a MariaDB
│   └── models.py         # Modelos: Historial (reportes completados)
├── flows/
│   ├── router.py         # Lógica de enrutamiento FSM
│   └── steps.py          # Definición de estados y pasos
├── security.py           # Validación de integridad del proyecto
├── .env                  # Configuración de base de datos
=======
├── credentials/           # Almacena el archivo .db de la sesión
├── database/
│   ├── connection.py     # Pool de conexiones a MariaDB
│   └── models.py         # Modelos de datos (Usuario)
├── flows/
│   ├── router.py         # Lógica de enrutamiento FSM
│   └── steps.py          # Definición de estados y pasos
├── .env                  # Variables de entorno
>>>>>>> 3ea514dd5db3340e63003e713ee6a3f78f3ceec6
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
<<<<<<< HEAD
   DB_NAME=wa_bot_db
   DB_USER=tu_usuario
   DB_PASS=tu_password
=======
   DB_NAME=whatsapp_bot
   DB_USER=root
   DB_PASSWORD=tu_password
   ```

5. **Inicia MariaDB y crea la base de datos:**
   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS whatsapp_bot;"
>>>>>>> 3ea514dd5db3340e63003e713ee6a3f78f3ceec6
   ```

## ▶️ Uso

Ejecuta el bot:
```bash
python main.py
```

El bot mostrará un código QR que debes escanear con tu WhatsApp para vincular el dispositivo.

<<<<<<< HEAD
Si la base de datos no existe, el bot la crea automáticamente al iniciar usando las credenciales del `.env`.

---

## 💬 Comandos

| Comando | ¿Desde dónde funciona? | Qué hace |
|---|---|---|
| `encuesta` | Cualquier estado | Inicia un nuevo reporte desde cero |
| `repetir` | Cualquier estado | Reinicia la encuesta actual (útil si te equivocaste a mitad de preguntas) |

Tanto `encuesta` como `repetir` se reconocen en cualquier combinación de mayúsculas/minúsculas y deben ser la única palabra en el mensaje.

---

## 📋 Flujo de la Encuesta (6 pasos)

| Paso | Pregunta | Validación |
|---|---|---|
| 1 | Escribe tu *nombre* y *apellido* completos: | No vacío |
| 2 | Escribe tu número de *cédula* *(solo números)*: | Solo dígitos, máximo 8 caracteres |
| 3 | Escribe tu *comuna*: | No vacío |
| 4 | Escribe tu *parroquia*: | No vacío |
| 5 | Escribe tu *correo electrónico*: | Debe contener @ y dominio |
| 6 | Escribe tu *número de teléfono*: | No vacío |

Al completar la encuesta, los datos se guardan en la tabla `historial` y se muestra un resumen con los comandos disponibles.

---

## 🗄️ Base de Datos

### Tabla: `sesiones` — Estado transitorio

Almacena el estado *actual* de cada conversación. Solo existe **una fila por número de teléfono** y se sobrescribe cada vez que el usuario avanza de paso o inicia un nuevo reporte.

| Campo | Tipo | Descripción |
|---|---|---|
| numero_telefono | VARCHAR(20) | Clave primaria |
| estado_actual | VARCHAR(50) | Estado FSM actual (INICIO, NOMBRE_APELLIDO, CEDULA, etc.) |
| datos_contexto | JSON | Datos recopilados durante la encuesta en curso |
| actualizado_el | TIMESTAMP | Última actualización |

> **Propósito:** El bot consulta esta tabla para saber en qué paso está el usuario *ahora mismo*. No guarda histórico.

### Tabla: `historial` — Registro permanente

Almacena **todos los reportes completados**. Cada vez que un usuario finaliza la encuesta se inserta una **fila nueva** con AUTO_INCREMENT. Nunca se sobrescribe ni se pierde información.

| Campo | Tipo | Descripción |
|---|---|---|
| id | INT (AUTO_INCREMENT) | Identificador único del reporte |
| numero_telefono | VARCHAR(20) | Número del proveedor |
| nombre_apellido | VARCHAR(200) | Nombre y apellido |
| cedula | VARCHAR(8) | Cédula de identidad |
| comuna | VARCHAR(100) | Comuna del proveedor |
| parroquia | VARCHAR(100) | Parroquia |
| correo | VARCHAR(150) | Correo electrónico |
| telefono | VARCHAR(20) | Teléfono de contacto |
| creado_el | TIMESTAMP | Fecha y hora del reporte |

> **Propósito:** Conservar el histórico completo de todos los reportes. Si un proveedor envía un reporte hoy, mañana y la semana siguiente, los tres quedan registrados como filas independientes.

### Diferencia clave entre ambas tablas

| Tabla | Guarda | ¿Se sobrescribe? | Función |
|---|---|---|---|
| `sesiones` | Estado actual del usuario | ✅ Sí (PK = teléfono) | Saber en qué paso está *ahora* |
| `historial` | Reportes completados | ❌ No (AUTO_INCREMENT) | Conservar el histórico de todos los envíos |

Son complementarias: `sesiones` maneja el "dónde va", `historial` guarda el "qué envió".

---

## ⏱️ Demora dinámica entre respuestas

Para evitar que WhatsApp detecte el bot como spam, cada respuesta se envía con una **demora aleatoria entre 1.5 y 5 segundos**. Esto simula el tiempo de lectura y escritura humana, haciendo que el tráfico de mensajes parezca natural y no automatizado.

WhatsApp puede bloquear cuentas que envían mensajes instantáneamente o con intervalos fijos, catalogándolos como spam. La demora dinámica reduce significativamente ese riesgo.

---

## ⏰ Tiempo de expiración de sesión

Si un usuario deja la encuesta a mitad y no interactúa durante más de **30 minutos**, la sesión se reinicia automáticamente al estado `INICIO`. Esto evita que mensajes accidentales posteriores se tomen como respuestas de preguntas anteriores.

---

## 🐛 Solución de Problemas

- **El bot no responde**: verifica que MariaDB esté corriendo y que el `.env` esté configurado correctamente.
- **Error "Unknown database"**: el bot intenta crearla automáticamente, pero verificá que el usuario de la DB tenga permisos de creación.
- **El QR no aparece**: eliminá el archivo `whatsapp_bot` (sesión SQLite) de la raíz y reiniciá el bot.

---

## 📝 Licencia

EULA — Uso libre pero no distribución. El incumplimiento puede conllevar cargos legales.

---

**Creador:** Ingeniero Jonathan Alexander Vargas
**Contacto:** contactoconexiatech@gmail.com
=======
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
>>>>>>> 3ea514dd5db3340e63003e713ee6a3f78f3ceec6
