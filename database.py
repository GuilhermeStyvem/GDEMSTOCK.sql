import pyodbc

# ============================================
# CONFIGURAÇÃO DA CONEXÃO COM O SQL SERVER
# ============================================
# Altere os valores abaixo conforme seu ambiente:
SERVER   = "localhost"        # ou o IP do servidor
DATABASE = "GDME_STOCK"
USERNAME = "sa"               # seu usuário do SQL Server
PASSWORD = "TSP@130505"   # sua senha do SQL Server

CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
)

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    return pyodbc.connect(CONNECTION_STRING)
