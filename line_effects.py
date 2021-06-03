from PySide2 import QtCore, QtWidgets, QtGui
import typing


# import abc


class AbstractChangeEffect(QtCore.QRunnable):
    # is actually abstract and should not be instantiated, but i haven't resolved the conflict of metaclasses here yet
    def __init__(self, app: QtWidgets.QApplication, changes):
        super().__init__()
        self.app = app
        self.changes = changes

    def run(self):
        pass


class ChangeCSSEffect(AbstractChangeEffect):
    def __init__(self, app: QtWidgets.QApplication, changes: typing.Dict[str, typing.Dict[str, str]]):
        """
        :param app: pointer to the application
        :param changes: Dict[<widget_name>, Dict[<property>: <value>]]
        """
        super().__init__(app, changes)
        # self.setAutoDelete(False)

    def run(self) -> None:
        self.app.main_window.signals.update_css_signal.emit(self.changes)
