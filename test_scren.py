from selenium import webdriver  # Mengimpor pustaka Selenium untuk kontrol browser otomatis.
from selenium.webdriver.common.by import By  # Mengimpor metode untuk menemukan elemen di halaman web.
from selenium.webdriver.support.ui import WebDriverWait  # Untuk menunggu elemen muncul di halaman.
from selenium.webdriver.support import expected_conditions as EC  # Untuk menentukan kondisi penungguan.
from selenium.webdriver.chrome.service import Service  # Mengelola layanan untuk driver Chrome.
from selenium.webdriver.chrome.options import Options  # Mengatur opsi untuk ChromeDriver.
from webdriver_manager.chrome import ChromeDriverManager  # Mengelola pengunduhan ChromeDriver otomatis.
from PIL import Image  # Mengimpor pustaka Pillow untuk manipulasi gambar.
from datetime import datetime  # Mengimpor pustaka untuk mendapatkan waktu saat ini.
import os  # Mengimpor pustaka untuk manipulasi file.
import time  # Mengimpor pustaka untuk penundaan eksekusi program.


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

# Blok utama program
if __name__ == "__main__":
    options = Options()  # Membuat objek opsi untuk ChromeDriver
    options.add_argument("--disable-gpu")  # Menonaktifkan penggunaan GPU
    options.add_argument("--start-maximized")  # Memulai browser dalam mode layar penuh
    options.add_argument("--ignore-certificate-errors")  # Mengabaikan kesalahan sertifikat
    options.add_argument("--disable-web-security")  # Menonaktifkan keamanan web
    options.add_argument("--allow-running-insecure-content")  # Mengizinkan konten yang tidak aman

    # Memulai driver Chrome dengan pengaturan yang ditentukan
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Membuka halaman utama
        driver.get("https://21cineplex.com/")
        # Menunggu hingga elemen 'body' tersedia
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Klik menu "Upcoming"
        upcoming_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upcoming"))
        )
        upcoming_menu.click()
        
        driver.execute_script("window.scrollTo(0, 150);")
        time.sleep(1) 

        # Klik film "1 Imam 2 Makmum"
        movie = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "1 Kakak 7 Ponakan"))
        )
        movie.click()
        # Menunggu hingga elemen 'body' tersedia setelah halaman baru dimuat
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Membuat nama file screenshot dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        screenshot_path = f"screenshot_{timestamp}.png"
        # Mengambil screenshot seluruh halaman
        capture_entire_page_with_scrolling(driver, screenshot_path)

        # Membuat nama file PDF
        pdf_path = f"{timestamp}.pdf"
        # Membuka screenshot sebagai gambar
        image = Image.open(screenshot_path)
        # Mengonversi gambar menjadi PDF
        pdf = image.convert('RGB')
        pdf.save(pdf_path)

        # Menghapus file screenshot setelah dikonversi ke PDF
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        print(f"Screenshot telah dihapus dan PDF telah berhasil disimpan: {pdf_path}")

    except Exception as e:  # Menangkap dan menangani kesalahan yang terjadi
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()  # Menutup browser setelah selesai
