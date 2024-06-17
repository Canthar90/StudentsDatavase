from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Average speed calculator')
        grid = QGridLayout()

        #Create Widgets
        distance_label = QLabel('Traveled Distance:')
        self.distance_line_input = QLineEdit()

        time_label = QLabel('Time(hours):')
        self.time_line_input = QLineEdit()

        self.system_dropdown = QComboBox()
        self.system_dropdown.addItems(['Metric(km)', 'Imperial(miles)'])

        calculate_button = QPushButton('Calculate')
        self.output_label = QLabel()

        # Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_input, 0, 1)
        grid.addWidget(self.system_dropdown, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_input, 1, 1)
        grid.addWidget(calculate_button, 2, 1, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)  

        self.setLayout(grid)


app = QApplication(sys.argv)
distance_calculator = SpeedCalculator()

distance_calculator.show()
sys.exit(app.exec())

