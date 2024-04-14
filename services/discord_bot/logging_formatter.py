import logging


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):  # noqa: A003
        log_color = self.COLORS[record.levelno]
        formatting = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        formatting = formatting.replace("(black)", self.black + self.bold)
        formatting = formatting.replace("(reset)", self.reset)
        formatting = formatting.replace("(levelcolor)", log_color)
        formatting = formatting.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(formatting, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)
