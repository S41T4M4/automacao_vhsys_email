Automação de Envio de E-mails no VHSYS
Este projeto automatiza o envio de e-mails na tela de "Contas a Receber" do VHSYS. Ele navega pela tabela, identifica os pedidos pendentes de envio de e-mail e dispara os e-mails automaticamente usando Python + Selenium.


1️⃣ Instale as Dependências

pip install selenium
2️⃣ Configure o WebDriver
Baixe o chromedriver correspondente à sua versão do Google Chrome e coloque-o no caminho do sistema.

3️⃣ Edite as Credenciais
Se o login no VHSYS for necessário, ajuste o script para incluir o login automaticamente.

4️⃣ Execute o Script

python automacao_email.py
