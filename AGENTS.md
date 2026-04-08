# 🛠 AGENTS.MD: Configuración del Bot de WhatsApp (Python + Neonize + MariaDB)

Este documento contiene las especificaciones técnicas e instrucciones de inicialización para desarrollar un bot de WhatsApp automatizado con persistencia en español.

## 1. Contexto del Proyecto
* **Objetivo:** Crear un bot de WhatsApp automatizado con flujo conversacional.
* **Motor de WhatsApp:** `Neonize` (Wrapper de Python para `whatsmeow` en Go).
* **Base de Datos:** `MariaDB 10.11+` para persistencia de estados.
* **Patrón de Diseño:** Máquina de Estados Finitos (FSM).

## 2. Requisitos del Sistema
El agente debe verificar:
* **Python:** 3.10 o superior.
* **Go (Golang):** Necesario para compilar las dependencias de `whatsmeow`.
* **MariaDB Server:** Instancia activa.

## 3. Estructura del Proyecto (Scaffolding)
```text
whatsapp_bot/
├── credentials/         # Almacena el archivo .db de la sesión de WhatsApp
├── database/
│   ├── connection.py    # Pool de conexiones a MariaDB
│   └── models.py        # Esquemas de tablas (En español)
├── flows/
│   ├── router.py        # Lógica para redireccionar según el estado del usuario
│   └── steps.py         # Definición de respuestas por cada paso
├── .env                 # Variables de entorno
├── main.py              # Punto de entrada
└── requirements.txt     # Dependencias del proyecto