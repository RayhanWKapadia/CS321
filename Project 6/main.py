import re

a_commands = []
asm_instructions = []

destinations = {'': '000', 'M=': '001', 'D=': '010', 'MD=': '011',
                'A=': '100', 'AM=': '101', 'AD=': '110', 'AMD=': '111'}
jumps = {'': '000', ';JGT': '001', ';JEQ': '010', ';JGE': '011',
         ';JLT': '100', ';JNE': '101', ';JLE': '110', ';JMP': '111'}
computations = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
                'A': '0110000', 'M': '1110000', '!D': '0001101', '!A': '0110001',
                '!M': '1110001', '-D': '0001111', '-A': '0110011', '-M': '1110011',
                'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111', 'D-1': '0001110',
                'A-1': '0110010', 'M-1': '1110010', 'D+A': '0000010', 'D+M': '1000010',
                'D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111',
                'D&A': '00000000', 'D&M': '1000000', 'D|A': '0010101', 'D|M': '1010101'}
symbols_table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384, 'KBD': 24576,
                 'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
                 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15}

file_name = input('File:')
asm_file = open(file_name + '.asm', 'r')

for line in asm_file:
    cleaned_line = re.sub(r'\/+.*\n|\n| *', '', line)
    if cleaned_line != '':
        a_commands.append(cleaned_line)

asm_file.close()

line_number = 0

for command in a_commands:
    symbol = re.findall(r'\(.+\)', command)
    if symbol != []:
        if symbol[0][1:-1] not in symbols_table:
            symbols_table[symbol[0][1:-1]] = line_number
            line_number -= 1
    line_number += 1

for line in a_commands:
    cleaned_line = re.sub(r'\(.+\)', '', line)
    if cleaned_line != '':
        asm_instructions.append(cleaned_line)

variable_number = 16

for command in asm_instructions:
    symbol = re.findall(r'@[a-zA-Z]+.*', command)
    if symbol != []:
        if symbol[0][1:] not in symbols_table:
            symbols_table[symbol[0][1:]] = variable_number
            variable_number += 1

hack_file = open(file_name + '1.hack', 'w')

for command in asm_instructions:
    if command[0] == '@':
        address = 0
        if command[1:] in symbols_table:
            address = symbols_table[command[1:]] + 32768
        else:
            address = int(command[1:]) + 32768
        hack_file.write('0' + bin(address)[3:] + '\n')
    else:
        dest_match = re.findall(r'.+=', command)
        if dest_match != []:
            dest_code = destinations[str(dest_match[0])]
        else:
            dest_code = destinations['']

        jump_match = re.findall(r';.+', command)
        if jump_match != []:
            jump_code = jumps[str(jump_match[0])]
        else:
            jump_code = jumps['']

        comp_code = computations[re.sub(r'.+=|;.+', '', command)]
        hack_file.write('111' + comp_code + dest_code + jump_code + '\n')

hack_file.close()
