
class Command:
    comamnds = {}

    def __init__(self, state, name, function):
        self.state = state
        self.name = name
        self.commands[name] = self

    def start(self, time):
        return

    def stop(self, time, delta):
        return


class Commands:
    def __init__(self, state):
        self.commands = []
        self.state = state

    def register(self, name, key, function):
        c = {}
        c['function'] = function
        c['started'] = False
        c['key'] = key
        c['name'] = name
        self.commands.append(c)

    def handle(self):
        for command in self.commands:
            if self.state.controls.pressed[command['key']] and not command['started']:
                if 'start' in command['function']:
                    command['function']['start']()
                command['started'] = not command['started']

            if not self.state.controls.pressed[command['key']] and command['started']:
                if 'stop' in command['function']:
                    command['function']['stop']()
                command['started'] = not command['started']

