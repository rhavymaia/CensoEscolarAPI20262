import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 2 Handlers
# Terminal
streamHandler = StreamHandler()  # Log messages to console
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Arquivo - Rotação autmática.
fileHandler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
