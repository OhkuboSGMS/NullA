import logging
from PyInstaller.utils.hooks import collect_data_files
logging.info('Adding mediapipe datas')
datas = collect_data_files('mediapipe')
