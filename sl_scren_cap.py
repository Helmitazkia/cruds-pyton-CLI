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

# # Fungsi untuk mengambil screenshot seluruh halaman dengan scrolling
# def capture_entire_page_with_scrolling(driver, save_path):
#     """Capture the entire page as a single screenshot by scrolling."""
#     # Ambil ukuran keseluruhan halaman
#     total_width = driver.execute_script("return document.body.scrollWidth")
#     total_height = driver.execute_script("return document.body.scrollHeight")

#     # Set ukuran jendela browser ke lebar halaman
#     driver.set_window_size(total_width, driver.execute_script("return window.innerHeight"))

#     # Scroll dan ambil screenshot di setiap bagian
#     stitched_image = Image.new('RGB', (total_width, total_height))
#     scroll_height = driver.execute_script("return window.innerHeight")
#     for scroll_offset in range(0, total_height, scroll_height):
#         driver.execute_script(f"window.scrollTo(0, {scroll_offset})")
#         time.sleep(1)  # Tunggu halaman selesai memuat
#         screenshot_path = f"temp_screenshot_{scroll_offset}.png"
#         driver.save_screenshot(screenshot_path)

#         # Tempelkan screenshot ke gambar utama
#         temp_image = Image.open(screenshot_path)
#         stitched_image.paste(temp_image, (0, scroll_offset))
#         os.remove(screenshot_path)

#     # Simpan gambar akhir
#     stitched_image.save(save_path)

# Fungsi untuk mengambil screenshot dari seluruh halaman dengan scrolling
def capture_entire_page_with_scrolling(driver, save_path):
    # Mendapatkan tinggi total halaman web
    total_height = driver.execute_script("return document.body.scrollHeight")
    # Mendapatkan tinggi viewport (area yang terlihat di browser)
    viewport_height = driver.execute_script("return window.innerHeight")

    # Menyimpan screenshot sementara dalam daftar
    stitched_image = []
    # Loop untuk menggulir halaman hingga akhir
    for scroll_position in range(0, total_height, viewport_height):
        # Menggulir ke posisi tertentu
        driver.execute_script(f"window.scrollTo(0, {scroll_position})")
        time.sleep(1)  # Menunggu agar halaman selesai menggulir
        # Menyimpan screenshot dari viewport saat ini
        screenshot_path = f"temp_screenshot_{scroll_position}.png"
        driver.save_screenshot(screenshot_path)
        stitched_image.append(screenshot_path)

    # Menggabungkan semua screenshot secara vertikal
    images = [Image.open(img) for img in stitched_image]  # Membuka semua screenshot sementara
    total_width = images[0].width  # Lebar keseluruhan halaman (semua screenshot memiliki lebar yang sama)
    stitched_height = sum(img.height for img in images)  # Menjumlahkan tinggi semua screenshot
    # Membuat gambar baru untuk menyatukan screenshot
    stitched_image_result = Image.new("RGB", (total_width, stitched_height))
    current_height = 0  # Posisi tinggi awal untuk menyisipkan screenshot

    # Menyisipkan screenshot satu per satu ke gambar baru
    for img in images:
        stitched_image_result.paste(img, (0, current_height))
        current_height += img.height  # Memperbarui posisi tinggi untuk screenshot berikutnya

    # Menyimpan gambar hasil penggabungan
    stitched_image_result.save(save_path)

    # Menghapus screenshot sementara setelah selesai
    for img in stitched_image:
        os.remove(img)

# Fungsi utama
if __name__ == "__main__":
    
    options = Options()

    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")  # Buka browser dalam ukuran penuh
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
