"""
Kode ini digunakan untuk mengonversi data dari file PDF ke file TXT. 
Setiap baris data pada PDF diekstrak, diformat, dan disimpan ke dalam file TXT 
dengan kolom yang dipisahkan oleh spasi. Semua aktivitas dicatat dalam log.
"""

import PyPDF2
import os
from config import setup_logger 


logger = setup_logger(log_folder="logs", log_filename="convert_pdf_to_txt")

def pdf_to_txt(pdf_file_path, txt_file_path):
    try:
        if not os.path.exists(pdf_file_path):
            logger.error(f"File PDF tidak ditemukan: {pdf_file_path}")
            return False

        logger.info(f"Memulai konversi dari PDF ke TXT. File sumber: {pdf_file_path}")
        reader = PyPDF2.PdfReader(pdf_file_path)
        text = ""

        # Ekstraksi teks dari setiap halaman
        for page in reader.pages:
            text += page.extract_text()

        if not text.strip():
            logger.warning(f"Tidak ada teks yang diekstrak dari file PDF: {pdf_file_path}")
            return False

        lines = text.splitlines()
        formatted_lines = []

        # Proses setiap baris data
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 3:
                name = " ".join(parts[:-2])
                email = parts[-2]
                phone = parts[-1]
                formatted_line = f"{name}    {email}    {phone}"
                formatted_lines.append(formatted_line)
            else:
                logger.warning(f"Baris tidak valid ditemukan: {line}")

        if not formatted_lines:
            logger.warning(f"Tidak ada baris data yang valid untuk dikonversi dari file PDF: {pdf_file_path}")
            return False

        logger.info(f"Data berhasil diformat:\n {formatted_lines}")

        # Simpan ke file TXT
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write("\n".join(formatted_lines))
        
        logger.info(f"File TXT berhasil disimpan di: {txt_file_path}")
        
        return True

    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
        return False

if __name__ == "__main__":
    pdf_file_path = "convert_customer.pdf"
    txt_file_path = r"C:\PythonProjects\selesai_convert\convert_customer.txt"

    success = pdf_to_txt(pdf_file_path, txt_file_path)

    if success:
        logger.info("Proses Convert PDF to TXT Sukses.")
    else:
        logger.error("Proses Convert PDF to TXT Gagal.")
