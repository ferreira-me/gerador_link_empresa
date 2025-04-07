import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def enviar_email_smtp(destinatario, empresa, cnpj, data, agente_nome, telefone, fax, endereco):
    # Configurações SMTP
    smtp_servidor = "smtp.office365.com"
    smtp_porta = "sua porta"
    remetente = "seu e-mail"
    senha = os.environ.get("SMTP_SENHA")  # Pegando do .env

    # Corpo do e-mail
    corpo = f"""
Olá!

Recebemos a sua confirmação da cotação.

Segue abaixo os dados:

Empresa: {empresa}
CNPJ: {cnpj}
Data da Cotação: {data}
Agente Responsável: {agente_nome}
Telefone: {telefone or 'N/A'}
Fax: {fax or 'N/A'}
Endereço: {endereco or 'N/A'}

Em caso de dúvidas, estamos à disposição.

Atenciosamente,  
Audaz Global
    """

    # Monta o e-mail
    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = ", ".join([
        destinatario
        
    ])
    msg['Subject'] = "Confirmação de Cotação"
    msg.set_content(corpo)

    # Envia o e-mail
    try:
        with smtplib.SMTP(smtp_servidor, smtp_porta) as smtp:
            smtp.set_debuglevel(1)
            smtp.starttls()
            smtp.login(remetente, senha)
            smtp.send_message(msg)
            print(f"E-mail enviado para {msg['To']}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")





