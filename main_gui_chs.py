from PyQt5 import QtWidgets
import sys
from main import get_chart, get_meta, exists, get_chart_dict, add_to_clipboard
import main_menu_chs


class MainDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.ui = main_menu_chs.Ui_Dialog()
        self.ui.setupUi(self)

    def get_chart(self, path, length):
        if exists(path) or not length == '':
            chart = get_chart_dict(path)
        if chart == "invalid path":
            self.ui.chartSource.setPlainText("错误: 非法路径")
        else:
            meta = get_meta(chart, length)
            if meta == (-1, -1, -1, -1):
                self.ui.chartSource.setPlainText("错误: 非法时间(请使用半角冒号(:))")
            else:
                self.ui.chartSource.setPlainText(get_chart(path, length))

    def to_clipboard(self, text):
        add_to_clipboard(text)


if __name__ == "__main__":
    myapp = QtWidgets.QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
