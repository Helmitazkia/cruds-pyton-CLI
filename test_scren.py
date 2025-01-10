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
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        upcoming_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upcoming"))
        )
        upcoming_menu.click()
        
        driver.execute_script("window.scrollTo(0, 150);")
        time.sleep(1)

        movie = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "1 Kakak 7 Ponakan"))
        )
        movie.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        screenshot_path = f"screenshot_{timestamp}.png"
        capture_entire_page_with_scrolling(driver, screenshot_path)

        pdf_path = f"{timestamp}.pdf"
        image = Image.open(screenshot_path)
        pdf = image.convert('RGB')
        pdf.save(pdf_path)

        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        print(f"Screenshot telah dihapus dan PDF telah berhasil disimpan: {pdf_path}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        driver.quit()
