from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from datetime import datetime
import os
import time

try:
 
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

 
    driver.get("https://www.tokopedia.com/login")

    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "login"))  
    )

 
    username_field = driver.find_element(By.NAME, "login")
    username_field.send_keys("085781046500")

  
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))  # Ganti sesuai dengan elemen tombol
        
    ).click()

    

    time.sleep(4)
    print(username_field.get_attribute("value"))  # Mendapatkan nilai input di kolom username

   

except Exception as e:
    print(f"Terjadi kesalahan: {e}")

finally:
    # Jangan tutup browser secara otomatis
    print("Program selesai tanpa menutup browser.")
