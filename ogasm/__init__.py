from textwrap import wrap
import ogins as ins

def header(number):
    raw_hex = hex(number)[2:].zfill(8)
    hex_bytes = wrap(raw_hex, 2)
    return bytearray([0xFF] + [int(hex_byte, 16) for hex_byte in hex_bytes])


def assemble(string):
    mnemonics = {value.name: key for key, value in ins.instructions.items()}
    try:
        return mnemonics[string]
    except:
        return int(string, 16)


def lexer(text):
    return [ i for i in text.replace('\n', ' ').split(' ') if i ]


def label_separator(strings):
    #Begin label separator.
    #The label separator takes the lexed assembly code and associates labels with
    #tokens, without specifying their locations.
    labels_removed = []
    known_labels = []
    current_label = []
    for string in strings:
        if string.startswith(':'):
            current_label.append(string[1:])
            known_labels.append(string[1:])
        else:
            if current_label:
                labels_removed.append((string, tuple(current_label)))
                current_label = []
            else:
                labels_removed.append((string, tuple()))
    return labels_removed, known_labels


def to_ints_before_labels(labels_removed, known_labels):
    numbers = []
    for token in labels_removed:
        if token[0] in known_labels:
            numbers.append(token)
        else:
            numbers.append((assemble(token[0]), token[1]))
    return numbers


def get_label_positions(numbers):
    labels = {}
    i = 0
    for token in numbers:
        for label in token[1]:
            labels[label] = i
            print(f'{label}: {i}')
        if type(token[0]) is int:
            i += 1
        else:
            i += 4
    return labels


def to_ints_after_labels(numbers, labels):
    bytecode = []
    for token in numbers:
        token = token[0]
        if type(token) is int:
            bytecode.append(token)
        else:
            token = labels[token]
            bytecode.append(token & 0xFF000000)
            bytecode.append(token & 0x00FF0000)
            bytecode.append(token & 0x0000FF00)
            bytecode.append(token & 0x000000FF)
    return bytecode


def to_bundle(bytecode):
    return header(len(bytecode)) + bytearray(bytecode)

def full_assemble(code):
    lexed = lexer(code)
    labels_removed, known_labels = label_separator(lexed)
    numbers = to_ints_before_labels(labels_removed, known_labels)
    labels = get_label_positions(numbers)
    raw_bytecode = to_ints_after_labels(numbers, labels)
    bytecode = to_bundle(raw_bytecode)
    return bytecode

