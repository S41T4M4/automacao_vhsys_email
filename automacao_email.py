import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_automacao():
    url = "https://app.vhsys.com.br/index.php?Secao=Financeiro.Contas.Rec&Modulo=Financeiro"
    email = email_entry.get()
    senha = senha_entry.get()
    data_inicial_emissao_value = data_inicial_emissao_entry.get()
    data_final_emissao_value = data_final_emissao_entry.get()

    if not email or not senha or not data_inicial_emissao_value:
        status_label.config(text="Erro: Campos vazios!", fg="red")
        return

    try:
        status_label.config(text="Iniciando a automação...", fg="blue")
        logs_text.insert(tk.END, "Iniciando a automação...\n")
        logs_text.see(tk.END)
        root.update()

       
        print("Iniciando WebDriver...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Login
        print("Realizando login...")
        user = driver.find_element(By.ID, "login")
        senha_input = driver.find_element(By.ID, "senha")
        entrar = driver.find_element(By.ID, "btnLogar")
        user.send_keys(email)
        senha_input.send_keys(senha)
        entrar.click()
        
        time.sleep(4)
        
        
        try:
            erro_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tt-alert--danger")))

            if erro_login:
                print("Erro: Usuário ou senha incorretos!")
                status_label.config(text="Erro: Usuário ou senha incorretos!", fg="red")
                logs_text.insert(tk.END, "Erro: Usuário ou senha incorretos!\n")
                logs_text.see(tk.END)
                driver.quit()
                return
        except TimeoutException:
            pass

        print("Login bem-sucedido, continuando...")
        status_label.config(text="Login bem-sucedido, continuando...", fg="green")
        root.update()

       
        def scroll_down():
            driver.execute_script("window.scrollBy(0, 200);")
            print("Rolando a página para baixo...")
            time.sleep(2)

        scroll_down()

        print("Abrindo a busca avançada...")
        busca_avancada = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-text.advanced-search"))
        )
        busca_avancada.click()
        time.sleep(4)

        print("Selecionando forma de pagamento...")
        forma_pagamento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Listar"]/div[2]/div/div[4]/div[2]/div/div[3]/div[3]/div/div/button'))
        )
        forma_pagamento.click()
        time.sleep(2)

        boleto = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-value="Boleto"]')))
        boleto.click()
        time.sleep(2)

        select_element = driver.find_element(By.ID, "emails_pesquisa")
        select = Select(select_element)
        select.select_by_value("0")
        time.sleep(2)

        data_inicial_emissao = driver.find_element(By.ID, "data_emissao_rec_inicio")
        data_inicial_emissao.clear()
        data_inicial_emissao.send_keys(data_inicial_emissao_value)
        data_inicial_emissao.send_keys(Keys.ENTER)
        time.sleep(2)

        data_final_emissao = driver.find_element(By.ID, "data_emissao_rec_fim")
        data_final_emissao.clear()
        data_final_emissao.send_keys(data_final_emissao_value)
        data_final_emissao.send_keys(Keys.ENTER)
        time.sleep(2)

        filtrar = driver.find_element(By.CLASS_NAME, "btn-icon-search")
        filtrar.click()
        time.sleep(2)

        scroll_down()
        def scroll_down_email():
            driver.execute_script("window.scrollBy(0, 100);")
            print("Rolando a página para baixo...")
            time.sleep(2)

        def processar_emails():
            while True:
                botoes_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")

                if not botoes_email:
                    print("Todos os e-mails já foram enviados!")
                    status_label.config(text="Todos os e-mails já foram enviados!", fg="green")
                    logs_text.insert(tk.END, "Todos os e-mails já foram enviados!\n")
                    logs_text.see(tk.END)
                    root.update()
                    break

                total_emails = len(botoes_email)
                progresso_bar["maximum"] = total_emails

                for i, botao in enumerate(botoes_email, start=1):
                    try:
                        scroll_down_email()  

                       
                        botoes_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")
                        if i <= len(botoes_email): 
                            botao = botoes_email[i - 1]
                            botao.click()

                            time.sleep(10)
                            botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar')]")))
                            botao_enviar.click()
                            time.sleep(10)

                            progresso_bar["value"] = i
                            restante = len(driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email"))
                            status_label.config(text=f"Restam {restante} e-mails para enviar...", fg="blue")
                            logs_text.insert(tk.END, f"Restam {restante} e-mails para enviar...\n")
                            logs_text.see(tk.END)
                            root.update()

                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                        logs_text.insert(tk.END, f"Erro ao enviar e-mail: {e}\n", "erro")
                        logs_text.see(tk.END)
                        continue

        processar_emails()

        driver.quit()
        print("Automação concluída!")
        status_label.config(text="Automação concluída!", fg="green")
        logs_text.insert(tk.END, "Automação concluída!\n")
        logs_text.see(tk.END)
        progresso_bar["value"] = progresso_bar["maximum"]
        root.update()

    except Exception as e:
        print(f"Erro inesperado: {e}")
        logs_text.insert(tk.END, f"Erro inesperado: {e}\n", "erro")
        status_label.config(text=f"Erro inesperado: {e}", fg="red")
        root.update()


root = tk.Tk()
root.title("Automação de E-mails")
root.geometry("400x400")

tk.Label(root, text="E-mail:").pack()
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Senha:").pack()
senha_entry = tk.Entry(root, width=30, show="*")
senha_entry.pack()

tk.Label(root, text="Data Inicial:").pack()
data_inicial_emissao_entry = tk.Entry(root, width=30)
data_inicial_emissao_entry.pack()

tk.Label(root, text="Data Final:").pack()
data_final_emissao_entry = tk.Entry(root, width=30)
data_final_emissao_entry.pack()

botao_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
botao_iniciar.pack()

status_label = tk.Label(root, text="Aguardando início...", fg="gray")
status_label.pack()

progresso_bar = ttk.Progressbar(root, length=300, mode="determinate")
progresso_bar.pack()

logs_text = tk.Text(root, height=8, width=50)
logs_text.pack()

root.mainloop()
