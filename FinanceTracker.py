import sys
from Classes import *
import datetime
import numpy as np
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QMessageBox, QScrollBar, QDialog, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import hashlib as hlib
import seaborn as sns


class FinanceTrackerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.expenses = []
        self.credits = []

        self.init_gui()

    def init_gui(self):
        #######################################
        #Main window styling
        self.setFixedSize(680,980)
        self.setStyleSheet("background-color: #8FBC8F")
        self.setWindowTitle('Finance Tracker App')
        self.setWindowIcon(QIcon('money_icon.png'))

        #######################################
        # Banner styling
        self.title_label = QLabel('Finance Tracker')
        self.title_label.setStyleSheet('font-family: sans-serif; font-size: 40px; font-weight: bold; margin-bottom: 5px; margin-top: 5px; color: #043927')
        self.bar_description = QLabel('This is an app to track your finances.\nYou can manage your current expenses \nand your various income sources.')
        self.bar_description.setStyleSheet("font-family: sans-serif; font-size: 16px; margin-top: 3px; margin-bottom: 5px; color: #043927")

        ####################################
        #self.currency_label = QLabel("Choose your currency: ")
        #self.currencies = QComboBox()
        ########################################
        #Expense widgets
        self.expense_label = QLabel('Expense:')
        self.expense_label.setStyleSheet('font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927')

        self.expense_input = QLineEdit()
        self.expense_input.setStyleSheet("background-color: #F5F5DC;")

        self.category_label = QLabel('Category:')
        self.category_label.setStyleSheet("font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927")
        self.expense_category_combobox = QComboBox()
        self.expense_category_combobox.setStyleSheet("background-color: #F5F5DC; font-size: 16px; color: #043927")
        self.expense_category_combobox.setFixedSize(200,30)
        self.expense_category_combobox.addItems(['Food', 'Entertainment', 'Bills', 'Travel', 'Shopping', 'Other'])

        self.add_expense_button = QPushButton('Add Expense')
        self.add_expense_button.setFixedSize(200,25)
        self.add_expense_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 16px; color: #043927")

        self.delete_expense_button = QPushButton('Delete Expense')
        self.delete_expense_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 16px; color: #043927")
        self.delete_expense_button.setFixedSize(200, 25)

        self.expense_list = QListWidget()
        self.expense_list.setStyleSheet("background-color: #F5F5DC;")

        ########################################
        #Credit widgets
        self.credit_label = QLabel('Credit:')
        self.credit_label.setStyleSheet('font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927')

        self.credit_input = QLineEdit()
        self.credit_input.setStyleSheet("background-color: #F5F5DC;")

        self.category2_label = QLabel('Category:')
        self.category2_label.setStyleSheet('font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927')

        self.credit_category_combobox = QComboBox()
        self.credit_category_combobox.setStyleSheet("background-color: #F5F5DC; font-size: 16px; color: #043927")
        self.credit_category_combobox.setFixedSize(200,30)
        self.credit_category_combobox.addItems(['Salary', 'Gift', 'Investments', 'Other'])

        self.add_credit_button = QPushButton('Add Credit')
        self.add_credit_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 16px; color: #043927")
        self.add_credit_button.setFixedSize(200,25)

        self.delete_credit_button = QPushButton('Delete Credit')
        self.delete_credit_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 16px; color: #043927")
        self.delete_credit_button.setFixedSize(200,25)

        self.credit_list = QListWidget()
        self.credit_list.setStyleSheet("background-color: #F5F5DC;")

        #######################################
        # Balance counter
        self.calculate_balance_button = QPushButton('Calculate Balance')
        self.balance_sum = QLabel(" ")
        self.balance_sum.setStyleSheet("font-size: 17px; font-family: sans-serif; font-color: #043927")
        self.calculate_balance_button.setFixedSize(250,35)
        self.calculate_balance_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927")

        #######################################
        # Plot styling
        self.chart_type_label = QLabel('Select Chart Type:')
        self.chart_type_label.setStyleSheet('font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927')

        self.chart_type_combobox = QComboBox()
        self.chart_type_combobox.setStyleSheet("background-color: #F5F5DC; font-family: sans-serif; font-size: 16px; color: #043927")
        self.chart_type_combobox.setFixedSize(200,30)
        self.chart_type_combobox.addItems(['Bar Chart', 'Pie Chart'])

        self.plot_chart_button = QPushButton('Plot Chart')
        self.plot_chart_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927")
        self.plot_chart_button.setFixedSize(200, 35)
        self.figure, self.ax = plt.subplots()
        self.chart_canvas = FigureCanvas(self.figure)

        #######################################
        # Operations on files
        self.save_button = QPushButton('Save Data')
        self.save_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927")
        self.save_button.setFixedSize(200, 50)

        self.load_button = QPushButton('Load Data')
        self.load_button.setStyleSheet("background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #043927")
        self.load_button.setFixedSize(200, 50)

        self.setup_layout()
        self.setup_connections()

    def setup_layout(self):
        main_layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label, alignment = Qt.AlignTop | Qt.AlignLeft)
        title_layout.addWidget(self.bar_description, alignment = Qt.AlignTop)

        expense_layout = QHBoxLayout()
        expense_layout.addWidget(self.expense_label)
        expense_layout.addWidget(self.expense_input)
        expense_layout.addWidget(self.category_label)
        expense_layout.addWidget(self.expense_category_combobox)

        expense_buttons_layout = QHBoxLayout()
        expense_buttons_layout.addWidget(self.add_expense_button, alignment=Qt.AlignLeft)
        expense_buttons_layout.addWidget(self.delete_expense_button, alignment=Qt.AlignRight)

        expense_layout_list = QVBoxLayout()
        expense_layout_list.addWidget(self.expense_list)

        credit_layout = QHBoxLayout()
        credit_layout.addWidget(self.credit_label)
        credit_layout.addWidget(self.credit_input)
        credit_layout.addWidget(self.category2_label)
        credit_layout.addWidget(self.credit_category_combobox)

        credit_buttons_layout = QHBoxLayout()
        credit_buttons_layout.addWidget(self.add_credit_button, alignment=Qt.AlignLeft)
        credit_buttons_layout.addWidget(self.delete_credit_button, alignment=Qt.AlignRight)

        credit_layout_list = QVBoxLayout()
        credit_layout_list.addWidget(self.credit_list)

        balance_layout = QHBoxLayout()
        balance_layout.addWidget(self.calculate_balance_button)
        balance_layout.addWidget(self.balance_sum)

        chart_layout = QHBoxLayout()
        chart_layout.addWidget(self.chart_type_label)
        chart_layout.addWidget(self.chart_type_combobox)
        chart_layout.addWidget(self.plot_chart_button)

        chart_plot_layout = QVBoxLayout()
        chart_plot_layout.addWidget(self.chart_canvas)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(expense_layout)
        main_layout.addLayout(expense_buttons_layout)
        main_layout.addLayout(expense_layout_list)
        main_layout.addLayout(credit_layout)
        main_layout.addLayout(credit_layout_list)
        main_layout.addLayout(credit_buttons_layout)
        main_layout.addLayout(balance_layout)
        main_layout.addLayout(chart_layout)
        main_layout.addLayout(chart_plot_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_connections(self):
        self.add_expense_button.clicked.connect(self.add_expense)
        self.delete_expense_button.clicked.connect(self.delete_expense)
        self.add_credit_button.clicked.connect(self.add_credit)
        self.delete_credit_button.clicked.connect(self.delete_credit)
        self.calculate_balance_button.clicked.connect(self.calculate_balance)
        self.plot_chart_button.clicked.connect(self.plot_chart)
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)

    def add_expense(self):
        expense_text = self.expense_input.text()
        category = self.expense_category_combobox.currentText()
        if not expense_text.isalpha():
            expense = Expense(float(expense_text), category)
            self.expenses.append(expense)
            self.update_lists()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Incorrect input!")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec()
            self.expense_input.clear()

    def delete_expense(self):
        selected_row = self.expense_list.currentRow()
        if selected_row != -1:
            del self.expenses[selected_row]
            self.update_lists()

    def add_credit(self):
        credit_text = self.credit_input.text()
        category = self.credit_category_combobox.currentText()
        if not credit_text.isalpha():
            credit = Credit(float(credit_text), category)
            self.credits.append(credit)
            self.update_lists()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Incorrect input!")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec()
            self.expense_input.clear()

    def delete_credit(self):
        selected_row = self.credit_list.currentRow()
        if selected_row != -1:
            del self.credits[selected_row]
            self.update_lists()

    def calculate_balance(self):
        total_expenses = sum(expense.amount for expense in self.expenses)
        total_credits = sum(credit.amount for credit in self.credits)
        balance = total_credits - total_expenses
        self.balance_sum.setText(f'Your current balance: {balance:.2f}')

    def plot_chart(self):
        chart_type = self.chart_type_combobox.currentText()

        if len(self.expenses) != 0 or len(self.credits) != 0:
            if chart_type == 'Bar Chart':
                self.plot_bar_chart()
            elif chart_type == 'Pie Chart':
                self.plot_pie_chart()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("There are no expenses or credits!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec()
            self.expense_input.clear()

    def plot_bar_chart(self):
        plt.clf()

        all_transactions = self.expenses + self.credits
        categories_dict = {}
        colors_dict = {}
        for transaction in all_transactions:
            category = transaction.category
            amount = transaction.amount
            if category in categories_dict:
                categories_dict[category] += amount
            else:
                categories_dict[category] = amount
                if isinstance(transaction, Expense):
                    colors_dict[category] = '#E9967A'
                elif isinstance(transaction, Credit):
                    colors_dict[category] = '#8FBC8F'

        categories = list(categories_dict.keys())
        amounts = list(categories_dict.values())

        colors = [colors_dict[category] for category in categories]
        plt.bar(categories, amounts, color=colors)
        plt.ylabel('Amount')
        title_font = {'family': 'sans-serif', 'color': '#2E8B57', 'weight': 'bold', 'size': 16}
        plt.title('Expenses and Credits by Category', fontdict=title_font)
        self.chart_canvas.draw_idle()
        self.chart_canvas.flush_events()

    def plot_pie_chart(self):
        plt.clf()
        all_transactions = self.expenses + self.credits

        categories_dict = {}
        for transaction in all_transactions:
            category = transaction.category
            amount = transaction.amount
            if category in categories_dict:
                categories_dict[category] += amount
            else:
                categories_dict[category] = amount

        categories = list(categories_dict.keys())
        amounts = list(categories_dict.values())

        colors = sns.color_palette("viridis")[0:len(categories)]

        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, labeldistance=1.2, shadow=True, colors=colors, radius=0.9)
        plt.axis('equal')
        plt.legend(title='Categories', loc="lower right")
        self.chart_canvas.figure.canvas.draw_idle()

    def update_lists(self):
        self.expense_list.clear()
        self.credit_list.clear()

        self.expense_list.addItems([str(expense) for expense in self.expenses])
        self.credit_list.addItems([str(credit) for credit in self.credits])

    def save_data(self):
        default_filename = datetime.datetime.now().strftime("%d.%m.%Y") + "_data.xml"
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Data', default_filename, 'XML Files (*.xml);;All Files (*)')
        if filename:
            root = ET.Element('data')
            expenses_element = ET.SubElement(root, 'expenses')
            for expense in self.expenses:
                expense_element = ET.SubElement(expenses_element, 'expense')
                Eamount_element = ET.SubElement(expense_element, 'amount')
                Eamount_element.text = str(expense.amount)
                Ecategory_element = ET.SubElement(expense_element, 'category')
                Ecategory_element.text = expense.category

            credits_element = ET.SubElement(root, 'credits')
            for credit in self.credits:
                credit_element = ET.SubElement(credits_element, 'credit')
                Camount_element = ET.SubElement(credit_element, 'amount')
                Camount_element.text = str(credit.amount)
                Ccategory_element = ET.SubElement(credit_element, 'category')
                Ccategory_element.text = credit.category

            tree = ET.ElementTree(root)
            tree.write(filename)

            msg = QMessageBox()
            msg.setWindowTitle("Save data")
            msg.setWindowIcon(QIcon("money_icon.png"))
            msg.setText("Your data has been saved!")
            msg.setStyleSheet("""
                       QMessageBox {
                           background-color: #8FBC8F;
                           border: 1px solid #707070;
                       }
                       QMessageBox QLabel {
                           color: #043927; font-family: sans-serif; font-size: 18px; 
                           padding-right:20px;
                           padding-top: 10px;
                           font-weight: bold;
                       }
                       QMessageBox QPushButton {
                           background-color: #F5F5DC; border-radius: 10px; font-family: sans-serif; font-size: 18px; 
                           font-weight: bold; color: #043927;
                           min-width: 100px; min-height: 30px;}
                   """)

            x = msg.exec()
            self.expense_input.clear()

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Load Data', '', 'XML Files (*.xml);;All Files (*)')
        if filename:
            try:
                tree = ET.parse(filename)
                root = tree.getroot()

                self.expenses = [Expense(float(expense.find('amount').text), expense.find('category').text) for expense in
                             root.find('expenses')]
                self.credits = [Credit(float(credit.find('amount').text), credit.find('category').text) for credit in
                             root.find('credits')]

                self.update_lists()
                self.calculate_balance()
            except Exception as e:
                error_message = f"Error loading data from file"
                QMessageBox.critical(self, 'Error', error_message)