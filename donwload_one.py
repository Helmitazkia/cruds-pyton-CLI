from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


download_folder = r"C:\PythonProjects\selesai_donwload"

def download_selected_rows(driver, row_limit=4):
    rows = driver.find_elements(By.CSS_SELECTOR, "tr[id^='tableRow_']")
    total_rows = len(rows)
    print(f"Total baris tabel ditemukan: {total_rows}")

    for i in range(min(row_limit, total_rows)):
        try:
            row_id = rows[i].get_attribute("id").replace("tableRow_", "")
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, f"btnDwn-{row_id}"))
            )
            download_button.click()
            print(f"Download dimulai untuk row ID: {row_id}")
        except Exception as e:
            print(f"Gagal memproses row ke-{i + 1} dengan ID {row_id}: {e}")

def wait_for_downloads(folder, timeout=300):
    """
    Tunggu hingga semua file di folder download selesai diunduh.
    Args:
        folder: Folder tempat file diunduh.
        timeout: Batas waktu maksimum untuk menunggu (dalam detik).
    """
    start_time = time.time()
    while True:
        
        incomplete_files = [f for f in os.listdir(folder) if f.endswith(".crdownload")]
        #cek apakah masih ada crdownload di forder pengunduhan
        if not incomplete_files:
            print("Semua file telah selesai diunduh.")
            break
        
        if time.time() - start_time > timeout:
            print("Waktu tunggu habis, beberapa file mungkin belum selesai diunduh.")
            break
        
        time.sleep(1)


if __name__ == "__main__":
    options = Options()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.dell.com/support/home/en-id?app=drivers")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        driverSearch = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "entry-main-input-home"))
        )
        driverSearch.clear()
        driverSearch.send_keys("OEMR R6615")

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "btn-entry-select"))
        ).click()

        time.sleep(2)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[id^='tableRow_']"))
        )
        
        download_selected_rows(driver, row_limit=4)

        wait_for_downloads(download_folder)

        print(f"Hasil download disimpan di folder: {download_folder}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()
