import line_effects
import abc


class AbstractBaseLine(abc.ABC):
    effect_type = None
    call_name = None
    arg_type = None
    description = None

    @classmethod
    @abc.abstractmethod
    def play(cls, app_reference, argument):
        ...




class CaramelldansenLine(AbstractBaseLine):
    effect_type = line_effects.ChangeCSSEffect
    call_name = 'caramelldansen'
    arg_type = 'color'
    description = 'WE CARAMELLDANSEN'

    @classmethod
    def play(cls, app_reference, color):
        changes = {}
        widgets = ['QWidget', 'PlayerLabel', 'LineLabel', 'ArgumentLabel', 'DataFrame', 'InputLineEdit',
                   'ControlledTextBrowser', 'CustomHintBarLabel']
        # colors = ['red', 'green', 'yellow', 'magenta', 'blue', 'pink', 'violet', 'orange']
        for i in widgets:
            changes[i] = {'color': color}

        cls.effect_type(app_reference, changes).run()


class FontSizeLine(AbstractBaseLine):
    effect_type = line_effects.ChangeCSSEffect
    call_name = 'font_size'
    arg_type = 'integer'
    description = 'WRONG LEVER, KRONK!'

    @classmethod
    def play(cls, app_reference, size):
        changes = {}
        widgets = ['QWidget', 'PlayerLabel', 'LineLabel', 'ArgumentLabel', 'DataFrame', 'InputLineEdit',
                   'ControlledTextBrowser', 'CustomHintBarLabel']
        for i in widgets:
           changes[i] = {'font-size': f'{size}pt'}

        cls.effect_type(app_reference, changes).run()