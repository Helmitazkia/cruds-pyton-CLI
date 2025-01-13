import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Fungsi untuk mengatur logger
def setup_logger(log_folder="logs", log_filename="app_log", when="midnight", interval=1, backup_count=7):
    """
    Setup logger with TimedRotatingFileHandler.

    Parameters:
    log_folder (str): Folder untuk menyimpan file log.
    log_filename (str): Nama dasar file log.
    when (str): Kapan file log berotasi (default: 'midnight').
    interval (int): Interval rotasi log (default: 1).
    backup_count (int): Jumlah maksimum file log yang disimpan (default: 7).

    Returns:
    logging.Logger: Objek logger yang sudah diatur.
    """
    # Buat folder log jika belum ada
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

  
    log_file_path = os.path.join(log_folder, f"{log_filename}.log")

    logger = logging.getLogger(log_filename)
    logger.setLevel(logging.DEBUG)  # Set level log (DEBUG, INFO, WARNING, ERROR, CRITICAL)

 
    handler = TimedRotatingFileHandler(log_file_path, when=when, interval=interval, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
