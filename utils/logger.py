import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

console.setFormatter(formatter)
logger.addHandler(console)  # 将日志输出至屏幕

__all__ = ["logger"]
