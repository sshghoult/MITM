import typing

from PySide2 import QtWidgets

from lables import PlayerLabel, LineLabel, ArgumentLabel


class DataFrame(QtWidgets.QFrame):
    def __init__(self, parent, objects: list,
                 label_type: typing.Union[typing.Type[PlayerLabel], typing.Type[LineLabel], typing.Type[ArgumentLabel]], *flags):
        super().__init__(parent, *flags)

        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.widgets = [label_type(self, x) for x in objects]
        # actually label_type is a subclass of DescribedLabel, first have different signature and only take object to build on
        for wdg in self.widgets:
            self.layout().addWidget(wdg)
        self.current_extension = None
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)