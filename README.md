📧 Automação de Envio de E-mails no VHSYS
Este projeto automatiza o envio de e-mails na tela de "Contas a Receber" do VHSYS. Ele navega pela tabela, identifica os pedidos pendentes de envio de e-mail e dispara os e-mails automaticamente usando Python + Selenium.

🚀 Funcionalidades
✅ Acesso Automático: O bot acessa a página de "Contas a Receber" no VHSYS.
✅ Leitura da Tabela: Identifica os pedidos e verifica o status do e-mail.
✅ Envio de E-mails: Clica no botão de envio para pedidos pendentes.
✅ Confirmação de Envio: Aguarda e verifica se o status do e-mail mudou para "Enviado".
✅ Tratamento de Erros: Lida com problemas de conexão e reinicia o WebDriver, se necessário.

🛠️ Tecnologias
Python 3.10+
Selenium WebDriver
Chromedriver
WebDriverWait para garantir a interação com elementos carregados dinamicamente
🔧 Configuração e Uso
1️⃣ Instale as Dependências
sh
Copiar
Editar
pip install selenium
2️⃣ Configure o WebDriver
Baixe o chromedriver correspondente à sua versão do Google Chrome e coloque-o no caminho do sistema.

3️⃣ Edite as Credenciais
Se o login no VHSYS for necessário, ajuste o script para incluir o login automaticamente.

4️⃣ Execute o Script
sh
Copiar
Editar
python automacao_email.py
📝 Como Funciona?
1️⃣ Acessa a página do VHSYS
2️⃣ Extrai a tabela de pedidos
3️⃣ Verifica se o e-mail foi enviado
4️⃣ Clica para enviar caso necessário
5️⃣ Aguarda a confirmação do envio

⚠️ Possíveis Problemas
Erro de conexão (WinError 10054): Ocorre se o VHSYS encerrar a conexão. O script já implementa uma reconexão automática.
Elementos não carregando: Pode ser necessário ajustar WebDriverWait para tempos de espera maiores.
🏆 Melhorias Futuras
🔹 Exportar logs detalhados para facilitar auditoria
🔹 Implementar interface gráfica (GUI) para melhor usabilidade
🔹 Adicionar suporte para outros métodos de pagamento além de boletos

