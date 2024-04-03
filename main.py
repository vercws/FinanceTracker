from FinanceTracker import *
from Password import *
import sys


app = QApplication(sys.argv)
app.setWindowIcon(QIcon("money_icon.png"))
FirstWindow = PasswordGetter()

while 1:
    FirstWindow = PasswordGetter()
    FirstWindow.show()

    result = FirstWindow.exec_()

    if result == QDialog.Accepted and FirstWindow.correct_password_entered:
        SecondWindow = FinanceTrackerApp()
        SecondWindow.show()
        sys.exit(app.exec_())
    elif result == QDialog.Rejected:
        break

sys.exit()


