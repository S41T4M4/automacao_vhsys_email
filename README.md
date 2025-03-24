# 📧 Automação de Envio de E-mails no VHSYS  

![GitHub repo size](https://img.shields.io/github/repo-size/S41T4M4/automacao_vhsys_email)  
![GitHub last commit](https://img.shields.io/github/last-commit/S41T4M4/automacao_vhsys_email)  




Automação desenvolvida para facilitar o **envio de e-mails na tela "Contas a Receber"** do VHSYS.  
A ferramenta **filtra boletos não enviados e dispara os e-mails automaticamente** usando **Python + Selenium**.  

---

## 📌 Recursos  

✅ **Login automático** no VHSYS  
✅ **Filtragem** de boletos não enviados  
✅ **Disparo automático** de e-mails  
✅ **Interface gráfica (Tkinter)** para facilitar o uso  
✅ **Execução em modo visível ou headless**  

---

## ⚡ Pré-requisitos  

Antes de iniciar, verifique se você tem os seguintes itens instalados:  

- [Python 3](https://www.python.org/downloads/)  
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/)  

### 🔹 Instale as dependências  

Execute o seguinte comando no terminal para instalar as bibliotecas necessárias:  

```bash
pip install selenium webdriver-manager
```

---

## 🚀 Como Usar  

### 🖥️ Modo depuração (com navegador aberto)  

Para visualizar a automação rodando no Chrome, utilize:  

```python
options.add_argument("--start-maximized")
```

### ⚡ Modo headless (sem abrir navegador)  

Para rodar a automação sem exibir a janela do Chrome, utilize:  

```python
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

---

## 📦 Como Gerar um Executável  

Para criar um **.exe** para rodar sem precisar do Python instalado, execute:  

```powershell
pyinstaller --onefile --windowed automacao_email.py
```

📌 O executável será gerado na pasta `dist/`.  

---


## 🤝 Contribuindo  

Se quiser contribuir para melhorias no projeto:  

1. **Fork** este repositório  
2. **Crie uma branch** para suas alterações:  
   ```bash
   git checkout -b minha-melhoria
   ```
3. **Commit suas mudanças**:  
   ```bash
   git commit -m "Melhoria na automação"
   ```
4. **Envie para o GitHub**:  
   ```bash
   git push origin minha-melhoria
   ```
5. **Abra um Pull Request** 🚀  

---


💡 **Criado por:** [Vitor Ibraim](https://github.com/S41T4M4)  
