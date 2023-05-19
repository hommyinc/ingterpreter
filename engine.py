import argparse
import msvcrt
from typing import Dict


class IngterpreterEngine:
    def __init__(
        self, 
        # configuration json file used by `runner.py`
        config_dict:Dict=None,
        # activation phrases
        start_string=None, end_string=None, 
        # operation keywords
        inc_ptr_op=None, dec_ptr_op=None, inc_val_op=None, dec_val_op=None, 
        print_op=None, store_op=None, loop_begin_op=None, loop_end_op=None,
        # language configuration
        lang_name=None, extension=None, encoding="euc-kr",
        # misc
        memory_size=32768
    ):
        # 설정 불러와서 엔진 초기 설정 진행
        if config_dict is not None:
            self.start_string = config_dict["COMMANDS"]["ACTIVATION"]["START"]
            self.end_string = config_dict["COMMANDS"]["ACTIVATION"]["END"]

            self.inc_ptr_op = config_dict["COMMANDS"]["OPERATION"]["INC_PTR_OP"]
            self.dec_ptr_op = config_dict["COMMANDS"]["OPERATION"]["DEC_PTR_OP"]
            self.inc_val_op = config_dict["COMMANDS"]["OPERATION"]["INC_VAL_OP"]
            self.dec_val_op = config_dict["COMMANDS"]["OPERATION"]["DEC_VAL_OP"]
            self.print_op = config_dict["COMMANDS"]["OPERATION"]["PRINT_OP"]
            self.store_op = config_dict["COMMANDS"]["OPERATION"]["STORE_OP"]
            self.loop_begin_op = config_dict["COMMANDS"]["OPERATION"]["LOOP_BEGIN_OP"]
            self.loop_end_op = config_dict["COMMANDS"]["OPERATION"]["LOOP_END_OP"]

            self.lang_name = config_dict["TITLE"]
            self.extension = config_dict["EXT"]
            self.encoding = config_dict["ENCODING"] if "ENCODING" in config_dict else encoding

        else:
            assert None not in [
                start_string, end_string,
                inc_ptr_op, dec_ptr_op, inc_val_op, dec_val_op,
                print_op, store_op, loop_begin_op, loop_end_op,
                lang_name, extension
            ], "error: either a configuration json file or keyword arguments required to initialize `IngterpreterEngine`"

            self.start_string = start_string
            self.end_string = end_string

            self.inc_ptr_op = inc_ptr_op
            self.dec_ptr_op = dec_ptr_op
            self.inc_val_op = inc_val_op
            self.dec_val_op = dec_val_op
            self.print_op = print_op
            self.store_op = store_op
            self.loop_begin_op = loop_begin_op
            self.loop_end_op = loop_end_op

            self.lang_name = lang_name
            self.extension = extension
            self.encoding = encoding
        
        for v in [
            self.start_string, self.end_string,
            self.inc_ptr_op, self.dec_ptr_op, self.inc_val_op, self.dec_val_op,
            self.print_op, self.store_op, 
            self.lang_name, self.extension, self.encoding
        ]:
            assert len(v) > 1, "error: invalid configuration"
        
        for v in [self.loop_begin_op, self.loop_end_op]:
            assert len(v) == 1, "error: invalid configuration"
        ##### 엔진 초기 설정 완료 #####
        
        # 기타 기본 언어 설정
        self.memory = [0 for i in range(memory_size)]
        self.pointer = 0
        self.pc = 0
        self.code = ''
        self.jump_to = {}

        self.inc_ptr_op = self.inc_ptr_op.split()
        self.dec_ptr_op = self.dec_ptr_op.split()
        self.inc_val_op = self.inc_val_op.split()
        self.dec_val_op = self.dec_val_op.split()
        self.print_op = self.print_op.split()
        self.store_op = self.store_op.split()

        self.start_string = self.start_string.split()
        self.end_string = self.end_string.split()

        self.op_dict = {
            self.to_string(self.inc_ptr_op) : self.increase_pointer,
            self.to_string(self.dec_ptr_op) : self.decrease_pointer,
            self.to_string(self.inc_val_op) : self.increase_value,
            self.to_string(self.dec_val_op) : self.decrease_value,
            self.to_string(self.print_op) : self.print_value,
            self.to_string(self.store_op) : self.store_value
        }

    def to_string(self, op):
        return ' '.join(op)

    def operation(self, code, ind):
        command = code[ind]
        for operator_str in self.op_dict.keys():
            operator = operator_str.split()
            if command == operator[0]:
                for i in range(len(operator)):
                    if code[ind + i] != operator[i]:
                        raise Exception("Syntax Error")
                self.op_dict[self.to_string(operator)]()
                pc_increment = len(operator)
                return pc_increment
        return -1

    def load(self, code:str):
        self.code = code

    def increase_pointer(self):
        if self.pointer >= len(self.memory):
            raise Exception("Out of memory")
        self.pointer += 1

    def decrease_pointer(self):
        if self.pointer <= 0:
            raise Exception("Out of memory")
        self.pointer -= 1

    def increase_value(self):
        self.memory[self.pointer] += 1

    def decrease_value(self):
        self.memory[self.pointer] -= 1

    def print_value(self):
        print(chr(self.memory[self.pointer]), end='')

    def store_value(self):
        self.memory[self.pointer] = ord(msvcrt.getch())

    def preprocess(self):
        stack = []
        for i in range(len(self.code)):
            command = self.code[i]
            if command == self.loop_begin_op:
                stack.append(i)
            elif command == self.loop_end_op:
                if len(stack) == 0:
                    raise Exception("Syntax Error")
                self.jump_to[i] = stack.pop(-1)
                self.jump_to[self.jump_to[i]] = i

        if len(stack) > 0:
            raise Exception("Syntax Error")

    def jump(self, command):
        if command == self.loop_begin_op and self.memory[self.pointer] == 0:
            self.pc = self.jump_to[self.pc]
        elif command == self.loop_end_op and self.memory[self.pointer] != 0:
            self.pc = self.jump_to[self.pc]
            

    def run(self):
        self.preprocess()
        
        while self.pc < len(self.code):
            
            pc_increment = self.operation(self.code, self.pc)
            if pc_increment != -1:
                self.pc += pc_increment
                continue
            else:
                pc_increment = 1

            command = self.code[self.pc]
            
            if command == self.loop_begin_op or command == self.loop_end_op:
                self.jump(command)

            self.pc += pc_increment

    def load(self, file_name:str):
        f = open(file_name, 'r')
        tokens = f.read().replace('\n', ' ').split()
        f.close()
        if self.start_string[0] in tokens:
            start = tokens.index(self.start_string[0])
            for i in range(len(self.start_string)):
                if tokens[start + i] != self.start_string[i]:
                    print(tokens[start + i])
                    print(self.start_string[i])
                    raise Exception("Syntax Error")
            start += len(self.start_string)
            if self.end_string[0] in tokens[start:]:
                end = tokens.index(self.end_string[0])
                for i in range(len(self.end_string)):
                    if tokens[end + i] != self.end_string[i]:
                        raise Exception("Syntax Error")
                
        self.code = tokens[start:end]

    def convert(self, input_file, output_file):
        f = open(input_file, 'r')
        lines = f.read().replace('\n', '')
        f.close()
        fw = open(output_file, 'w')
        fw.write(self.to_string(self.start_string) + '\n\n')
        for command in lines:
            if command == '>':
                fw.write(self.to_string(self.inc_ptr_op) + ' ')
            elif command == '<':
                fw.write(self.to_string(self.dec_ptr_op) + ' ')
            elif command == '+':
                fw.write(self.to_string(self.inc_val_op) + ' ')
            elif command == '-':
                fw.write(self.to_string(self.dec_val_op) + ' ')
            elif command == '.':
                fw.write(self.to_string(self.print_op) + ' ')
            elif command == ',':
                fw.write(self.to_string(self.store_op) + ' ')
            elif command == '[':
                fw.write(self.to_string(self.loop_begin_op) + ' ')
            elif command == ']':
                fw.write(self.to_string(self.loop_end_op) + ' ')
        fw.write('\n\n' + self.to_string(self.end_string))

# ing = Ingterpreter()
# #ing.convert('helloworld.bf', 'helloworld.ing')
# ing.load('tictactoe.ing')
# ing.run()
