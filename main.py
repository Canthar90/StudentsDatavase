from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Managment app')

        # Adding menu bar
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        # Adding actions for menu items
        add_student_action = QAction('Add Student', self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction('Search', self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)


        # Creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

    
    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    
    def search(self):
        search = SearchDialog()
        search.exec()
        


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add New Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        
        # Add sutdent name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Combobox of courses
        self.course_name = QComboBox()
        courses = ["Bioloty", "Mah", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
       name = self.student_name.text()
       course = self.course_name.itemText(self.course_name.currentIndex())
       mobile = self.mobile.text()
       connect = sqlite3.connect('database.db')
       cursor = connect.cursor()
       cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", 
                      (name, course, mobile))
       connect.commit()
       cursor.close()
       connect.close()
       student_managment_main.load_data()
    

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search for the student")
        self.setFixedHeight(200)
        self.setFixedWidth(200)

        layout = QVBoxLayout()

        # Name input
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText('Name')
        layout.addWidget(self.search_name)

        # search button
        search = QPushButton("Search")
        search.clicked.connect(self.search_student)
        layout.addWidget(search)


        self.setLayout(layout)

    def search_student(self):
        name = self.search_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)
        # print(rows)
        items = student_managment_main.table.findItems(name, 
                                    Qt.MatchFlag.MatchFixedString)
        for item in items:
            # print(item)
            student_managment_main.table.item(item.row(), 1).setSelected(True)


app = QApplication(sys.argv)
student_managment_main = MainWindow()

student_managment_main.show()


sys.exit(app.exec())