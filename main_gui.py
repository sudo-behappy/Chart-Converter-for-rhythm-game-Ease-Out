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
                self.ui.chartSource.setPlainText("error: invalid time(please use English :, not：)")
            else:
                delta = main.get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1])
                note_list = main.get_note_list(chart, delta)
                adjusted_note_list = main.adjust_notes(note_list, delta)
                chart_string = main.generate_code_string(adjusted_note_list)
                self.ui.chartSource.setPlainText(chart_string)

    def to_clipboard(self, text):
        main.add_to_clipboard(text)


if __name__ == "__main__":
    myapp = QtWidgets.QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
