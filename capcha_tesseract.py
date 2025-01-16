# This script automates the login process for a web application by handling CAPTCHA challenges using Selenium and OCR.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import traceback
from PIL import Image
import pytesseract
from pytesseract import pytesseract

if __name__ == "__main__":
    for i in range(10):
        print(f"Percobaan ke-{i+1}")
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get("https://xtra.superindo.co.id/")

            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print("Alert ditutup.")
            except:
                print("Tidak ada alert yang muncul.")

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            driver_email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            driver_email.clear()
            driver_email.send_keys("setyawan.pramono@nirwanalestari.com")
            print("Email berhasil diisi!")

            driver_password = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            driver_password.clear()
            driver_password.send_keys("Lion@4321981987654321")
            print("Password berhasil diisi!")

            captcha_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "Imageid"))
            )
            captcha_path = f"C:\\PythonProjects\\chapca_selesai\\captcha_{i+1}.png"
            captcha_element.screenshot(captcha_path)
            print("Gambar CAPTCHA berhasil disimpan!")

            path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd = path_to_tesseract

            img = Image.open(captcha_path)
            
            #image to text
            text = pytesseract.image_to_string(img)
            print(f"CAPTCHA dibaca: {text}")

            captcha_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "captcha"))
            )
            captcha_field.clear()
            captcha_field.send_keys(text)
            print("CAPTCHA berhasil diisi!")

            login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "btn-login"))
            )
            login_button.click()
            print("Login berhasil!")

        except Exception as e:
            print("Terjadi kesalahan selama proses Selenium:")
            traceback.print_exc()

        finally:
            driver.quit()
