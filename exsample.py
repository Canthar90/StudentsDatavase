from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()


        # Create Widgets
        name_label = QLabel("Name:")
        name_line_edit = QLineEdit()

        date_birth_label = QLabel("Date of birth MM/DD/YYYY:")
        date_birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        output_label = QLabel("")


        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(date_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(output_label, 3, 0, 1, 2)

        self.setLayout(grid)


app = QApplication(sys.argv)
age_calculator = AgeCalculator()

age_calculator.show()
sys.exit(app.exec())