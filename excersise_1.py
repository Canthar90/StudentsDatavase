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
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel('')

        # Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_input, 0, 1)
        grid.addWidget(self.system_dropdown, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_input, 1, 1)
        grid.addWidget(calculate_button, 2, 1, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)  

        self.setLayout(grid)

    def calculate_speed(self):
        if self.system_dropdown.currentText() == 'Metric(km)':
            converter = 1
            unit_label = 'km'
        else :
            converter = 1.609
            unit_label = 'mil'

        speed = (int(self.distance_line_input.text()) / int(self.time_line_input.text()))/converter
        
        self.output_label.setText(f"Your speed is : {speed} {unit_label}")
    


app = QApplication(sys.argv)
distance_calculator = SpeedCalculator()

distance_calculator.show()
sys.exit(app.exec())

