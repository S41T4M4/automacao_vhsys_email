from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://app.vhsys.com.br/index.php?Secao=Financeiro.Contas.Rec&Modulo=Financeiro")

wait = WebDriverWait(driver, 10)

email = driver.find_element(By.ID, "login")
senha = driver.find_element(By.ID, "senha")
entrar = driver.find_element(By.ID, "btnLogar")
email.send_keys("vitor_jcdecor")
senha.send_keys('620MS8W.6ci"')
entrar.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")))

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom()


while True:
    botao_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")

    if not botao_email:
        print("Nenhum botão de e-mail encontrado.")
        break

    for botao in botao_email:
        try:
            tooltip = botao.get_attribute("data-tooltip")
            if tooltip == "Enviar Email":
                botao.click()
                time.sleep(3)

                botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar')]")))
                botao_enviar.click()

                time.sleep(6)

        
            botao_email = driver.find_elements(By.CLASS_NAME, "action-icon.icon-envelope.tip.top.action-send-email")
            print(f"Restam {len(botao_email)} emails para enviar. ")
            if not botao_email:
                print("Todos os e-mails foram enviados.")
                break

        except Exception as e:
            print(f"Erro ao processar um email: {e}")
            continue

driver.quit()
