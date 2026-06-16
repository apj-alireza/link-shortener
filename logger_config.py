import os
import logging

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("shortener_project")
handler = logging.FileHandler("logs/app.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
