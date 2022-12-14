from PyQt5 import QtWidgets
import sys
import main
import main_menu_eng


class MainDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.ui = main_menu_eng.Ui_Dialog()
        self.ui.setupUi(self)

    def get_chart(self, path, length):
        if main.exists(path) or not length == '':
            chart = main.get_chart_dict(path)
        if chart == "invalid path":
            self.ui.chartSource.setPlainText("error: invalid path")
        else:
            meta = main.get_meta(chart, length)
            if meta == (-1, -1, -1, -1):
                self.ui.chartSource.setPlainText("error: invalid time")
            else:
                self.ui.chartSource.setPlainText(main.get_chart(path, length))

    def to_clipboard(self, text):
        main.add_to_clipboard(text)


if __name__ == "__main__":
    myapp = QtWidgets.QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
