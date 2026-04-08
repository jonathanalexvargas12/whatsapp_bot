import os

def create_structure():
    # Definición de la estructura
    folders = [
        'database',
        'flows',
        'credentials'
    ]
    
    files = {
        'database/connection.py': '# Configuración de MariaDB\nimport mysql.connector',
        'database/models.py': '# Modelos de tablas',
        'flows/router.py': '# Enrutador de estados',
        'flows/steps.py': '# Lógica de pasos',
        'main.py': '# Punto de entrada principal\nfrom neonize.client import NewClient',
        '.env': 'DB_HOST=localhost\nDB_USER=root\nDB_PASS=\nDB_NAME=wa_bot_db',
        'requirements.txt': 'neonize\nmysql-connector-python\npython-dotenv'
    }

    # Crear carpetas
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, '__init__.py'), 'w') as f:
            pass
        print(f"✔ Carpeta creada: {folder}")

    # Crear archivos
    for path, content in files.items():
        with open(path, 'w') as f:
            f.write(content)
        print(f"✔ Archivo creado: {path}")

if __name__ == "__main__":
    create_structure()
    print("\n🚀 Estructura lista. Ahora ejecuta: pip install -r requirements.txt")