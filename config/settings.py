# settings.py
import os

# Configuración general del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta de archivos CSV
DATA_DIR = os.path.join(BASE_DIR, '../data')

# Ruta de salida para visualizaciones
OUTPUT_DIR = os.path.join(BASE_DIR, '../output')

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'user': 'root',
    'password': 'Admin.123',
    'host': 'localhost',
    'database': 'ouladdb'
}

# Cadena de conexión SQLAlchemy
SQLALCHEMY_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"