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


# Fungsi untuk mengambil screenshot dari seluruh halaman dengan scrolling
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
    pdf = image.convert('RGB')  # Konversi ke RGB (diperlukan untuk PDF)
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

        # Klik menu "Upcoming"
        upcoming_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Upcoming")))
        upcoming_menu.click()

        # Tunggu hingga elemen navigasi termuat
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))

        # Looping melalui semua halaman
        page_links = driver.find_elements(By.CLASS_NAME, "page-link")
        page_count = len(page_links)
        for i in range(page_count):
            print(f"Mengambil screenshot halaman {i + 1}...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_page_{i + 1}_{timestamp}.png"
            capture_entire_page_with_scrolling(driver, screenshot_path)

            # Convert gambar screenshot ke PDF
            pdf_path = f"screenshot_page_{i + 1}_{timestamp}.pdf"
            convert_image_to_pdf(screenshot_path, pdf_path)
            print(f"Halaman {i + 1} berhasil disimpan sebagai PDF: {pdf_path}")
            
            
            # Klik link ke halaman berikutnya, kecuali jika di halaman terakhir
            if i < page_count - 1:
                next_page = driver.find_elements(By.CLASS_NAME, "page-link")[i + 1]
                next_page.click()
                time.sleep(3)  # Tunggu agar halaman baru dimuat
                
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
                print(f"Gambar {screenshot_path} telah dihapus setelah konversi ke PDF.")
    
        print("Semua halaman telah diambil screenshot-nya dan dikonversi ke PDF.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()
