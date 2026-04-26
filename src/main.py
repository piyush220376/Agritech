import sys
import os
from PyQt5.QtWidgets import QApplication
from ui import ChatBot


def _load_dotenv():
    """Load .env from the project root (next to this file or one level up)."""
    for candidate in [
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
    ]:
        path = os.path.abspath(candidate)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip())
            break


if __name__ == "__main__":
    _load_dotenv()
    app = QApplication(sys.argv)
    window = ChatBot()
    window.show()
    sys.exit(app.exec_())
