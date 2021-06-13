from line_effects import *
# import application
import typing
import random
from PySide2 import QtWidgets
import deck
import inspect



class LineExecutioner:
    """Object that executes lines received from server by call_name and argument"""
    def __init__(self):
        self.app = None
        self.lines = None

    def load(self, app_reference: QtWidgets.QApplication):
        """Loads line objects from specific module."""
        # Called after application object instantiation to avoid circular import
        self.app = app_reference
        self.lines = {cls.call_name: cls for name, cls in deck.__dict__.items() if inspect.isclass(cls) and cls is not deck.AbstractBaseLine}
        print(self.lines)

    def execute(self, line, argument):
        """Execution of line among existing by call_name and external received argument"""
        self.lines[line].play(self.app, argument)


if __name__ == '__main__':
    le = LineExecutioner()
    le.load(None)



