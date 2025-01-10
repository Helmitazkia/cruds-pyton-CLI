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



# Lokasi folder download
download_folder = r"C:\PythonProjects\selesai_donwload"

def capture_entire_page_with_scrolling():
 
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # for scroll_position in range(0, total_height, viewport_height):
      
    #     driver.execute_script(f"window.scrollTo(0, {scroll_position})")
    
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(2) 
      
    

# Fungsi utama
if __name__ == "__main__":
    
    options = Options()
    
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False, 
        "directory_upgrade": True, 
        "safebrowsing.enabled": True 
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")  
    options.add_argument("--ignore-certificate-errors")  
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    # Gunakan WebDriver Manager untuk secara otomatis mengelola ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Buka website utama
        driver.get("https://www.dell.com/support/home/en-id?app=drivers")
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ) 
        
        driverSearch = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "entry-main-input-home"))
        )

        driverSearch.clear()
        driverSearch.send_keys("OEMR R6615")
        time.sleep(1)
        
        
        driverSearchBtn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "btn-entry-select"))
        )
       
        
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "btn-entry-select"))
            
        ).click()
                
        capture_entire_page_with_scrolling()
        
        time.sleep(1)
        
        
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ckbCheckAllMdl'))
        )
        driver.execute_script("document.getElementById('ckbCheckAllMdl').click();")
        
        time.sleep(1)
        
        var1 = driver.find_element(By.ID, "ckbCheckAllMdl").is_selected()
        
        print(var1)
        
        
        driverSearchBtn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "mdldriversDL-DownloadList"))
        )
       
        
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "mdldriversDL-DownloadList"))
            
        ).click()
        
        time.sleep(10)
        
        print(f"Hasil download disimpan di folder: {download_folder}")
        
    
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()