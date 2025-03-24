import tkinter as tk
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
        root.update()

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 26)

        user = driver.find_element(By.ID, "login")
        senha_input = driver.find_element(By.ID, "senha")
        entrar = driver.find_element(By.ID, "btnLogar")
        user.send_keys(email)
        senha_input.send_keys(senha)
        entrar.click()

        def scroll_to_bottom():
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        scroll_to_bottom()

        busca_avancada = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-text.advanced-search"))
        )
        busca_avancada.click()
        time.sleep(4)

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
        data_inicial_emissao.click()
        time.sleep(2)
        data_inicial_emissao.clear()
        data_inicial_emissao.send_keys(data_inicial_emissao_value)
        data_inicial_emissao.send_keys(Keys.ENTER)

        time.sleep(2)
        data_final_emissao = driver.find_element(By.ID, "data_emissao_rec_fim")
        data_final_emissao.click()
        time.sleep(2)
        data_final_emissao.clear()
        data_final_emissao.send_keys(data_final_emissao_value)
        data_final_emissao.send_keys(Keys.ENTER)

        time.sleep(2)
        filtrar = driver.find_element(By.CLASS_NAME, "btn-icon-search")
        filtrar.click()
        time.sleep(2)

        scroll_to_bottom()

        def processar_emails():
            while True:
                botoes_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")

                if not botoes_email:
                    status_label.config(text="Todos os e-mails foram enviados!", fg="green")
                    root.update()
                    break

                for i, botao in enumerate(botoes_email, start=1):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                        time.sleep(1)

                        status_label.config(text=f"Enviando e-mail {i}/{len(botoes_email)}...", fg="blue")
                        root.update()

                        botao.click()
                        time.sleep(3)

                        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar')]")))
                        botao_enviar.click()

                        try:
                            WebDriverWait(driver, 3).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "notify-message-general-wrapper"))
                            )
                            status_label.config(text="Erro: e-mail do cliente incorreto!", fg="red")
                            root.update()
                            continue
                        except TimeoutException:
                            pass

                        time.sleep(5)
                        botoes_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")
                        restante = len(botoes_email)

                        status_label.config(text=f"Restam {restante} e-mails para enviar...", fg="blue")
                        root.update()

                        if not botoes_email:
                            status_label.config(text="Todos os e-mails foram enviados com sucesso!", fg="green")
                            root.update()
                            break

                    except NoSuchElementException:
                        status_label.config(text="Erro: Elemento não encontrado.", fg="red")
                        root.update()
                        continue

                    except TimeoutException:
                        status_label.config(text="Erro: Tempo de espera excedido.", fg="red")
                        root.update()
                        continue

                    except ElementClickInterceptedException:
                        status_label.config(text="Erro: Não foi possível clicar no botão.", fg="red")
                        root.update()
                        continue

                    except Exception as e:
                        status_label.config(text=f"Erro inesperado: {e}", fg="red")
                        root.update()
                        continue

            driver.quit()
            status_label.config(text="Automação concluída!", fg="green")
            root.update()

        processar_emails()

    except Exception as e:
        status_label.config(text=f"Erro inesperado: {e}", fg="red")
        root.update()
        driver.quit()


root = tk.Tk()
root.title("Automação de E-mails")
root.geometry("300x350")

tk.Label(root, text="E-mail:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Senha:").pack(pady=5)
senha_entry = tk.Entry(root, width=30, show="*")
senha_entry.pack()

tk.Label(root, text="Data Inicial de Emissão").pack(pady=5)
data_inicial_emissao_entry = tk.Entry(root, width=30)
data_inicial_emissao_entry.pack()

tk.Label(root, text="Data Final de emissão").pack(pady=5)
data_final_emissao_entry = tk.Entry(root, width=30)
data_final_emissao_entry.pack()

botao_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
botao_iniciar.pack(pady=20)

status_label = tk.Label(root, text="Aguardando início...", fg="gray")
status_label.pack(pady=10)

root.mainloop()
