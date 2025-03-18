from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os 
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("VHSYS_EMAIL")
PASSWORD = os.getenv("VHSYS_PASSWORD")

print("Iniciando o script para enviar e-mails...", flush=True)

service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

print("Abrindo a página de login...", flush=True)
driver.get("https://app.vhsys.com.br/index.php?Secao=Financeiro.Contas.Rec&Modulo=Financeiro")

wait = WebDriverWait(driver, 10)

print("Preenchendo login e senha...", flush=True)
user = driver.find_element(By.ID, "login")
senha = driver.find_element(By.ID, "senha")
entrar = driver.find_element(By.ID, "btnLogar")
user.send_keys(EMAIL)
senha.send_keys(PASSWORD)
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
                break

        except Exception as e:
            print(f"Erro ao processar um email: {e}", flush=True)
            continue

print("Encerrando WebDriver...", flush=True)
driver.quit()
print("Script finalizado com sucesso!", flush=True)
