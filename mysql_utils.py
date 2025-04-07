# mysql_utils.py
import mysql.connector
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def buscar_cotacao_por_codigo_e_cnpj(codigo, cnpj=None):
    try:
        conexao = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        cursor = conexao.cursor(dictionary=True)

        query = """
            SELECT 
                Q.CODE,
                Q.DATE_CREATION, 
                C.NAME_CG AS CLIENTE_NOME, 
                C.FEDERAL_REGISTRATION, 
                A.NAME_CG AS AGENTE_NOME,
                C.PHONE, 
                C.FAXPHONE,
                AD.STREET_NAME,
                AD.COMPLEMENT,
                AD.CITY_NAME,
                AD.NEIGHBORHOOD
            FROM M0205_QUOTATION Q
            JOIN M0130_CONTACT_GENERAL C ON Q.CLIENT_CONTACT_GENERAL_FK = C.ID
            LEFT JOIN M0130_CONTACT_GENERAL A ON Q.AGENT_CONTACT_GENERAL_FK = A.ID
            LEFT JOIN M0001_ADDRESS AD ON C.ADDRESS_FK = AD.ID
            WHERE Q.CODE = %s
        """

        params = [codigo]

        if cnpj:
            query += """
            AND REPLACE(REPLACE(REPLACE(C.FEDERAL_REGISTRATION, '.', ''), '/', ''), '-', '') = %s
            """
            params.append(cnpj)

        query += " LIMIT 1"

        cursor.execute(query, tuple(params))
        resultado = cursor.fetchone()

        if resultado:
            endereco = f"{resultado['STREET_NAME'] or ''}, {resultado['COMPLEMENT'] or ''}, {resultado['NEIGHBORHOOD'] or ''}, {resultado['CITY_NAME'] or ''}"
            return {
                'nro_cotacao': resultado['CODE'],
                'empresa': resultado['CLIENTE_NOME'],
                'cnpj': resultado['FEDERAL_REGISTRATION'],
                'data': resultado['DATE_CREATION'],
                'agente_nome': resultado['AGENTE_NOME'],
                'telefone': resultado['PHONE'],
                'fax': resultado['FAXPHONE'],
                'endereco': endereco.strip(', ').strip()
            }

        return None

    except Exception as e:
        print(f"[ERRO MySQL] {e}")
        return None

    finally:
        if 'conexao' in locals():
            conexao.close()