📧 Automação de Envio de E-mails no VHSYS
Este projeto automatiza o envio de e-mails na tela de "Contas a Receber" do VHSYS. Ele navega pela tabela, identifica os pedidos pendentes de envio de e-mail e dispara os e-mails automaticamente usando Python + Selenium.


Para rodar o script em modo de janela aberta, para melhor depuração:

options.add_argument("--start-maximized")

Para rodar o script sem abrir a janela:

options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


