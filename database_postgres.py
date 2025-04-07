import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Conexão com o banco PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("PG_HOST", "localhost"),
        port=os.environ.get("PG_PORT", 5432),  # <- ADICIONE ESSA LINHA
        database=os.environ.get("PG_DATABASE", "cotacoesdb"),
        user=os.environ.get("PG_USER", "postgres"),
        password=os.environ.get("PG_PASSWORD", "sua_senha")
    )

# Cria a tabela de tokens, se não existir
def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id SERIAL PRIMARY KEY,
                nro_cotacao TEXT NOT NULL,
                cnpj TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'PENDENTE',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    finally:
        conn.close()

# Salva novo token
def salvar_token(nro_cotacao, cnpj, token):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO links (nro_cotacao, cnpj, token)
            VALUES (%s, %s, %s)
        ''', (nro_cotacao, cnpj, token))
        conn.commit()
    finally:
        conn.close()

# Busca token pendente
def buscar_token(token):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT nro_cotacao, cnpj FROM links WHERE token = %s AND status = %s',
            (token, "PENDENTE")
        )
        resultado = cursor.fetchone()
        if resultado:
            return {'nro_cotacao': resultado[0], 'cnpj': resultado[1]}
        return None
    finally:
        conn.close()

# Marca token como confirmado
def marcar_como_confirmado(token):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE links SET status = %s WHERE token = %s',
            ("CONFIRMADO", token)
        )
        conn.commit()
    finally:
        conn.close()