from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
import time


def web_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def proxy_driver(url):
    driver = web_driver()
    proxyurl = "https://www.4everproxy.com/"
    driver.get(proxyurl)
    driver.maximize_window()
    time.sleep(3)
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]/p').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div[1]/div[2]/div/div/form/div[1]/input[1]').send_keys(url)

    driver.find_element(By.XPATH, '//*[@id="server_name"]').send_keys("f")
    driver.find_element(By.XPATH, '//*[@id="server_name"]').send_keys(Keys.RETURN)

    driver.find_element(By.XPATH, '//*[@id="server_select"]').send_keys("fr")
    driver.find_element(By.XPATH, '//*[@id="server_select"]').send_keys(Keys.RETURN)

    driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div[1]/div[2]/div/div/form/div[1]/button').click()

    return driver

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Paramètres du serveur SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Créer l'objet du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Ajouter le corps du message
    msg.attach(MIMEText(message, 'plain'))

    # Établir une connexion au serveur SMTP de Gmail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Se connecter au compte Gmail
    server.login(sender_email, sender_password)

    # Envoyer l'e-mail
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Fermer la connexion au serveur SMTP
    server.quit()

def load_config(path):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config