import logging
import os
from logging.handlers import RotatingFileHandler

#Criar pasta de logs.
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

#Nome do arquivo de log.
LOG_FILE = os.path.join(LOGS_DIR, "app.log")

#Criação do logger
logger = logging.getLogger("locadora")
logger.setLevel(logging.DEBUG)

#Formato do log
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

#Exibir no terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#File Handler com rotação (até 5 arquivos de 1mb cada)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)