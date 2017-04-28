import logging
logging.basicConfig(
        filename='crawler.log',
        format='%(asctime)s %(module)s %(message)s',
        level=logging.INFO)

logger = logging.getLogger()
