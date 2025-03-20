import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
from webdriver_manager.chrome import ChromeDriverManager



def iniciar_automacao():
    email = email_entry.get()
    senha = senha_entry.get()

    if not email or not senha:
        messagebox.showwarning("Campos vazios", "Por favor, insira e-mail e senha.")
        return

    try:
        messagebox.showinfo("Automação", "Iniciando a automação...")

        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Abrindo a página de login...", flush=True)
        driver.get(" https://app.vhsys.com.br/index.php?Secao=Financeiro.Contas.Rec&Modulo=Financeiro")

        wait = WebDriverWait(driver, 16)

        print("Preenchendo login e senha...", flush=True)
        user = driver.find_element(By.ID, "login")
        senha_input = driver.find_element(By.ID, "senha")
        entrar = driver.find_element(By.ID, "btnLogar")
        user.send_keys(email)
        senha_input.send_keys(senha)
        entrar.click()

        print("Aguardando a página carregar...", flush=True)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")))

        def scroll_to_bottom():
            print("Rolando até o final da página...", flush=True)
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("Chegou ao final da página.", flush=True)
                    break
                last_height = new_height

        scroll_to_bottom()

        print("Iniciando processamento dos e-mails...", flush=True)

        while True:
            botao_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")

            if not botao_email:
                print("Nenhum botão de e-mail encontrado. Encerrando script.", flush=True)
                messagebox.showinfo("Automação", "Todos os e-mails foram enviados.")
                break

            for i, botao in enumerate(botao_email, start=1):
                try:
                    tooltip = botao.get_attribute("data-tooltip")
                    if tooltip == "Enviar Email":
                        print(f"Processando e-mail {i}/{len(botao_email)}...", flush=True)
                        botao.click()
                        time.sleep(3)

                        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar')]")))
                        botao_enviar.click()

                        time.sleep(10)
                    botao_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")
                    print(f"Restam {len(botao_email)} emails para enviar.", flush=True)

                    if not botao_email:
                        print("Todos os e-mails foram enviados.", flush=True)
                        messagebox.showinfo("Automação", "Todos os e-mails foram enviados com sucesso.")
                        break

                except NoSuchElementException:
                    print("Erro: Elemento não encontrado durante a automação.", flush=True)
                    messagebox.showerror("Erro", "Não foi possível localizar um elemento na página.")
                    continue

                except TimeoutException:
                    print("Erro: Tempo limite excedido para carregar o elemento.", flush=True)
                    messagebox.showerror("Erro", "Tempo de espera excedido. Verifique sua conexão ou a página.")
                    continue

                except ElementClickInterceptedException:
                    print("Erro: Não foi possível clicar no botão, ele pode estar oculto.", flush=True)
                    messagebox.showerror("Erro", "Não foi possível clicar no botão. Ele pode estar oculto.")
                    continue

                except Exception as e:
                   
                    print(f"Erro inesperado: {e}", flush=True)
                    continue

        print("Encerrando WebDriver...", flush=True)
        driver.quit()
        messagebox.showinfo("Sucesso", "Automação concluída!")
        print("Script finalizado com sucesso!", flush=True)

    except Exception as e:
        print(f"Não possui emails para serem enviados {e}", flush=True) 
        messagebox.showerror("Sem Emails", "Não possuem e-mails para serem enviados")


root = tk.Tk()
root.title("Automação de E-mails")
root.geometry("350x200")

tk.Label(root, text="E-mail:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Senha:").pack(pady=5)
senha_entry = tk.Entry(root, width=30, show="*")
senha_entry.pack()

botao_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
botao_iniciar.pack(pady=20)

root.mainloop()
