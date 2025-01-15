from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import time

def update_google_sheet(date, month, result_count):
    try:
        # Autentikasi ke Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/PythonProjects/credentials.json", scope)
        client = gspread.authorize(creds)
        print("Autentikasi berhasil!")

        #Open
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1WuFWf2purRlAnBVN8X5msXPp_cDRsHnjPJ4LST1ozCI/edit?gid=0#gid=0").sheet1
        print("Spreadsheet berhasil dibuka!")

        # Temukan kolom berdasarkan bulan
        column = None
        if month == "January":
            column = "C"  
        else:
            print("Bulan tidak dikenali!")
            return

        # Update nilai di Google Sheets berdasarkan tanggal
        row = int(date) + 1  # Baris berdasarkan tanggal
        cell = f"{column}{row}"
        sheet.update_acell(cell, result_count)
        print(f"Data berhasil diperbarui di {cell}: {result_count}")

    except Exception as e:
        print("Kesalahan saat mengupdate Google Sheets:")
        traceback.print_exc()

if __name__ == "__main__":
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://127.0.0.1:8000/admin/login")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Login
        driverEmail = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "data.email"))
        )
        driverEmail.clear()
        driverEmail.send_keys("helmitazkia85@gmail.com")
        print("Email berhasil diisi!")

        time.sleep(1)
        driverPassword = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "data.password"))
        )
        driverPassword.clear()
        driverPassword.send_keys("12345678")
        print("Password berhasil diisi!")

        time.sleep(1)
        driverBtn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driverBtn.click()
        print("Login berhasil!")

        
        driver.get("http://127.0.0.1:8000/admin")
        category = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Categories"))
        )
        category.click()
        print("Berhasil membuka halaman Categories!")

        # Hitung jumlah data
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        result_count = len(rows)
        print(f"Jumlah data yang ditemukan: {result_count}")

        # Dapatkan tanggal dan bulan saat ini
        now = datetime.now()
        date = now.strftime("%d")
        month = now.strftime("%B")

        # Update Google Sheets
        update_google_sheet(date, month, result_count)

    except Exception as e:
        print("Terjadi kesalahan selama proses Selenium:")
        traceback.print_exc()

    finally:
        driver.quit()
