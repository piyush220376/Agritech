import os

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QTextEdit, QLineEdit, QTabWidget, QFileDialog, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QFont

from chat_model import get_response
from voice_model import VoiceThread
from plant_model import PlantAnalysisThread
from prices import build_mp_slug_index, fetch_commodityonline_precise


# ================= THEME =================
WHITE_FG = "#FAFAFA"
LANGUAGE_BTN_BG = "#B19CD9"
SEMI_TRANSPARENT_BG = "rgba(23, 23, 23, 150)"
SEMI_TRANSPARENT_GRAY = "rgba(42, 42, 42, 150)"

BACKGROUND_IMAGE_PATH = r"D:\ai farmer chat bot\ui\image.png"

current_image_path = None


# ================ TRANSLATIONS ================
TRANSLATIONS = {
    "English": {
        "window_title": "AI Farmer Chat Bot",
        "title": "🌾 Smart Farmer AI Assistant",
        "chat_tab": "Chat",
        "plant_tab": "Disease Detection",
        "prices_tab": "Mandi Prices",
        "send": "Send",
        "voice": "Voice",
        "upload_image": "Upload Image",
        "analyze": "Analyze",
        "fetch_prices": "Fetch Prices",
        "chat_input_placeholder": "Type your message...",
        "you": "You",
        "bot": "FarmBot",
    },
    "Hindi": {
        "window_title": "एआई किसान चैट बॉट",
        "title": "🌾 स्मार्ट किसान एआई सहायक",
        "chat_tab": "चैट",
        "plant_tab": "रोग पहचान",
        "prices_tab": "मंडी भाव",
        "send": "भेजें",
        "voice": "वॉइस",
        "upload_image": "छवि अपलोड करें",
        "analyze": "विश्लेषण करें",
        "fetch_prices": "भाव देखें",
        "chat_input_placeholder": "यहाँ लिखें...",
        "you": "आप",
        "bot": "फार्मबॉट",
    },
    "Gujarati": {
        "window_title": "AI ખેડૂત ચેટ બોટ",
        "title": "🌾 સ્માર્ટ ખેડૂત AI સહાયક",
        "chat_tab": "ચેટ",
        "plant_tab": "રોગ ઓળખ",
        "prices_tab": "મંડી ભાવ",
        "send": "મોકલો",
        "voice": "વોઇસ",
        "upload_image": "છબી અપલોડ કરો",
        "analyze": "વિશ્લેષણ",
        "fetch_prices": "ભાવ જુઓ",
        "chat_input_placeholder": "અહીં લખો...",
        "you": "તમે",
        "bot": "ફાર્મબોટ",
    },
    "Telugu": {
        "window_title": "AI రైతు చాట్ బాట్",
        "title": "🌾 స్మార్ట్ రైతు AI సహాయకుడు",
        "chat_tab": "చాట్",
        "plant_tab": "రోగ నిర్ధారణ",
        "prices_tab": "మండి ధరలు",
        "send": "పంపండి",
        "voice": "వాయిస్",
        "upload_image": "చిత్రం అప్లోడ్ చేయి",
        "analyze": "విశ్లేషించు",
        "fetch_prices": "ధరలు చూడండి",
        "chat_input_placeholder": "ఇక్కడ టైప్ చేయండి...",
        "you": "మీరు",
        "bot": "ఫార్మబాట్",
    },
}


# ================= BACKGROUND =================
class TransparentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bg = QPixmap(BACKGROUND_IMAGE_PATH) if os.path.exists(BACKGROUND_IMAGE_PATH) else None

    def paintEvent(self, event):
        if self.bg:
            painter = QPainter(self)
            scaled = self.bg.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)


# ================= LANGUAGE BUTTON =================
class LanguageButton(QPushButton):
    def __init__(self, text, selected=False):
        super().__init__(text)
        self.selected = selected
        self.setFixedSize(70, 35)
        self.setFont(QFont("Arial", 9, QFont.Bold))
        self.update_style()

    def update_style(self):
        if self.selected:
            self.setStyleSheet(f"background:{LANGUAGE_BTN_BG}; color:black; border-radius:15px;")
        else:
            self.setStyleSheet(f"background:{SEMI_TRANSPARENT_GRAY}; color:{WHITE_FG}; border-radius:15px;")

    def set_selected(self, val):
        self.selected = val
        self.update_style()


# ================= MANDI THREAD =================
class MandiThread(QThread):
    prices_ready = pyqtSignal(list)

    def __init__(self, commodity, state, market):
        super().__init__()
        self.commodity = commodity
        self.state = state
        self.market = market

    def run(self):
        rows = fetch_commodityonline_precise(self.commodity, self.state, self.market)
        self.prices_ready.emit(rows)


# ================= CHAT THREAD =================
class ChatThread(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, text, lang):
        super().__init__()
        self.text = text
        self.lang = lang

    def run(self):
        reply = get_response(self.text, self.lang)
        self.response_ready.emit(reply)


