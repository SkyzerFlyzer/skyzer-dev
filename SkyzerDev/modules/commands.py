import json


class CommandOption:
    name: str
    description: str
    required: bool
    choices: list[str]

    def __init__(self, name: str, description: str, required: bool, choices: list[str] = None):
        if choices is None:
            choices = []
        self.name = name
        self.description = description
        self.required = required
        self.choices = choices


class SubCommand:
    name: str
    description: str
    usage: str
    options: list[CommandOption]

    def __init__(self, name: str, description: str, usage: str, options: list[CommandOption]):
        self.name = name
        self.description = description
        self.usage = usage
        self.options = options


class Command:
    name: str
    description: str
    usage: str
    options: list[CommandOption]
    sub_commands: list[SubCommand]

    def __init__(self, name: str, description: str, usage: str, options=None,
                 sub_commands=None):
        if sub_commands is None:
            sub_commands = []
        if options is None:
            options = []
        self.name = name
        self.description = description
        self.usage = usage
        self.options = options
        self.sub_commands = sub_commands


def load_commands() -> list[Command]:
    with open('SkyzerDev/modules/data/commands.json') as f:
        commands = json.load(f)
    command_list = []
    for command, values in commands.items():
        if values['sub_commands']:
            sub_commands = []
            for sub_command, sub_values in values['sub_commands'].items():
                sub_command_object = SubCommand(sub_command, sub_values['description'], sub_values['usage'],
                                                sub_values['options'])
                sub_commands.append(sub_command_object)
            command_object = Command(command, values['description'], values['usage'], sub_commands=sub_commands)
        elif values['options']:
            options = []
            for option, option_values in values['options'].items():
                option_object = CommandOption(option, option_values['description'], option_values['required'],
                                              option_values['choices'])
                options.append(option_object)
            command_object = Command(command, values['description'], values['usage'], options=options)
        else:
            command_object = Command(command, values['description'], values['usage'])
        command_list.append(command_object)
    return command_list
