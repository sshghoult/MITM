from PySide2 import QtCore, QtGui, QtWidgets
import IO
import sys
import internal_logic
import room_main_ui
import typing
# import threading
# import time
import random
# import lines


class Application(QtWidgets.QApplication):
    """
    Subclass of QApplication to achieve flexibility when needed
    """
    def __init__(self, sys_arguments):
        super().__init__(sys_arguments)
        self.main_window = room_main_ui.RoomMainWindow(internal_logic.Client())
        self.main_window.show()


if __name__ == '__main__':
    # at this point i openly hate qt with passion

    app = Application(sys.argv)
    # lines_container = lines.PlayableLinesContainer(app)
    #
    # threadpool = QtCore.QThreadPool()
    # io_thrd = IO.IOWorkerThread(app)
    # threadpool.start(io_thrd)
    app.main_window.client.line_executioner.load(app)

    app.exec_()
