"""
Kode ini digunakan untuk mengonversi data dari file PDF ke file TXT. 
Setiap baris data pada PDF diekstrak, diformat, dan disimpan ke dalam file TXT 
dengan kolom yang dipisahkan oleh spasi.
"""

import PyPDF2

def pdf_to_txt(pdf_file_path, txt_file_path):
    try:
        reader = PyPDF2.PdfReader(pdf_file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        lines = text.splitlines()
        formatted_lines = []

        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 3:
                name = " ".join(parts[:-2])
                email = parts[-2]
                phone = parts[-1]
                formatted_line = f"{name}    {email}    {phone}"
                formatted_lines.append(formatted_line)

        print(formatted_lines)

        with open(txt_file_path, 'w') as txt_file:
            txt_file.write("\n".join(formatted_lines))
        
        print(f"File TXT berhasil disimpan di: {txt_file_path}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

pdf_file_path = "convert_customer.pdf"
txt_file_path = r"C:\PythonProjects\selesai_convert\convert_customer.txt"
pdf_to_txt(pdf_file_path, txt_file_path)
