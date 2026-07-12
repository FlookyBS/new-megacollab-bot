import logging

if __name__ == "__main__":
    exit()

class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    BOLD = "\033[1m"

    LEVEL_STYLES = {
        "WARNING": ("\033[33m", False),        # yellow
        "ERROR": ("\033[31m", False),          # red
        "CRITICAL": ("\033[31m", True),        # bold red
    }

    def format(self, record):
        original_levelname = record.levelname
        original_msg = record.msg

        style = self.LEVEL_STYLES.get(original_levelname)

        if style:
            color, bold_message = style

            # Style the [LEVEL]
            record.levelname = (
                f"{self.BOLD}{color}{original_levelname}{self.RESET}"
            )

            # Style the message (no bold unless specified)
            if bold_message:
                record.msg = f"{self.BOLD}{color}{original_msg}{self.RESET}"
            else:
                record.msg = f"{color}{original_msg}{self.RESET}"

        message = super().format(record)

        # Restore to avoid side effects
        record.levelname = original_levelname
        record.msg = original_msg

        return message

handler = logging.StreamHandler()
handler.setFormatter(
    ColorFormatter("[%(levelname)s] %(message)s")
)

logging.basicConfig(
    level=logging.INFO,  # minimum level shown
    handlers=[handler],
)

logger = logging.getLogger(__name__)