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


"""
Program ini bertujuan untuk mengambil screenshot dari semua halaman "Coming Soon" di situs web 21Cineplex.
Setiap halaman akan di-scroll secara penuh, diambil screenshot-nya, dan kemudian dikonversi menjadi file PDF.
Program ini juga menangani navigasi antar halaman secara otomatis melalui elemen pagination hingga mencapai halaman terakhir.
"""


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


# Fungsi untuk mengonversi gambar ke PDF
def convert_image_to_pdf(image_path, pdf_path):
    image = Image.open(image_path)
    pdf = image.convert('RGB')
    pdf.save(pdf_path)


# Blok utama program
if __name__ == "__main__":
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        
        driver.get("https://21cineplex.com/")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        
        upcoming_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upcoming"))
        )
        upcoming_menu.click()

        #Scroll ke bawah untuk melihat pagination
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


        page_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-link[href*='/comingsoon/1']"))
        )
        page_1.click()

     
        driver.get("https://21cineplex.com/comingsoon/1")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Berhasil membuka halaman: https://21cineplex.com/comingsoon/1")

        # 6. Loop untuk pagination dan screenshot
        page_number = 1
        while True:
            print(f"Mengambil screenshot halaman {page_number}...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_page_{page_number}_{timestamp}.png"
            capture_entire_page_with_scrolling(driver, screenshot_path)

   
            pdf_path = f"screenshot_page_{page_number}_{timestamp}.pdf"
            convert_image_to_pdf(screenshot_path, pdf_path)
            print(f"Halaman {page_number} berhasil disimpan sebagai PDF: {pdf_path}")

         
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
                print(f"Gambar {screenshot_path} telah dihapus setelah konversi ke PDF.")

            # Cek apakah ada halaman berikutnya
            try:
                next_pages = driver.find_elements(By.CSS_SELECTOR, ".page-link")
                found_next = False
                for page in next_pages:
                    href = page.get_attribute("href")
                    if href and f"/comingsoon/{page_number + 1}" in href:  
                        page.click()
                        time.sleep(3)  
                        page_number += 1
                        found_next = True
                        break

                if not found_next:
                    print("Tidak ada halaman berikutnya. Proses selesai.")
                    break
            except Exception as e:
                print(f"Kesalahan saat memvalidasi halaman berikutnya: {e}")
                break

        print("Semua halaman telah diambil screenshot-nya dan dikonversi ke PDF.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()
