from line_effects import *
# import application
import typing
import random
from PySide2 import QtWidgets
import deck
import inspect



class LineExecutioner:
    def __init__(self):
        self.app = None
        self.lines = None

    def load(self, app_reference: QtWidgets.QApplication):
        self.app = app_reference
        self.lines = {cls.call_name: cls for name, cls in deck.__dict__.items() if inspect.isclass(cls) and cls is not deck.AbstractBaseLine}
        print(self.lines)

    def execute(self, line, argument):
        self.lines[line].play(self.app, argument)


if __name__ == '__main__':
    le = LineExecutioner()
    le.load(None)



