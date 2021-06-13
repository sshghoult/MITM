from PySide2 import QtCore, QtWidgets, QtGui
import typing


# import abc


class AbstractChangeEffect(QtCore.QRunnable):
    """Abstract Base Class of the effects that should not be instantiated"""
    # can't be properly marked with abc due to metaclass conflict
    def __init__(self, app: QtWidgets.QApplication, changes):
        super().__init__()
        self.app = app
        self.changes = changes

    def run(self):
        pass


class ChangeCSSEffect(AbstractChangeEffect):
    """Effect of the line that changes CSS of the widget to achieve the stated effect of the line."""
    def __init__(self, app: QtWidgets.QApplication, changes: typing.Dict[str, typing.Dict[str, str]]):
        """
        Init merely instantiates object
        :param app: pointer to the application
        :param changes: Dict[<widget_name>: Dict[<property>: <value>]]
        """
        super().__init__(app, changes)
        # self.setAutoDelete(False)

    def run(self):
        """Executes the effect of the line"""
        self.app.main_window.signals.update_css_signal.emit(self.changes)
