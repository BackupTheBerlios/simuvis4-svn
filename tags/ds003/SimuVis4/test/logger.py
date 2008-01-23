
mainWin.logWin.show()

logger.info("------------- Starting test!")
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")

try:
    x = 1 / 0

except:
    logger.exception("exception test")

