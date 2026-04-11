from typing import Tuple
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QLineEdit,
    QFileDialog,
)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("game2anki.exe")
        self.resize(1200, 800)

        self._build_ui()

    def _build_ui(self) -> None:
        root_container = QWidget()
        self.setCentralWidget(root_container)

        root_layout = QVBoxLayout(root_container)

        root_layout.addLayout(self._build_title_bar())
        root_layout.addLayout(self._build_top_bar())
        root_layout.addLayout(self._build_middle_section())
        root_layout.addWidget(self._build_card_fields_panel())
        root_layout.addWidget(self._build_card_preview_panel())
        root_layout.addLayout(self._build_bottom_bar())

    def _build_title_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        title = QLabel("game2anki")
        title.setStyleSheet("font-weight: bold; padding: 4px;")

        settings_button = QPushButton("Settings")
        help_button = QPushButton("Help")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(settings_button)
        layout.addWidget(help_button)

        return layout

    def _build_top_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.open_screenshot_button = QPushButton("Open Screenshot")
        self.open_screenshot_button.clicked.connect(self.open_screenshot_action)

        layout.addWidget(self.open_screenshot_button)
        layout.addWidget(QPushButton("Paste"))
        layout.addWidget(QPushButton("Re-run OCR"))
        layout.addWidget(QPushButton("Re-tokenize"))
        layout.addWidget(QPushButton("Save Draft"))
        layout.addStretch()

        return layout

    @Slot()
    def open_screenshot_action(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, # Parent Window (MainWindow)
            "Open Screenshot", # Dialog title
            "", # Starting folder/path (TODO: Let this be set in Settings)
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)" # Allowed file types
        )

        if not file_path:
            return

        print(file_path)

    def _build_middle_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        screenshot_panel = self._build_screenshot_panel()
        ocr_panel = self._build_ocr_sentence_panel()

        layout.addWidget(screenshot_panel, 1)
        layout.addWidget(ocr_panel, 1)

        return layout

    def _build_screenshot_panel(self) -> QWidget:
        panel, layout = self._create_panel("SCREENSHOT PANEL")

        screenshot_box = QFrame()
        screenshot_box.setFrameShape(QFrame.Shape.Box)
        screenshot_box.setMinimumHeight(260)

        screenshot_layout = QVBoxLayout(screenshot_box)

        screenshot_label = QLabel("screenshot")
        screenshot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        screenshot_layout.addStretch()
        screenshot_layout.addWidget(screenshot_label)
        screenshot_layout.addStretch()

        layout.addWidget(screenshot_box)

        return panel

    def _build_ocr_sentence_panel(self) -> QWidget:
        panel, layout = self._create_panel("OCR / SENTENCE PANEL")

        sentence_label = QLabel("Sentence (editable):")
        sentence_input = QTextEdit()
        sentence_input.setPlainText("これから ぼうけんが はじまる！")
        sentence_input.setMaximumHeight(90)

        tokens_label = QLabel("Token candidates:")
        tokens_row = self._build_token_row()

        selected_token_label = QLabel("Selected token: ぼうけん")

        layout.addWidget(sentence_label)
        layout.addWidget(sentence_input)
        layout.addWidget(tokens_label)
        layout.addLayout(tokens_row)
        layout.addWidget(selected_token_label)
        layout.addStretch()

        return panel

    def _build_token_row(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        for token in ["これから", "ぼうけん", "が", "はじまる"]:
            button = QPushButton(token)
            layout.addWidget(button)

        layout.addStretch()
        return layout

    def _build_card_fields_panel(self) -> QWidget:
        panel, layout = self._create_panel("ENRICHMENT / CARD FIELDS")

        form_layout = QGridLayout()

        expression_label = QLabel("Expression:")
        expression_input = QLineEdit("冒険")

        reading_label = QLabel("Reading:")
        reading_input = QLineEdit("ぼうけん")

        meaning_label = QLabel("Meaning:")
        meaning_input = QLineEdit("adventure")

        source_label = QLabel("Source:")
        source_input = QLineEdit("Pokemon")

        tags_label = QLabel("Tags:")
        tags_input = QLineEdit("pokemon, game-mining, vocab")

        sentence_label = QLabel("Sentence:")
        sentence_input = QLineEdit("これから ぼうけんが はじまる！")

        form_layout.addWidget(expression_label, 0, 0)
        form_layout.addWidget(expression_input, 0, 1)
        form_layout.addWidget(reading_label, 0, 2)
        form_layout.addWidget(reading_input, 0, 3)

        form_layout.addWidget(meaning_label, 1, 0)
        form_layout.addWidget(meaning_input, 1, 1, 1, 3)

        form_layout.addWidget(source_label, 2, 0)
        form_layout.addWidget(source_input, 2, 1, 1, 3)

        form_layout.addWidget(tags_label, 3, 0)
        form_layout.addWidget(tags_input, 3, 1, 1, 3)

        form_layout.addWidget(sentence_label, 4, 0)
        form_layout.addWidget(sentence_input, 4, 1, 1, 3)

        layout.addLayout(form_layout)

        return panel

    def _build_card_preview_panel(self) -> QWidget:
        panel, layout = self._create_panel("CARD PREVIEW")

        front_label = QLabel("Front: 冒険")
        back_label = QLabel("Back: ぼうけん / adventure")
        context_label = QLabel("Context: これから ぼうけんが はじまる！")

        layout.addWidget(front_label)
        layout.addWidget(back_label)
        layout.addWidget(context_label)

        return panel

    def _build_bottom_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        layout.addWidget(QPushButton("Add to Anki"))
        layout.addWidget(QPushButton("Skip"))
        layout.addWidget(QPushButton("Clear"))
        layout.addStretch()

        return layout

    def _create_panel(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.Box)

        layout = QVBoxLayout(panel)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")

        layout.addWidget(title_label)

        return panel, layout
