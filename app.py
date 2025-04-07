from flask import Flask, render_template, request, redirect
import uuid
import re
from mysql_utils import buscar_cotacao_por_codigo_e_cnpj
from database_postgres import init_db, salvar_token, buscar_token, marcar_como_confirmado
from enviar_email import enviar_email_smtp as enviar_email  # Usando SMTP
import os  # necessário para pegar a porta do ambiente

app = Flask(__name__)
init_db()


@app.route('/', methods=['GET', 'POST'])
def formulario_vendedor():
    if request.method == 'POST':
        nro_cotacao = request.form['nro_cotacao'].strip()
        cnpj_input = request.form['cnpj'].strip()
        cnpj = re.sub(r'\D', '', cnpj_input)

        dados = buscar_cotacao_por_codigo_e_cnpj(nro_cotacao, cnpj)

        if not dados:
            return render_template('formulario.html', erro="Nenhuma cotação encontrada com esse número e CNPJ.")

        token = str(uuid.uuid4())
        salvar_token(nro_cotacao, cnpj, token)
        base_url = os.environ.get("BASE_URL", "http://localhost:5000")
        link = f"{base_url}/confirmar/{token}"


        return render_template('link_gerado.html', link=link, dados=dados)

    return render_template('formulario.html')


@app.route('/confirmar/<token>', methods=['GET', 'POST'])
def confirmar_cotacao(token):
    token_data = buscar_token(token)
    if not token_data:
        return render_template('erro.html', mensagem="Link inválido ou expirado.")

    dados = buscar_cotacao_por_codigo_e_cnpj(token_data['nro_cotacao'], token_data['cnpj'])

    if request.method == 'POST':
        marcar_como_confirmado(token)
        try:
            destinatario = request.form['email']
            enviar_email(
                destinatario=destinatario,
                empresa=dados['empresa'],
                cnpj=dados['cnpj'],
                data=dados['data'],
                agente_nome=dados['agente_nome'],
                telefone=dados['telefone'],
                fax=dados['fax'],
                endereco=dados['endereco']
            )
        except Exception as e:
            return render_template('erro.html', mensagem=f"Erro ao enviar e-mail: {str(e)}")

        return render_template('sucesso.html', email=destinatario)

    return render_template('form_cliente.html', dados=dados)


# 🔧 Esta parte é obrigatória para funcionar no Railway
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))