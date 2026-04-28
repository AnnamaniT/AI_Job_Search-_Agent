# logger.py ################################
import config

def debug(msg: str):
    if config.PRINT_DEBUG_LOGS:
        print(msg)