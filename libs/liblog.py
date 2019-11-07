import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('pdfgrab.log')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
console_formatter = logging.Formatter('%(levelname)s:%(message)s')


file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
