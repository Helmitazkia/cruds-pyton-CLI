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




def capture_entire_page_with_scrolling(driver, save_path):
 
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

   
    stitched_image = []
  
    for scroll_position in range(0, total_height, viewport_height):
      
        driver.execute_script(f"window.scrollTo(0, {scroll_position})")
        time.sleep(1) 
      
        screenshot_path = f"temp_screenshot_{scroll_position}.png"
        driver.save_screenshot(screenshot_path)
        stitched_image.append(screenshot_path)

    
    images = [Image.open(img) for img in stitched_image]  
    total_width = images[0].width 
    stitched_height = sum(img.height for img in images) 
 
    stitched_image_result = Image.new("RGB", (total_width, stitched_height))
    current_height = 0 

    
    for img in images:
        stitched_image_result.paste(img, (0, current_height))
        current_height += img.height  

    
    stitched_image_result.save(save_path)

   
    for img in stitched_image:
        os.remove(img)

# Fungsi utama
if __name__ == "__main__":
    
    options = Options()

    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")  
    options.add_argument("--ignore-certificate-errors")  
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    # Gunakan WebDriver Manager untuk secara otomatis mengelola ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Buka website utama
        driver.get("https://21cineplex.com/")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ) 


        theaters_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Theaters"))
        )
        theaters_menu.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "cityChanged"))
        )  

       
        from selenium.webdriver.support.ui import Select
        dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "cityChanged"))
        )
        select = Select(dropdown)
        select.select_by_visible_text("BEKASI")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "CIPLAZ CIBITUNG XXI"))
        )  

        
        ciplaz_cibitung = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "CIPLAZ CIBITUNG XXI"))
        )
        ciplaz_cibitung.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )  

     
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshot_{timestamp}.png"
        capture_entire_page_with_scrolling(driver, screenshot_path)

       
        pdf_path = f"screenshot_{timestamp}.pdf"
        image = Image.open(screenshot_path)
        pdf = image.convert('RGB')
        pdf.save(pdf_path)

        print(f"Screenshot dan PDF telah berhasil disimpan: {pdf_path}")

        # Hapus file gambar sementara
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        # Tutup driver
        driver.quit()
