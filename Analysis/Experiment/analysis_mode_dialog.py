from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from enum import Enum


class AnalysisMode(Enum):
    SAMPLING = 1
    QBER_COMPUTATION = 2
    PLOTTING = 3
    ATTRIBUTE_COMPUTATION = 4
    PREPROCESSED_DISPLAY = 5


class AnalysisModeDialog(QDialog):
    selected_mode = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Analysis Mode")
        self.setGeometry(100, 100, 300, 200)

        main_layout = QVBoxLayout()

        # Create horizontal layouts
        top_layout = QHBoxLayout()
        middle_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Create buttons for each enum option and add them to appropriate layouts
        self.buttons = {}
        buttons = [
            (AnalysisMode.SAMPLING, top_layout),
            (AnalysisMode.QBER_COMPUTATION, top_layout),
            (AnalysisMode.PLOTTING, middle_layout),
            (AnalysisMode.ATTRIBUTE_COMPUTATION, middle_layout),
            (AnalysisMode.PREPROCESSED_DISPLAY, bottom_layout)
        ]

        for mode, layout in buttons:
            button = QPushButton(mode.name.replace("_", " ").title())
            # noinspection ALL
            button.clicked.connect(lambda _, m=mode: self.select_mode(m))
            layout.addWidget(button)
            self.buttons[mode] = button

        # Add horizontal layouts to the main vertical layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def select_mode(self, mode):
        AnalysisModeDialog.selected_mode = mode
        self.accept()


def get_selected_mode():
    app = QApplication([])
    dialog = AnalysisModeDialog()
    dialog.exec()
    return AnalysisModeDialog.selected_mode
