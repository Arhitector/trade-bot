import logging

from config.settings import PAIR as DEFAULT_PAIRPAIR
from config.settings import TRADING_STRATEGY as DEFAULT_TRADING_STRATEGY

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(f"{DEFAULT_PAIRPAIR} {DEFAULT_TRADING_STRATEGY}")
