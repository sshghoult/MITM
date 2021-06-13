from PySide2.QtCore import QRunnable
import typing
import re
import random
import line_mechanics


# i need a bunch of QRunnables that implement Line's effect to be called when an input received

class AccessibleLine:
    """An object of internal logic whose information is to be displayed on the GUI's line-describing labels"""
    # has nothing to do with accessibility
    def __init__(self, call_name: str, description: str, arg_type: str):
        self.arg_type = arg_type
        self.description = description
        self.call_name = call_name

    def __str__(self) -> str:
        return self.call_name + f"({self.arg_type})"


class Player:
    def __init__(self, username: str, masked_name: str, hitpoints: int, GUIstate: 'PlayerGUIState'):
        """An object of internal logic that contains information about player in the lobby"""
        self.hitpoints = hitpoints
        self.masked_name = masked_name
        self.username = username
        self.GUIstate = GUIstate

    def __str__(self) -> str:
        return self.masked_name + f' ({self.username})'

    def current_state_str(self) -> str:
        return self.GUIstate.construct_description()


class LocalPlayer(Player):
    """An object of internal logic that contains information about player that uses this client"""
    def __init__(self, username: str, masked_name: str, hitpoints: int, GUIstate: 'PlayerGUIState'):
        super().__init__(username, masked_name, hitpoints, GUIstate)
        self.lines = set()
        self.args = set()


class AccessibleArgument:
    """An object of internal logic whose information is to be displayed on the GUI's line-describing labels"""
    # has nothing to do with accessibility
    possible_types = {'color', 'integer'}

    def __init__(self, _type: str, value: str):
        if _type in self.possible_types:
            self.type = _type
        else:
            raise ValueError("Incorrect type of the argument")
        self.value = value

    def __str__(self) -> str:
        return self.type + f': {str(self.value)}'


class PlayerGUIState:
    """An object of internal logic to contain and display information about state of player's GUI"""

    def __init__(self):
        with open('widget_styles.css', 'r') as source:
            data = ''.join([x.replace('\n', '').strip() for x in source.readlines()])
        objects = re.findall(r'.*? \{.*?\}', data)
        css_dict = {}
        for obj in objects:
            name = re.search(r'^\w*? {', obj)
            traits = obj[name.end():]
            name = name[0][:-2]
            css_dict[name] = {}
            traits = re.findall(r'.*?: .*?;', traits)
            # print(traits)
            css_dict[name].update({x.split(':')[0]: x.split(':')[1][1:-1] for x in traits})
        self.default_state = css_dict
        self.state = self.default_state.copy()
        # print(self.state)
        # print()

    def construct_css(self) -> str:
        """Method that forms syntactically correct CSS string from data to apply to the widgets"""
        # print(self.state)
        # return ';\n'.join(f'{i}: {self.state[i]}' for i in self.state)
        result = []
        for widget in self.state:
            traits = self.state[widget]
            traits_result = '\n'.join([f'{j}: {traits[j]};' for j in traits])
            result.append(f'{widget}' + '{' + f'{traits_result}' '}')
        # print('\n'.join(result))
        return '\n'.join(result)

    def construct_description(self) -> str:
        """Method that constructs a description of player's GUI state to display on the GUI"""
        # return '<br/>'.join(f'{str(i)}: {self.state[i]}' for i in self.state)
        return f'''<p><small>{'<br/>'.join((f"{i}: {self.state['QWidget'][i]}" for i in self.state["QWidget"]))}</small></p>'''

    def __repr__(self) -> str:
        return f'PlayerGUIState id={id(self)}'


class Client:
    """Main unit of the internal logic that manages everything and connects logic to GUI"""
    def __init__(self):
        self.current_player = Player('current_player', 'c', 10, PlayerGUIState())
        self.players = [Player(f'username{x}', f'h', 10, PlayerGUIState()) for x in range(1)] + [self.current_player]
        self.lines = [AccessibleLine(f'caramelldansen', f'caramelldansen_description', 'color'),
                      AccessibleLine('font_size', 'font_size_description', 'integer')]
        self.args = [AccessibleArgument('integer', str(10)), AccessibleArgument('color', 'orange'),
                     AccessibleArgument('integer', str(20)), AccessibleArgument('color', 'magenta')]

        # serverless demo only
        # self.lines_container = lines.PlayableLinesContainer()
        self.line_executioner = line_mechanics.LineExecutioner()


    def check_line(self, line: str) -> typing.Optional[typing.Tuple[bool, None, None], typing.Tuple[bool, AccessibleLine, AccessibleArgument]]:
        """Check format to be correct, line and argument meant to be accessible and appropriate.
        Returns result of check and line and argument objects if these were correct and therefore found"""
        #  -> typing.Tuple[bool, str] to be changed
        import room_main_ui
        # yes, it is terrible approach still, but alternatives are no better
        if re.fullmatch(r'.+\..+\(.+\)', line) is None:
            room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('incorrect format')
            self.send_line(line, False)
            return False, None, None
        # line = "masked_name.call_name(argument)"
        target_masked_name, line_and_argument = line.split('.')
        line, argument = line_and_argument.split('(')
        argument = argument[:-1]
        # print(f'line: {line}')
        # print(f'argument: {argument}')

        for i in self.players:
            if i.masked_name == target_masked_name:
                player_object = i
                break
        else:
            self.send_line(line, False)
            room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('no such player in the room')
            return False, None, None

        for i in self.lines:
            if i.call_name == line:
                line_object = i
                break
        else:
            room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('no such line in the deck')
            self.send_line(line, False)
            return False, None, None

        for i in self.args:
            if i.value == argument:
                arg_object = i
                break
        else:
            room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('no such argument in the deck')
            self.send_line(line, False)
            return False, None, None

        if arg_object.type == line_object.arg_type:
            pass
        else:
            room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('incorrect_argument_type')
            self.send_line(line, False)
            return False, None, None

        room_main_ui.RoomMainWindow.signals.update_hint_bar_signal.emit('200 OK')
        self.send_line(line, True)
        if player_object is self.current_player:
            self.line_executioner.execute(line, argument)
        return True, line_object, arg_object

    def send_line(self, line: str, success: bool):
        pass

    def get_new_line(self):
        line_obj = self.line_executioner.lines[random.choice(list(self.line_executioner.lines.keys()))]
        return AccessibleLine(line_obj.call_name, line_obj.description, line_obj.arg_type)


    def get_new_arg(self) -> AccessibleArgument:
        """Get new argument from the pool"""
        x = random.choice((('color', random.choice(['red', 'green', 'yellow', 'magenta', 'blue', 'pink', 'violet', 'orange'])),
                           ('integer', str(random.randint(10, 30)))))
        return AccessibleArgument(*x)
