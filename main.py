import time
import os
import sys
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
import logging
from libs.utils import load_config, web_driver, send_email


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Env variables
load_dotenv()
visa_email = os.getenv('VISA_EMAIL')
visa_mdp = os.getenv('VISA_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

# Config variables
config = load_config("config/config.yaml")
info_config = config['info']
year_month_max = info_config["year_month_max"]
recipient_email = info_config["recipient_email"]
url = info_config["url"]

def connection():
    url_down = True
    while url_down:
        try:
            driver = web_driver()
            logging.info(f"Start connection.")
            driver.get(url)
            driver.maximize_window()

            time.sleep(3)
            driver.save_screenshot('step0.png')
            # Connection
            driver.find_element(By.XPATH, '//*[@id="user_email"]').send_keys(visa_email)
            driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(visa_mdp)

            driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/div[3]/label/div').click()
            driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/p[1]/input').click()
            time.sleep(10)
            driver.save_screenshot('step1.png')
            # Appointment url
            driver.get(f"https://ais.usvisa-info.com/fr-fr/niv/schedule/34159750/appointment")
            time.sleep(10)
            driver.save_screenshot('step2.png')
            url_down = False
        except Exception as e:
            logging.info(f"Connection failed !")
            logging.error(e)
            time.sleep(60)
            continue
    return driver

driver = connection()

# Search
seconds = 60
while True:
    try:
        logging.info(f"Start searching.")
        driver.save_screenshot('step3.png')
        found = False
        driver.find_element(By.XPATH, '//*[@id="appointments_consulate_appointment_date"]').click()
        i = 1
        while i <= 20:
            year_month = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text
            year_month = year_month.split("\n")[1]
            if year_month == year_month_max:
                break
            
            month_element = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]')
            date_elements = []
            try:
                date_elements = month_element.find_elements(By.CLASS_NAME, 'undefined')
                logging.info(f"{year_month} | Number of days: {len(date_elements)}")
                date_elements = [
                date_element for date_element in date_elements 
                if 'ui-datepicker-unselectable' not in date_element.get_attribute('class') 
                and 'ui-state-disabled' not in date_element.get_attribute('class')
            ]
            except:
                pass
            if date_elements:
                found = True
                found_year_month = year_month
                break

            i += 1
            driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a').click()
        if found:
            logging.info(f"Found on {found_year_month}")
            subject = 'USA visa'
            message = f"""A slot is available on {found_year_month},
            Please click here to reserve it: {url}"""
            send_email(sender_email, sender_password, recipient_email, subject, message)
            logging.info(f"Email sent successfuly !")
            break
        logging.info(f"No slot found before {year_month_max}, waiting {seconds} seconds to research.")
        driver.refresh()
        time.sleep(seconds)
    except Exception as e:
        logging.info(f"Searching failed !")
        logging.error(e)
        driver.quit()
        driver = connection()
        continue