# ================= MAIN WINDOW =================
class ChatBot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "English"
        self.language_buttons = {}

        # load mandi dropdown data
        idx = build_mp_slug_index()
        self._mandi_state = idx["state"]["name"]
        self._mandi_markets = list(idx["markets"].values())
        self._mandi_commodities = list(idx["commodities"].values())

        # runtime prefixes (set by update_ui_texts)
        self.you_prefix = "You"
        self.bot_prefix = "FarmBot"

        self.init_ui()

    # ---------- UI SETUP ----------
    def init_ui(self):
        self.setWindowTitle("AI Farmer Chat Bot")
        self.setGeometry(100, 100, 1100, 780)

        self.central_widget = TransparentWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.setup_header(layout)
        self.setup_tabs(layout)
        # apply translations to visible UI
        self.update_ui_texts()

    # ---------- HEADER ----------
    def setup_header(self, layout):
        header = QHBoxLayout()

        self.title_label = QLabel("🌾 Smart Farmer AI Assistant")
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title_label.setStyleSheet(f"color:{WHITE_FG}; background:{SEMI_TRANSPARENT_BG}; padding:15px;")
        header.addWidget(self.title_label)

        header.addStretch()

        for lang in ["English", "Hindi", "Gujarati", "Telugu"]:
            btn = LanguageButton(lang, lang == self.current_language)
            btn.clicked.connect(lambda _, l=lang: self.select_language(l))
            self.language_buttons[lang] = btn
            header.addWidget(btn)

        layout.addLayout(header)

    def setup_tabs(self, layout):
        self.tabs = QTabWidget()
        # larger tab labels for easier tapping
        self.tabs.setStyleSheet(
            "QTabBar::tab { font-size: 14px; min-width: 120px; min-height: 36px; padding: 6px; }"
        )
        self.setup_chat_tab()
        self.setup_plant_tab()
        self.setup_prices_tab()
        layout.addWidget(self.tabs)

    def setup_chat_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        # make the chat area semi-transparent white so background is visible
        self.chat_display.setStyleSheet("background-color: rgba(255,255,255,220); color: black;")
        v.addWidget(self.chat_display)

        h = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.returnPressed.connect(self.send_message)
        self.chat_input.setFixedHeight(34)
        # semi-transparent white input to match chat area
        self.chat_input.setStyleSheet("background-color: rgba(255,255,255,220); color: black; border-radius:4px; padding:4px;")
        h.addWidget(self.chat_input)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        self.send_btn.setFixedHeight(36)
        self.send_btn.setMinimumWidth(90)
        self.send_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        h.addWidget(self.send_btn)

        self.voice_btn = QPushButton("Voice")
        self.voice_btn.clicked.connect(self.listen_voice)
        self.voice_btn.setFixedHeight(36)
        self.voice_btn.setMinimumWidth(90)
        self.voice_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        h.addWidget(self.voice_btn)

        v.addLayout(h)
        self.tabs.addTab(tab, "Chat")

    # ---------- PLANT TAB ----------
    def setup_plant_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)

        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        self.upload_btn.setFixedHeight(40)
        self.upload_btn.setFont(QFont("Segoe UI", 11))
        v.addWidget(self.upload_btn)

        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze_disease)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setFixedHeight(40)
        self.analyze_btn.setFont(QFont("Segoe UI", 11))
        v.addWidget(self.analyze_btn)

        self.plant_results = QTextEdit()
        # semi-transparent white results area (keep current text style)
        self.plant_results.setStyleSheet("background-color: rgba(255,255,255,220); color: black;")
        v.addWidget(self.plant_results)

        self.tabs.addTab(tab, "Disease Detection")

    # ---------- PRICES TAB ----------
    def setup_prices_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)

        # ---- Controls row ----
        h = QHBoxLayout()

        self.commodity_combo = QComboBox()
        self.commodity_combo.addItems(self._mandi_commodities)
        self.commodity_combo.setFixedHeight(36)
        self.commodity_combo.setFont(QFont("Segoe UI", 10))
        h.addWidget(self.commodity_combo)

        self.market_combo = QComboBox()
        self.market_combo.addItems(self._mandi_markets)
        self.market_combo.setFixedHeight(36)
        self.market_combo.setFont(QFont("Segoe UI", 10))
        h.addWidget(self.market_combo)

        self.fetch_btn = QPushButton("Fetch Prices")
        self.fetch_btn.clicked.connect(self.fetch_prices)
        self.fetch_btn.setFixedHeight(36)
        self.fetch_btn.setMinimumWidth(130)
        self.fetch_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        h.addWidget(self.fetch_btn)

        v.addLayout(h)

        # ---- Results area ----
        self.prices_display = QTextEdit()
        self.prices_display.setReadOnly(True)
        self.prices_display.setStyleSheet(
            "background-color: rgba(255,255,255,220); color: black; font-family: Consolas, monospace;"
        )
        v.addWidget(self.prices_display)

        self.tabs.addTab(tab, "Mandi Prices")

    # ---------- CHAT ----------
    def send_message(self):
        text = self.chat_input.text().strip()
        if not text:
            return

        self.chat_display.append(f"{self.you_prefix}: {text}")
        self.chat_input.clear()

        # PASS CURRENT LANGUAGE HERE
        self.thread = ChatThread(text, self.current_language)
        self.thread.response_ready.connect(self.show_response)
        self.thread.start()

    def show_response(self, msg):
        self.chat_display.append(f"{self.bot_prefix}: {msg}")

    # ---------- VOICE ----------
    def listen_voice(self):
        # indicate listening state
        if hasattr(self, 'voice_btn'):
            self.voice_btn.setText("Listening...")
            self.voice_btn.setEnabled(False)

        self.voice_thread = VoiceThread(self.current_language)
        self.voice_thread.voice_recognized.connect(self.voice_result)
        self.voice_thread.voice_error.connect(self.voice_error)
        # ensure we reset button when thread finishes
        self.voice_thread.finished.connect(self.on_voice_finished)
        self.voice_thread.start()

    def voice_result(self, text):
        self.chat_input.setText(text)
        self.send_message()

    def voice_error(self, err):
        self.chat_display.append(err)
        # restore voice button when an error occurs
        self.on_voice_finished()

    def on_voice_finished(self):
        # reset voice button text to localized label
        tr = TRANSLATIONS.get(self.current_language, TRANSLATIONS["English"])
        label = tr.get('voice', 'Voice')
        if hasattr(self, 'voice_btn'):
            self.voice_btn.setText(label)
            self.voice_btn.setEnabled(True)

    # ---------- PLANT ----------
    def upload_image(self):
        global current_image_path
        path, _ = QFileDialog.getOpenFileName(self, "Select image")
        if path:
            current_image_path = path
            self.analyze_btn.setEnabled(True)

    def analyze_disease(self):
        self.thread = PlantAnalysisThread(current_image_path)
        self.thread.analysis_ready.connect(self.plant_results.setText)
        self.thread.start()

    # ---------- PRICES ----------
    def fetch_prices(self):
        commodity = self.commodity_combo.currentText()
        market = self.market_combo.currentText()

        self.prices_display.setPlainText(f"Fetching prices for {commodity} in {market}…")
        self.fetch_btn.setEnabled(False)

        self.mandi_thread = MandiThread(commodity, self._mandi_state, market)
        self.mandi_thread.prices_ready.connect(self._show_prices)
        self.mandi_thread.start()

    def _show_prices(self, rows):
        self.fetch_btn.setEnabled(True)

        if not rows:
            self.prices_display.setPlainText("No data returned.")
            return

        # Error row
        if "error" in rows[0]:
            self.prices_display.setPlainText(f"⚠ {rows[0]['error']}")
            return

        lines = []
        for r in rows:
            lines.append(
                f"📦 {r.get('commodity','-')}  |  🏪 {r.get('market','-')}  |  📅 {r.get('date','-')}\n"
                f"   Min: ₹{r.get('min','-')}   Modal: ₹{r.get('modal','-')}   Max: ₹{r.get('max','-')}"
                + (f"   Grade: {r.get('grade','-')}" if r.get('grade') and r.get('grade') != '-' else "")
            )
        self.prices_display.setPlainText("\n\n".join(lines))

    # ---------- LANGUAGE ----------
    def select_language(self, lang):
        self.current_language = lang
        for name, btn in self.language_buttons.items():
            btn.set_selected(name == lang)
        # update visible UI strings
        self.update_ui_texts()

    def update_ui_texts(self):
        tr = TRANSLATIONS.get(self.current_language, TRANSLATIONS["English"])
        # window and header
        try:
            self.setWindowTitle(tr.get("window_title", "AI Farmer Chat Bot"))
            self.title_label.setText(tr.get("title", self.title_label.text()))
        except Exception:
            pass

        # tabs (chat=0, plant=1, prices=2)
        try:
            if self.tabs.count() > 0:
                self.tabs.setTabText(0, tr.get("chat_tab", "Chat"))
            if self.tabs.count() > 1:
                self.tabs.setTabText(1, tr.get("plant_tab", "Disease Detection"))
            if self.tabs.count() > 2:
                self.tabs.setTabText(2, tr.get("prices_tab", "Mandi Prices"))
        except Exception:
            pass

        # buttons and placeholders
        try:
            if hasattr(self, 'send_btn'):
                self.send_btn.setText(tr.get('send', 'Send'))
            if hasattr(self, 'voice_btn'):
                # only update to the default label if not currently listening
                if getattr(self, 'voice_thread', None) and self.voice_thread.isRunning():
                    # keep Listening... label while running
                    pass
                else:
                    self.voice_btn.setText(tr.get('voice', 'Voice'))
            if hasattr(self, 'upload_btn'):
                self.upload_btn.setText(tr.get('upload_image', 'Upload Image'))
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.setText(tr.get('analyze', 'Analyze'))
            if hasattr(self, 'fetch_btn'):
                self.fetch_btn.setText(tr.get('fetch_prices', 'Fetch Prices'))
            if hasattr(self, 'chat_input'):
                self.chat_input.setPlaceholderText(tr.get('chat_input_placeholder', 'Type your message...'))
        except Exception:
            pass

        # prefixes used in chat messages
        self.you_prefix = tr.get('you', 'You')
        self.bot_prefix = tr.get('bot', 'FarmBot')
