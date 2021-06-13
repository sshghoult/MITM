from PySide2 import QtCore, QtGui, QtWidgets
import time
import random, string
# import room_main_ui
import application
import line_effects
import line_mechanics


class IOWorkerThread(QtCore.QRunnable):
    """Temporarily used GUI-package specific Thread-like object to imitate input of data and therefore mock server-sent data"""
    def __init__(self, app: application.Application):
        super().__init__()
        self.app = app
        self.switch = True
        self.app.main_window.signals.shutdown_signal.connect(self.shutdown)
        self.lines_container = line_mechanics.PlayableLinesContainer(app)

    def shutdown(self):
        self.switch = False

    def run(self):
        # self.lines_container.get_line_runnable('YMCA').play()
        # time.sleep(1)
        # # self.lines_container.get_line_runnable('delimitation', 0).play()
        # self.lines_container.get_line_runnable('font_size', random.randint(10, 30)).play()
        while self.switch:

            # print('IO start')
            time.sleep(1)
            # TODO: add semaphore system here to prevent race condition
            # yes, there is no default instruments for QRunnable to do it. yes, it is terrible.
            if self.switch:
                ...
                # self.lines_container.get_line_runnable('YMCA').play()
                time.sleep(1)
                # self.lines_container.get_line_runnable('delimitation', 0).play()
                # self.lines_container.get_line_runnable('font_size', random.randint(10, 30)).play()

            else:
                break
            # print('IO finish')
