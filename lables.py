from PySide2 import QtWidgets, QtCore, QtGui

import internal_logic


class DescribedLabel(QtWidgets.QLabel):
    """Label, which purpose is providing additional info on object by click
    (e.g. description of the line, enemies' states)"""

    def __init__(self, parent, maintext: str,
                 extendedtext: str):
        self.maintext = f'<p><b>{maintext}</b></p>'
        self.extendedtext = self.maintext + f'<p>{extendedtext}</p>'
        super().__init__(self.maintext, parent)
        self.setMouseTracking(True)
        self.state = 0

        self.setFocusPolicy(QtCore.Qt.TabFocus)
        # style = "border-style: outset;" \
        #         "border-width: 1px;" \
        #         "border-color: grey"

        # self.setStyleSheet(style)
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        # self.setFrameShadow(QtWidgets.QFrame.Raised)

    def update_texts(self, maintext:  str, extendedtext: str):
        self.maintext = f'<p><b>{maintext}</b></p>'
        self.extendedtext = self.maintext + f'<p>{extendedtext}</p>'
        self.setText(self.maintext)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.extend_cut()
        ev.accept()

    def extend_cut(self):
        # this system might be a bad idea if you want to compare options
        # closes the last when opens another
        if self.state == 0:
            self.state = 1
            if self.parent().current_extension is not None:
                self.parent().current_extension.extend_cut()
            self.parent().current_extension = self
            self.setText(self.extendedtext)
        else:
            self.state = 0
            self.setText(self.maintext)
            self.parent().current_extension = None


# should have one more class in inheritance chain?

class PlayerLabel(DescribedLabel):
    def __init__(self, parent, bound_player_object: internal_logic.Player):
        super().__init__(parent,
                         bound_player_object.masked_name + f'<br/><i><small><small>({bound_player_object.username})</small></small></i>',
                         bound_player_object.current_state_str())
        self.bound_object = bound_player_object

    def update_bound_object(self, new_object):
        self.bound_object = new_object
        maintext = new_object.masked_name + f'<br/><i><small><small>({new_object.username})</small></small></i>'
        extendedtext = new_object.current_state_str()
        self.update_texts(maintext, extendedtext)



class LineLabel(DescribedLabel):
    def __init__(self, parent, bound_line_object: internal_logic.AccessibleLine):
        """

        :param parent:
        :param bound_line_object:
        """
        super().__init__(parent, str(bound_line_object),
                         bound_line_object.description)
        self.bound_object = bound_line_object

    def update_bound_object(self, new_object):
        self.bound_object = new_object
        maintext = str(new_object)
        extendedtext = new_object.description
        self.update_texts(maintext, extendedtext)


class ArgumentLabel(DescribedLabel):
    def __init__(self, parent, bound_arg_object: internal_logic.AccessibleArgument):
        super().__init__(parent, str(bound_arg_object), '')
        self.bound_object = bound_arg_object

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        ev.accept()

    def update_bound_object(self, new_object):
        self.bound_object = new_object
        maintext = str(new_object)
        self.update_texts(maintext, '')

