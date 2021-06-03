from PySide2 import QtWidgets, QtCore, QtGui


class ChatFrame(QtWidgets.QFrame):
    def __init__(self, parent, *flags):
        super().__init__(parent, *flags)
        mainlayout = QtWidgets.QGridLayout(self)
        self.setLayout(mainlayout)
        browser = ControlledTextBrowser(self)
        # browser.setSource(QtCore.QUrl('test_source.txt'))
        # browser.setTextColor(QtGui.QColor('white'))
        with open('test_source.txt', 'r') as source:
            browser.setHtml(source.read())
        mainlayout.addWidget(browser)
        browser.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding))
        self.entry_frame = EntryFrame(self)
        mainlayout.addWidget(self.entry_frame)


class EntryFrame(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget, *flags):
        super().__init__(parent, *flags)
        mainlayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainlayout)
        self.hint_bar = CustomHintBarLabel('hint bar', self)
        mainlayout.addWidget(self.hint_bar)

        self.mitm_checkbox = QtWidgets.QCheckBox('MITM', self)
        mainlayout.addWidget(self.mitm_checkbox)

        self.input_entry = InputLineEdit(self)
        mainlayout.addWidget(self.input_entry)
        from room_main_ui import RoomMainWindow
        # yes, it's terrible, but it works. PyQt is terrible in the first place.
        RoomMainWindow.signals.update_hint_bar_signal.connect(self.hint_bar.setText)


class CustomHintBarLabel(QtWidgets.QLabel):
    def __init__(self, text, parent, *flags):
        super().__init__(f"<i>{text}</i>", parent, *flags)

    def setText(self, text: str) -> None:
        super().setText(f"<i>{text}</i>")


class InputLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, *flags):
        super().__init__(parent, *flags)
        self.installEventFilter(self)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress and event.modifiers() & QtCore.Qt.ControlModifier:
            if event.matches(QtGui.QKeySequence.Copy) or event.matches(QtGui.QKeySequence.Paste) or event.matches(QtGui.QKeySequence.Undo) \
                    or event.matches(QtGui.QKeySequence.Redo) or event.matches(QtGui.QKeySequence.Cut) \
                    or event.matches(QtGui.QKeySequence.SelectAll):
                # print('shortcut blocked')
                return True
        return False


class ControlledTextBrowser(QtWidgets.QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)
        from room_main_ui import RoomMainWindow
        # yes, it's terrible, but it works. PyQt is terrible in the first place.
        RoomMainWindow.signals.append_to_text_browser.connect(self.append)

    # def setHtml(self, text: str) -> None:
    #     super().setHtml(f'''<font color="#00ef00">{text}</font>''')


