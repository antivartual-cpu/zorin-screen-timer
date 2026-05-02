import subprocess
import sys
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


SETTINGS_SCHEMA = "org.gnome.desktop.session"
SETTINGS_KEY = "idle-delay"

LANGUAGES = {
    "en": {
        "window_title": "Zorin Screen Timer",
        "language_label": "Language / 言語",
        "section_title": "Screen timeout",
        "current_prefix": "Current setting:",
        "unavailable_current": "Current setting: Unavailable",
        "applied": "Applied successfully.",
        "failed": "Failed to apply setting.",
        "refresh": "Refresh",
        "custom": "Custom ({seconds} sec)",
        "durations": {
            1800: "30 min",
            3600: "1 hour",
            7200: "2 hours",
            10800: "3 hours",
            14400: "4 hours",
            18000: "5 hours",
        },
        "current_durations": {
            1800: "30 min",
            3600: "1 hour",
            7200: "2 hours",
            10800: "3 hours",
            14400: "4 hours",
            18000: "5 hours",
        },
    },
    "ja": {
        "window_title": "Zorin Screen Timer",
        "language_label": "Language / 言語",
        "section_title": "画面オフ時間",
        "current_prefix": "現在設定:",
        "unavailable_current": "現在設定: 取得不可",
        "applied": "設定しました。",
        "failed": "設定に失敗しました。",
        "refresh": "再読み込み",
        "custom": "カスタム ({seconds}秒)",
        "durations": {
            1800: "30分",
            3600: "1時間",
            7200: "2時間",
            10800: "3時間",
            14400: "4時間",
            18000: "5時間",
        },
        "current_durations": {
            1800: "30分",
            3600: "1時間",
            7200: "2時間",
            10800: "3時間",
            14400: "4時間",
            18000: "5時間",
        },
    },
}

DURATIONS = (1800, 3600, 7200, 10800, 14400, 18000)


class ZorinScreenTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "en"
        self.current_seconds = None
        self.last_message_key = ""
        self.last_error = ""
        self.duration_buttons = {}

        self.setWindowTitle("Zorin Screen Timer")
        self.setMinimumWidth(420)

        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("日本語", "ja")
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.language_label = QLabel()
        self.language_label.setObjectName("languageLabel")
        self.current_label = QLabel()
        self.current_label.setAlignment(Qt.AlignCenter)
        self.current_label.setObjectName("currentLabel")

        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setObjectName("messageLabel")

        self.error_detail_label = QLabel()
        self.error_detail_label.setWordWrap(True)
        self.error_detail_label.setAlignment(Qt.AlignCenter)
        self.error_detail_label.setObjectName("errorDetailLabel")

        self.refresh_button = QPushButton()
        self.refresh_button.clicked.connect(self.load_current_setting)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        button_layout = QGridLayout()
        button_layout.setSpacing(8)
        for index, seconds in enumerate(DURATIONS):
            button = QPushButton()
            button.setCheckable(True)
            button.setMinimumHeight(42)
            button.clicked.connect(lambda checked=False, value=seconds: self.apply_setting(value))
            self.duration_buttons[seconds] = button
            self.button_group.addButton(button)
            button_layout.addWidget(button, index // 2, index % 2)

        button_box = QGroupBox()
        self.button_box = button_box
        button_box.setLayout(button_layout)

        language_layout = QGridLayout()
        language_layout.addWidget(self.language_label, 0, 0)
        language_layout.addWidget(self.language_combo, 0, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(language_layout)
        main_layout.addWidget(self.current_label)
        main_layout.addWidget(button_box)
        main_layout.addWidget(self.refresh_button)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.error_detail_label)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        container = QWidget()
        container.setObjectName("mainPanel")
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet(
            """
            QWidget#mainPanel {
                background: #ece9d8;
                color: #111111;
                font-family: Tahoma, "MS Shell Dlg 2", Arial, sans-serif;
                font-size: 13px;
            }
            QMainWindow {
                background: #ece9d8;
            }
            QGroupBox {
                border: 1px solid #7f9db9;
                border-radius: 2px;
                margin-top: 10px;
                padding: 12px 8px 8px 8px;
                background: #f5f4ea;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 9px;
                padding: 0 4px;
                color: #0a246a;
                background: #ece9d8;
            }
            QLabel {
                font-size: 13px;
            }
            QLabel#languageLabel {
                color: #1f1f1f;
                font-weight: 700;
            }
            QLabel#currentLabel {
                border: 1px solid #aca899;
                background: #ffffff;
                color: #111111;
                font-size: 16px;
                font-weight: 600;
                padding: 12px;
            }
            QLabel#messageLabel {
                color: #0a5a0a;
                font-weight: 600;
                min-height: 20px;
            }
            QLabel#errorDetailLabel {
                color: #7a0000;
                font-size: 11px;
                min-height: 16px;
            }
            QPushButton {
                border: 1px solid #003c74;
                border-top-color: #ffffff;
                border-left-color: #ffffff;
                border-right-color: #7f9db9;
                border-bottom-color: #7f9db9;
                border-radius: 2px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff,
                    stop: 0.45 #ecebe1,
                    stop: 1 #d6d3c3
                );
                color: #111111;
                font-size: 13px;
                padding: 7px 12px;
            }
            QPushButton:hover {
                border: 1px solid #0a64ad;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff,
                    stop: 1 #dbeafd
                );
            }
            QPushButton:pressed,
            QPushButton:checked {
                border: 2px solid #0a64ad;
                background: #c8ddf8;
                padding-top: 8px;
                padding-left: 13px;
                font-weight: 700;
            }
            QPushButton:checked {
                color: #003c74;
            }
            QComboBox {
                border: 1px solid #7f9db9;
                background: #ffffff;
                color: #111111;
                padding: 5px 8px;
            }
            """
        )

        self.update_texts()
        self.load_current_setting()

    def texts(self):
        return LANGUAGES[self.language]

    def change_language(self):
        self.language = self.language_combo.currentData()
        self.update_texts()

    def update_texts(self):
        texts = self.texts()
        self.setWindowTitle(texts["window_title"])
        self.language_label.setText(texts["language_label"])
        self.button_box.setTitle(texts["section_title"])
        self.refresh_button.setText(texts["refresh"])

        for seconds, button in self.duration_buttons.items():
            button.setText(texts["durations"][seconds])

        self.update_current_label()
        self.update_message_label()
        self.update_selected_button()

    def update_current_label(self):
        texts = self.texts()
        if self.current_seconds is None:
            self.current_label.setText(texts["unavailable_current"])
            return

        duration_text = texts["current_durations"].get(
            self.current_seconds, texts["custom"].format(seconds=self.current_seconds)
        )
        self.current_label.setText(f"{texts['current_prefix']} {duration_text}")

    def update_message_label(self):
        if not self.last_message_key:
            self.message_label.clear()
            self.error_detail_label.clear()
            return

        self.message_label.setText(self.texts()[self.last_message_key])
        self.error_detail_label.setText(self.last_error)

    def update_selected_button(self):
        self.button_group.setExclusive(False)
        for seconds, button in self.duration_buttons.items():
            button.setChecked(seconds == self.current_seconds)
        self.button_group.setExclusive(True)

    def run_gsettings(self, args):
        return subprocess.run(
            ["gsettings", *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def parse_idle_delay(self, value):
        match = re.search(r"\b(\d+)\b", value.strip())
        if not match:
            raise ValueError(f"Could not parse idle-delay value: {value.strip()}")
        return int(match.group(1))

    def load_current_setting(self, keep_message=False):
        result = self.run_gsettings(["get", SETTINGS_SCHEMA, SETTINGS_KEY])
        if result.returncode != 0:
            self.current_seconds = None
            self.last_message_key = "failed"
            self.last_error = self.command_error(result)
            self.update_texts()
            return

        try:
            self.current_seconds = self.parse_idle_delay(result.stdout)
            self.last_error = ""
            if not keep_message:
                self.last_message_key = ""
        except ValueError:
            self.current_seconds = None
            self.last_message_key = "failed"
            self.last_error = self.command_error(result)

        self.update_texts()

    def apply_setting(self, seconds):
        result = self.run_gsettings(
            ["set", SETTINGS_SCHEMA, SETTINGS_KEY, str(seconds)]
        )
        if result.returncode != 0:
            self.last_message_key = "failed"
            self.last_error = self.command_error(result)
            self.update_texts()
            return

        self.last_message_key = "applied"
        self.last_error = ""
        self.load_current_setting(keep_message=True)
        if self.current_seconds is None:
            return

        self.last_message_key = "applied"
        self.last_error = ""
        self.update_texts()

    def command_error(self, result):
        stderr = result.stderr.strip() if result.stderr else ""
        stdout = result.stdout.strip() if result.stdout else ""
        if stderr and stdout:
            return f"{stderr}\n{stdout}"
        return stderr or stdout or f"gsettings exited with code {result.returncode}"


def main():
    app = QApplication(sys.argv)
    window = ZorinScreenTimer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
