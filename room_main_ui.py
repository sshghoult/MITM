from PySide2 import QtCore, QtGui, QtWidgets
import internal_logic
import typing
# import time


from chatframe import ChatFrame
from dataframe import DataFrame
from lables import PlayerLabel, LineLabel, ArgumentLabel


class CommunicationSignals(QtCore.QObject):
    update_css_signal = QtCore.Signal(dict)
    shutdown_signal = QtCore.Signal()
    update_hint_bar_signal = QtCore.Signal(str)
    append_to_text_browser = QtCore.Signal(str)


class RoomMainWindow(QtWidgets.QMainWindow):
    signals = CommunicationSignals()

    def __init__(self, client_object: internal_logic.Client, *args, **kwargs):
        super(RoomMainWindow, self).__init__(*args, **kwargs)
        self.client = client_object
        self.setup_ui()
        self.installEventFilter(self)

    def setup_ui(self):
        self.setWindowTitle('MITM')
        main_layout = QtWidgets.QGridLayout(self)

        main_frame = QtWidgets.QFrame(self)
        self.setCentralWidget(main_frame)
        self.centralWidget().setStyleSheet(open('widget_styles.css', 'r').read())
        main_frame.setLayout(main_layout)

        self.player_frame = DataFrame(self, self.client.players, PlayerLabel)
        main_layout.addWidget(self.player_frame, 1, 1)
        self.player_frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.line_frame = DataFrame(self, self.client.lines, LineLabel)
        main_layout.addWidget(self.line_frame, 1, 2)
        self.line_frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.args_frame = DataFrame(self, self.client.args, ArgumentLabel)
        main_layout.addWidget(self.args_frame, 1, 3)
        self.args_frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.chat_frame = ChatFrame(self)
        main_layout.addWidget(self.chat_frame, 1, 4)
        self.chat_frame.entry_frame.input_entry.setFocus()
        self.chat_frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.signals.update_css_signal.connect(self.update_css)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress and event.key() == 16777220:
            result, line_obj, arg_obj = self.client.check_line(self.chat_frame.entry_frame.input_entry.text())
            self.signals.append_to_text_browser.emit(self.chat_frame.entry_frame.input_entry.text())
            print(arg_obj.__repr__())
            # print(self.client.lines)
            print(self.client.args)
            if result:
                self.chat_frame.entry_frame.input_entry.setText('')
                new_line_obj = self.client.get_new_line()
                new_arg_object = self.client.get_new_arg()

                for i in self.line_frame.widgets:
                    # print(i.bound_object.__repr__())
                    if i.bound_object is line_obj:
                        i.update_bound_object(new_line_obj)
                        # self.line_frame.widgets.remove(i)
                        self.client.lines.remove(line_obj)
                        self.client.lines.append(new_line_obj)
                        # self.line_frame.widgets.append(new_line_obj)
                        break

                # print(f'analyzing arguments; aeg_obj: {arg_obj}')
                for i in self.args_frame.widgets:
                    # print(f'analyzing {i}, BO: {i.bound_object}')
                    # print(i.bound_object.__repr__())
                    if i.bound_object is arg_obj:
                        # print(f'found! {i.bound_object}')
                        # print('previous: ' + i.bound_object.__repr__())
                        i.update_bound_object(new_arg_object)
                        self.client.args.remove(arg_obj)
                        self.client.args.append(new_arg_object)
                        # print(f'new_object: {new_arg_object}')
                        # print('new: ' + i.bound_object.__repr__())
                        # self.args_frame.widgets.remove(i)
                        # self.args_frame.widgets.append(new_arg_object)
                        break
                # print(self.client.args)

            return True
        return False
        # if event.type() == QtCore.QEvent.KeyPress:
        #     print(event.key())
        # return False

    def update_window_title(self, title: str):
        self.setWindowTitle(title)

    # should be new_data: Dict[<widget_name>, Dict[<property>: <value>]]
    def update_css(self, new_data: typing.Dict[str, typing.Dict[str, str]]):
        # print(self.client.current_player.GUIstate.state)
        # print(new_data)
        for widget in new_data:
            new_info = new_data[widget]
            # print(widget, self.client.current_player.GUIstate.state[widget])
            for trait in new_info:
                self.client.current_player.GUIstate.state[widget] = \
                    self.client.current_player.GUIstate.state.get(widget, {})
                self.client.current_player.GUIstate.state[widget][trait] = new_info[trait]
            # print(widget, self.client.current_player.GUIstate.state[widget])
        self.centralWidget().setStyleSheet(self.client.current_player.GUIstate.construct_css())
        # print(self.client.current_player.GUIstate.state)
        # print()

        # print('updated_css')

    def event(self, event: QtCore.QEvent) -> bool:
        return super().event(event)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.signals.shutdown_signal.emit()
        super().closeEvent(event)

# TODO: implement a timer
# TODO: behaviour-changing effects
# (but not for the demo, don't have time to)
# TODO: create venv  with required packages on the flash drive
