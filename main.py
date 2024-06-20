from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Managment app')
        self.setMinimumSize(800, 600)

        # Adding menu bar
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        # Adding actions for menu items
        add_student_action = QAction(QIcon('icons/add.png') ,'Add Student', self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon('icons/search.png') ,'Search', self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)


        # Creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        # Create Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)


        # Create Status bar and its elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)


    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Edit Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    
    def load_data(self):
        connection = DatabaseConnection().connect()
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
        

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About program')

        content = """
        This app was created during the "Python Mega Course" by Dawid Cieślak
        Feel free to use
"""

        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # IM getting current data from main window table 
        self.index = student_managment_main.table.currentRow()
        student_name = student_managment_main.table.item(self.index, 1).text()
        student_course = student_managment_main.table.item(self.index, 2).text()
        student_mobile = student_managment_main.table.item(self.index, 3).text()

        self.student_id = student_managment_main.table.item(self.index, 0).text()

        # Change student name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combobox of available courses
        self.course_name = QComboBox()
        courses = ["Biology", "Mah", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(student_course)
        layout.addWidget(self.course_name)

        # Add Mobile
        self.mobile_number = QLineEdit(student_mobile)
        self.mobile_number.setPlaceholderText("Mobile-nr")
        layout.addWidget(self.mobile_number)

        # Submit button
        submit = QPushButton("Update")
        submit.clicked.connect(self.update_student_record)
        layout.addWidget(submit)

        self.setLayout(layout)


    def update_student_record(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                (self.student_name.text(), 
                self.course_name.itemText(self.course_name.currentIndex()),
                self.mobile_number.text(), self.student_id))
        
        connection.commit()
        
        cursor.close()
        connection.close()
        student_managment_main.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedHeight(120)
        self.setFixedWidth(200)

        layout = QGridLayout()

        confirmation = QLabel('Are you sure you wan to delete?')
        yes = QPushButton('Yes')
        no = QPushButton('No')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.exit_dialog)

    def delete_student(self):
        index = student_managment_main.table.currentRow()
        student_id = student_managment_main.table.item(index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        cursor.execute("DELETE from students WHERE id = ?", (student_id,))

        connection.commit()
        cursor.close()
        connection.close()

        student_managment_main.load_data()  
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText('Record was delited succesfully')
        confirmation_widget.exec()  

    def exit_dialog(self):
        self.close()


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
        courses = ["Biology", "Mah", "Astronomy", "Physics"]
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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)
        # print(rows)
        items = student_managment_main.table.findItems(name, 
                                    Qt.MatchFlag.MatchFixedString)
        for item in items:
            # print(item)
            student_managment_main.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
student_managment_main = MainWindow()

student_managment_main.show()


sys.exit(app.exec())