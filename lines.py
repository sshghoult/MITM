from line_effects import *
# import application
import typing
import random


# this is a temporary implementation, i'm thinking about lazy loading of required object from file
# though this shouldn't take too much memory

# perhaps i shouldn't store already created QRunnables and store arguments for them to be created

# : application.Application,

class PlayableLine:
    def __init__(self, app, call_name: str, effect_class: typing.Type[AbstractChangeEffect],
                 effect_arguments: tuple):
        self.effect_arguments = effect_arguments
        self.effect_class = effect_class
        self.call_name = call_name
        self.app = app

    def play(self):
        runnable = self.effect_class(self.app, *self.effect_arguments)
        runnable.run()


class PlayableLinesContainer:
    # TODO: this might be a terrible idea, is it better to create a tree of inheritance with class for each card? should think about it.
    def __init__(self):
        self.lines = {}
        self.args_types = {}


    def ready(self, app):
        self.app = app
        self.load_lines()

    def get_line_runnable(self, name, *args, **kwargs):
        # print(f'get_line_runnable: {args}; {kwargs}')
        return self.lines[name](*args, **kwargs)

    def load_lines(self):
        def caramelldansen(usls):
            result = {}
            widgets = ['QWidget', 'PlayerLabel', 'LineLabel', 'ArgumentLabel', 'DataFrame', 'InputLineEdit',
                       'ControlledTextBrowser', 'CustomHintBarLabel']
            colors = ['red', 'green', 'yellow', 'magenta', 'blue', 'pink', 'violet', 'orange']
            line = None
            for i in widgets:
                result[i] = {'color': usls}
                # f'#{(hex(random.getrandbits(8))[2:] + hex(random.getrandbits(8))[2:] + hex(random.getrandbits(8))[2:]).rjust(6, "0")}'
                line = PlayableLine(self.app, 'caramelldansen', ChangeCSSEffect, (result,))
            return line

        def delimitation(width):
            # i'm not sure it works
            result = {}
            widgets = ['QWidget']
            for i in widgets:
                result[i] = {'border-width': f'{width}px'}
            line = PlayableLine(self.app, 'delimitation', ChangeCSSEffect, (result,))
            return line

        def font_size(size):
            # extremely big fonts resize the window, might be a weapon
            result = {}
            widgets = ['QWidget', 'PlayerLabel', 'LineLabel', 'ArgumentLabel', 'DataFrame', 'InputLineEdit',
                       'ControlledTextBrowser', 'CustomHintBarLabel']
            for i in widgets:
                result[i] = {'font-size': f'{size}pt'}
            line = PlayableLine(self.app, 'font_size', ChangeCSSEffect, (result,))
            return line





        self.lines[caramelldansen.__name__] = caramelldansen
        self.args_types[caramelldansen.__name__] = 'color'
        #
        # self.lines[delimitation.__name__] = delimitation
        self.lines[font_size.__name__] = font_size
        self.args_types[font_size.__name__] = 'integer'

