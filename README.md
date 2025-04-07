# 📦 Sistema de Confirmação de Cotações

Este projeto é uma aplicação web desenvolvida em **Python + Flask**, que permite a confirmação de cotações comerciais por parte de clientes via um link único. O objetivo é facilitar o processo de aceite de propostas e registrar automaticamente a confirmação no banco de dados, além de enviar os dados por e-mail.

---

## 🎯 Funcionalidades

- Consulta a uma cotação no banco MySQL com base no número e CNPJ
- Geração de um link único e seguro de confirmação
- Registro da confirmação em banco PostgreSQL
- Envio automático de e-mail com os dados da cotação ao cliente
- Interface amigável com Bootstrap

---

## 🧰 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Gunicorn](https://gunicorn.org/) (para produção)
- [MySQL](https://www.mysql.com/) (consulta de cotações)
- [PostgreSQL](https://www.postgresql.org/) (armazenamento de tokens)
- [SMTP Outlook](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365)
- [Bootstrap 5](https://getbootstrap.com/)

---



