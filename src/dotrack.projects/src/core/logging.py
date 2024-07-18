import logging.config
from logging import LogRecord
from pathlib import Path
from typing import Any

from src.core.settings import settings

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message: str, use_color: bool = True) -> str:
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {"WARNING": YELLOW, "INFO": BLUE, "DEBUG": CYAN, "CRITICAL": YELLOW, "ERROR": RED}


class ColoredLogger(logging.Logger):
    FORMAT = (
        "[dotrack.projects][%(levelname)s] %(asctime)s - %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
    )
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name: str):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg: str, use_color: bool = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record: LogRecord):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[dotrack.projects][%(levelname)s] %(asctime)s - %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "rotating_file_handler": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 10,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["rotating_file_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def init_logging() -> None:
    if settings.DEBUG:
        LOGGING_CONFIG["loggers"][""]["handlers"].remove("rotating_file_handler")
    else:
        LOGGING_CONFIG["loggers"]["uvicorn"] = {
            "handlers": ["default", "rotating_file_handler"],
            "level": "INFO",
            "propagate": False,
        }

    logging.config.dictConfig(LOGGING_CONFIG)

    logging.setLoggerClass(ColoredLogger)
