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
    QMessageBox,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap

from app.core.ocr_service import OCRService
from app.core.text_normalizer import normalize_for_display
from app.core.tokenization import KanjiCandidate, Token, TokenizationService
from app.integrations.dictionary.jisho_client import JishoDictionaryClient


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("game2anki.exe")
        self.resize(1200, 800)

        self.ocr_service = OCRService()
        self.tokenization_service = TokenizationService(JishoDictionaryClient())
        self.current_pixmap_path = None
        self.current_tokens: list[Token] = []
        self.selected_token: Token | None = None
        self.selected_candidate: KanjiCandidate | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        root_container = QWidget()
        root_scroll = QScrollArea()
        root_scroll.setWidgetResizable(True)
        root_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root_scroll.setWidget(root_container)
        self.setCentralWidget(root_scroll)

        root_layout = QVBoxLayout(root_container)

        root_layout.addLayout(self._build_title_bar())
        root_layout.addLayout(self._build_top_bar())
        root_layout.addLayout(self._build_middle_section())
        root_layout.addWidget(self._build_kanji_candidates_panel())
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

        self.rerun_ocr_button = QPushButton("Re-run OCR")
        self.rerun_ocr_button.clicked.connect(self.run_ocr_action)

        self.retokenize_button = QPushButton("Re-tokenize")
        self.retokenize_button.clicked.connect(self.run_tokenization_action)

        layout.addWidget(self.open_screenshot_button)
        layout.addWidget(QPushButton("Paste"))
        layout.addWidget(self.rerun_ocr_button)
        layout.addWidget(self.retokenize_button)
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
            self.current_pixmap_path = ""

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            print("Failed to load image.")
            return

        self.current_pixmap = pixmap
        self.current_pixmap_path = file_path
        self.scale_screenshot_image()

    @Slot()
    def scale_screenshot_image(self) -> None:
        if not hasattr(self, "current_pixmap"):
            return

        if self.current_pixmap.isNull():
            return

        scaled_pixmap = self.current_pixmap.scaled(
            self.screenshot_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.screenshot_label.setPixmap(scaled_pixmap)

    @Slot()
    def run_ocr_action(self) -> None:
        if not self.current_pixmap_path:
            QMessageBox.warning(
                self,
                "OCR Error",
                "No screenshot selected"
            )
            return

        try:
            extracted_text = self.ocr_service._extract_text(self.current_pixmap_path)

        except Exception as e:
            QMessageBox.critical(
                self,
                "OCR Error",
                f"OCR failed: {e}"
            )
            return

        if not extracted_text:
            QMessageBox.information(
                self,
                "OCR Result",
                "OCR returned no text."
            )
            return

        normalized_text = normalize_for_display(extracted_text)
        self.sentence_input.setPlainText(normalized_text)

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
        screenshot_box.setMinimumHeight(300)
        screenshot_box.setMinimumWidth(500)

        screenshot_layout = QVBoxLayout(screenshot_box)

        self.screenshot_label = QLabel("screenshot")
        self.screenshot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        screenshot_layout.addWidget(self.screenshot_label)

        layout.addWidget(screenshot_box)

        return panel

    def _build_ocr_sentence_panel(self) -> QWidget:
        panel, layout = self._create_panel("OCR / SENTENCE PANEL")

        sentence_label = QLabel("Sentence (editable):")
        self.sentence_input = QTextEdit()
        self.sentence_input.setPlaceholderText(
            "OCR result will appear here. You can edit the text after OCR runs."
            )
        self.sentence_input.setStyleSheet("font-size: 20px;")
        self.sentence_input.setMaximumHeight(90)

        layout.addWidget(sentence_label)
        layout.addWidget(self.sentence_input)

        self.token_status_label = QLabel("Review or edit the OCR sentence, then click Re-tokenize.")
        self.selected_token_label = QLabel("Selected token: none")

        tokens_label = QLabel("Tokens:")
        self.tokens_container = QWidget()
        self.tokens_grid = QGridLayout(self.tokens_container)
        self.tokens_grid.setContentsMargins(0, 0, 0, 0)
        self.tokens_grid.setSpacing(6)

        layout.addWidget(self.token_status_label)
        layout.addWidget(tokens_label)
        layout.addWidget(self.tokens_container)
        layout.addWidget(self.selected_token_label)
        layout.addStretch()

        return panel

    def _build_kanji_candidates_panel(self) -> QWidget:
        panel, layout = self._create_panel("KANJI CANDIDATES")

        self.selected_candidate_label = QLabel("Selected candidate: none")
        self.candidates_container = QWidget()
        self.candidates_layout = QHBoxLayout(self.candidates_container)
        self.candidates_layout.setContentsMargins(0, 0, 0, 0)
        self.candidates_layout.setSpacing(8)

        candidates_scroll = QScrollArea()
        candidates_scroll.setWidgetResizable(True)
        candidates_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        candidates_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        candidates_scroll.setFrameShape(QFrame.Shape.NoFrame)
        candidates_scroll.setMinimumHeight(96)
        candidates_scroll.setWidget(self.candidates_container)

        layout.addWidget(candidates_scroll)
        layout.addWidget(self.selected_candidate_label)

        return panel

    @Slot()
    def run_tokenization_action(self) -> None:
        sentence = self.sentence_input.toPlainText()
        self.current_tokens = self.tokenization_service.tokenize(sentence)
        self.selected_token = None
        self.selected_candidate = None

        self._render_tokens()
        self._clear_layout(self.candidates_layout)
        self._render_token_selection()

        if not sentence.strip():
            self.token_status_label.setText("No sentence to tokenize.")
            return

        if not self.current_tokens:
            self.token_status_label.setText("No tokens found.")
            return

        self.token_status_label.setText(f"Found {len(self.current_tokens)} tokens.")

    def _render_tokens(self) -> None:
        self._clear_layout(self.tokens_grid)

        for index, token in enumerate(self.current_tokens):
            button = QPushButton(token.surface)
            button.setEnabled(token.selectable)
            button.clicked.connect(lambda checked=False, selected=token: self.select_token(selected))
            button.setStyleSheet(self._token_button_style(token))
            self.tokens_grid.addWidget(button, index // 6, index % 6)

    @Slot()
    def select_token(self, token: Token) -> None:
        self.selected_token = token
        self.selected_candidate = None

        self._render_tokens()
        self._render_token_selection()
        self._clear_layout(self.candidates_layout)

        self.token_status_label.setText(f"Looking up candidates for {token.surface}...")
        candidates = self.tokenization_service.get_candidates(token)

        if candidates:
            self.token_status_label.setText(f"Found {len(candidates)} candidates for {token.surface}.")
        elif self.tokenization_service.last_error:
            self.token_status_label.setText(self.tokenization_service.last_error)
        else:
            self.token_status_label.setText(f"No candidates found for {token.surface}.")

        self._render_candidates(candidates)

    def _render_candidates(self, candidates: list[KanjiCandidate]) -> None:
        self._clear_layout(self.candidates_layout)

        for candidate in candidates:
            button = QPushButton(self._candidate_button_text(candidate))
            button.setMinimumSize(220, 76)
            button.setMaximumWidth(280)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.clicked.connect(
                lambda checked=False, selected=candidate: self.select_candidate(selected)
            )
            button.setStyleSheet(self._candidate_button_style(candidate))
            self.candidates_layout.addWidget(button)

        self.candidates_layout.addStretch()

    @Slot()
    def select_candidate(self, candidate: KanjiCandidate) -> None:
        self.selected_candidate = candidate
        candidates = self.tokenization_service.get_candidates(self.selected_token) if self.selected_token else []
        self._render_candidates(candidates)
        self._render_token_selection()
        self._populate_card_fields(candidate)

    def _render_token_selection(self) -> None:
        token_text = self.selected_token.surface if self.selected_token else "none"
        self.selected_token_label.setText(f"Selected token: {token_text}")

        if self.selected_candidate:
            meaning = self._candidate_meaning_text(self.selected_candidate)
            self.selected_candidate_label.setText(
                f"Selected candidate: {self.selected_candidate.expression} "
                f"({self.selected_candidate.reading}) - {meaning}"
            )
        else:
            self.selected_candidate_label.setText("Selected candidate: none")

    def _token_button_style(self, token: Token) -> str:
        if token == self.selected_token:
            return "font-weight: bold; background-color: #d8ecff; color: #000000;"
        return ""

    def _candidate_button_style(self, candidate: KanjiCandidate) -> str:
        if candidate == self.selected_candidate:
            return (
                "font-weight: bold; background-color: #dff3df; color: #000000; "
                "text-align: left; padding: 8px;"
            )
        return "text-align: left; padding: 8px;"

    def _candidate_button_text(self, candidate: KanjiCandidate) -> str:
        common_marker = "common" if candidate.is_common else "dictionary"
        meaning = self._candidate_meaning_text(candidate)
        return f"{candidate.expression}  [{candidate.reading}]  {common_marker}\n{meaning}"

    def _candidate_meaning_text(self, candidate: KanjiCandidate) -> str:
        if not candidate.meanings:
            return "No English definition listed"
        return "; ".join(candidate.meanings)

    def _build_card_fields_panel(self) -> QWidget:
        panel, layout = self._create_panel("ENRICHMENT / CARD FIELDS")

        form_layout = QGridLayout()

        expression_label = QLabel("Expression:")
        self.expression_input = QLineEdit()

        reading_label = QLabel("Reading:")
        self.reading_input = QLineEdit()

        meaning_label = QLabel("Meaning:")
        self.meaning_input = QLineEdit()

        source_label = QLabel("Source:")
        self.source_input = QLineEdit()

        tags_label = QLabel("Tags:")
        self.tags_input = QLineEdit()

        sentence_label = QLabel("Sentence:")
        self.card_sentence_input = QLineEdit()

        form_layout.addWidget(expression_label, 0, 0)
        form_layout.addWidget(self.expression_input, 0, 1)
        form_layout.addWidget(reading_label, 0, 2)
        form_layout.addWidget(self.reading_input, 0, 3)

        form_layout.addWidget(meaning_label, 1, 0)
        form_layout.addWidget(self.meaning_input, 1, 1, 1, 3)

        form_layout.addWidget(source_label, 2, 0)
        form_layout.addWidget(self.source_input, 2, 1, 1, 3)

        form_layout.addWidget(tags_label, 3, 0)
        form_layout.addWidget(self.tags_input, 3, 1, 1, 3)

        form_layout.addWidget(sentence_label, 4, 0)
        form_layout.addWidget(self.card_sentence_input, 4, 1, 1, 3)

        layout.addLayout(form_layout)

        return panel

    def _populate_card_fields(self, candidate: KanjiCandidate) -> None:
        self.expression_input.setText(candidate.expression)
        self.reading_input.setText(candidate.reading)
        self.meaning_input.setText(self._candidate_meaning_text(candidate))
        self.card_sentence_input.setText(self.sentence_input.toPlainText())

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

    def _clear_layout(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)
