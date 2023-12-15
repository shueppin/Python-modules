TEXT_COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'dark_yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'light_grey': '\033[37m',
    'dark_grey': '\033[90m',
    'light_red': '\033[91m',
    'light_green': '\033[92m',
    'yellow': '\033[93m',
    'light_blue': '\033[94m',
    'pink': '\033[95m',
    'light_cyan': '\033[96m',
    'white': '\033[97m'
}

BG_COLORS = {
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'orange': '\033[43m',
    'blue': '\033[44m',
    'purple': '\033[45m',
    'cyan': '\033[46m',
    'light_grey': '\033[47m',
    'dark_grey': '\033[100m',
    'light_red': '\033[101m',
    'light_green': '\033[102m',
    'yellow': '\033[103m',
    'light_blue': '\033[104m',
    'pink': '\033[105m',
    'light_cyan': '\033[106m',
    'white': '\033[107m'
}

SPECIAL = {
    'reset': '\033[0m',
    'bold': '\033[01m',
    # 'disable': '\033[02m',
    'italics': '\033[03m',
    'underlined': '\033[04m',
    'reverse': '\033[07m',
    # 'invisible': '\033[08m',
    'strikethrough': '\033[09m',
    'thick_underlined': '\033[21m',
    'boxed': '\033[51m',
    # 'boxed2': '\033[52m',
}


HEX_COMMANDS = {
    '0': TEXT_COLORS['black'],
    '1': TEXT_COLORS['blue'],
    '2': TEXT_COLORS['green'],
    '3': TEXT_COLORS['cyan'],
    '4': TEXT_COLORS['red'],
    '5': TEXT_COLORS['purple'],
    '6': TEXT_COLORS['dark_yellow'],
    '7': TEXT_COLORS['light_grey'],
    '8': TEXT_COLORS['dark_grey'],
    '9': TEXT_COLORS['light_blue'],
    'A': TEXT_COLORS['light_green'],
    'B': TEXT_COLORS['light_cyan'],
    'C': TEXT_COLORS['light_red'],
    'D': TEXT_COLORS['pink'],
    'E': TEXT_COLORS['yellow'],
    'F': TEXT_COLORS['white'],
    'L': SPECIAL['italics'],
    'R': SPECIAL['reset']
}


class ComplexColorPrint:
    def __init__(self):
        self.output = ''

    def add_text(self, text: str, color: str, special: str or list = None, background=''):
        if text and color:  # If both variables are not empty
            if color in TEXT_COLORS:  # If the color exists
                self.output += TEXT_COLORS[color]

            if special:  # If some special features are given
                special_elements = []

                if type(special) == str:  # If it is a string, then it splits it into a list
                    special = special.strip()

                    if ',' in special:  # This means, the elements are separated by a ","
                        special_elements = special.split(',')

                    elif ';' in special:  # This means, the elements are separated by a ";"
                        special_elements = special.split(';')

                    elif ' ' in special:  # This means, the elements are separated by a space
                        special_elements = special.split(' ')

                    else:  # This means it is only one element
                        special_elements.append(special)

                elif type(special) == list:  # If it is a list then it's perfect
                    special_elements = special

                for element in special_elements:  # Go through all the elements
                    element = str(element)
                    element = element.strip()  # Remove all spaces

                    if element in SPECIAL:  # If the element exists
                        self.output += SPECIAL[element]

            if background:  # If a background color is  given
                if background in BG_COLORS:  # If the color exists
                    self.output += BG_COLORS[background]

            self.output += str(text)
            self.output += SPECIAL['reset']

    def print(self, show_result=True):
        output = self.output

        self.output = ''  # Reset the output text

        if show_result:
            print(output)
        else:
            return output


def hex_commands_print(text: str, separation_character='§', show_result=True):
    text_list = text.split(separation_character)

    output_text_list = [text_list[0]]

    for part in text_list[1:]:  # Skip the first element because it will not have a hex command
        color_code = part[0].capitalize()
        try:
            color_string = HEX_COMMANDS[color_code]
        except KeyError:
            color_string = f'ERROR_WRONG_COLOR_{color_code}'

        output_part = color_string + part[1:]
        output_text_list.append(output_part)

    output = ''.join(output_text_list)

    if show_result:
        print(output)
    else:
        return output


def color_print(text: str, color: str, special: str or list = None, background='', show_result=True):
    color_printer = ComplexColorPrint()
    color_printer.add_text(text, color, special, background)

    return color_printer.print(show_result=show_result)


def structure_list_color_print(text_structure_list: list, show_result: bool = True):
    """
    Create a complex colored text line with one list containing dictionaries.

    :param show_result: If it should print the result or just return it
    :param text_structure_list: List that contains dictionaries with the keys "text", "color", "special" (optional) and "background" (optional). Help can be found in the function "color_print".
    """
    color_printer = ComplexColorPrint()  # Create a complex color printer

    for text_part_dictionary in text_structure_list:
        if 'text' in text_part_dictionary and 'color' in text_part_dictionary:
            text = text_part_dictionary['text']
            color = text_part_dictionary['color']

            if 'special' in text_part_dictionary:
                special = text_part_dictionary['special']
            else:
                special = ''

            if 'background' in text_part_dictionary:
                background = text_part_dictionary['background']
            else:
                background = ''

            color_printer.add_text(text, color, special=special, background=background)

    return color_printer.print(show_result=show_result)


if __name__ == '__main__':
    """
    The "background" and the "special" arguments are optional.
    
    The "special" arguments can be passed either as a string (separated by "," or ";" or a space) or as list
    """
    color_print('Color_print: Space', 'green', special='bold underlined', background='black')
    color_print('Color_print: Comma', 'green', special='bold, underlined', background='black')
    color_print('Color_print: Semicolon', 'green', special='bold; underlined', background='black')
    color_print('Color_print: List', 'green', special=['bold', 'underlined'], background='black')

    ColorPrinter = ComplexColorPrint()
    ColorPrinter.add_text('Complex', 'red', 'bold')
    ColorPrinter.add_text('Color', 'green')
    ColorPrinter.add_text('Print()', 'light_cyan', 'underlined')
    ColorPrinter.print()

    structure_list_color_print([{'text': 'structure_', 'color': 'blue', 'special': 'underlined'}, {'text': 'list_', 'color': 'cyan'}, {'text': 'color_', 'color': 'purple', 'special': 'italics'}, {'text': 'print()', 'color': 'dark_yellow', 'special': 'boxed'}])
