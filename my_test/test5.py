from test6 import my_class
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)

logging.info("This is a info log.")
