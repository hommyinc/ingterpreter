import platform
if "windows" in platform.system().lower():
    import msvcrt as getchlib
else:
    import getch as getchlib
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
            self.start_string = config_dict["COMMANDS"]["ACTIVATION"]["START"].strip()
            self.end_string = config_dict["COMMANDS"]["ACTIVATION"]["END"].strip()

            self.inc_ptr_op = config_dict["COMMANDS"]["OPERATION"]["INC_PTR_OP"].strip()
            self.dec_ptr_op = config_dict["COMMANDS"]["OPERATION"]["DEC_PTR_OP"].strip()
            self.inc_val_op = config_dict["COMMANDS"]["OPERATION"]["INC_VAL_OP"].strip()
            self.dec_val_op = config_dict["COMMANDS"]["OPERATION"]["DEC_VAL_OP"].strip()
            self.print_op = config_dict["COMMANDS"]["OPERATION"]["PRINT_OP"].strip()
            self.store_op = config_dict["COMMANDS"]["OPERATION"]["STORE_OP"].strip()
            self.loop_begin_op = config_dict["COMMANDS"]["OPERATION"]["LOOP_BEGIN_OP"].strip()
            self.loop_end_op = config_dict["COMMANDS"]["OPERATION"]["LOOP_END_OP"].strip()

            self.lang_name = config_dict["TITLE"].strip()
            self.extension = config_dict["EXT"].strip()
            self.encoding = config_dict["ENCODING"].strip() if "ENCODING" in config_dict else encoding.strip()

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
            assert len(v) >= 1, "error: invalid configuration"
        
        for v in [self.loop_begin_op, self.loop_end_op]:
            assert len(v) == 1, "error: invalid configuration"
        ##### 엔진 초기 설정 완료 #####
        
        # 기타 기본 언어 설정
        #   ref) https://kciter.so/posts/crafting-esolang#초기화
        self.memory = [0 for i in range(memory_size)] # 메모리
        self.initialize()
        self.op_dict = {
            self.inc_ptr_op : self.increase_pointer,
            self.dec_ptr_op : self.decrease_pointer,
            self.inc_val_op : self.increase_value,
            self.dec_val_op : self.decrease_value,
            self.print_op   : self.print_value,
            self.store_op   : self.store_value,
        }

    #################### operation ####################

    def operation(self):
        code, ind = self.code, self.pc
        command_1stchr = code[ind]
        for operator_str in self.op_dict:
            if command_1stchr == operator_str[0]:
                if code[ind:ind+len(operator_str)] == operator_str:
                    self.op_dict[operator_str]()
                    pc_increment = len(operator_str)
                    return pc_increment
        return -1

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
        self.memory[self.pointer] = ord(getchlib.getch())

    def jump(self, command):
        if command == self.loop_begin_op and self.memory[self.pointer] == 0:
            self.pc = self.jump_to[self.pc]
        elif command == self.loop_end_op and self.memory[self.pointer] != 0:
            self.pc = self.jump_to[self.pc]

    #################### run ####################

    def initialize(self, file_name:str=None):
        if file_name is not None:
            with open(file_name, 'r', encoding=self.encoding) as f:
                tokens = f.read().replace('\n', '')
            try:
                start_idx = tokens.index(self.start_string) + len(self.start_string)-1
                end_idx = tokens.index(self.end_string)
            except:
                raise Exception("error: Syntax Error\n\t"
                    f"check the content of your script file: {file_name}\n"
                    f"the content of {self.lang_name} script must start with \"{self.start_string}\" "
                    f"and end with \"{self.end_string}\".")
                    
            self.code = tokens[start_idx:end_idx]
        else:
            self.code = ''  # 코드를 저장할 배열
        
        self.pointer = 0    # 포인터
        self.pc = 0         # 프로그램 카운터, 코드의 위치
        self.jump_to = {}

    def preprocess(self):
        stack = []
        for i in range(len(self.code)):
            command = self.code[i]
            if command == self.loop_begin_op:
                stack.append(i)
            elif command == self.loop_end_op:
                if len(stack) == 0:
                    raise Exception("error: Syntax Error\n\t"
                        "the content of your script file have irregular loop syntaxes.")
                self.jump_to[i] = stack.pop(-1)
                self.jump_to[self.jump_to[i]] = i
        if len(stack) > 0:
            raise Exception("error: Syntax Error\n\t"
                "the content of your script file have irregular loop syntaxes.")

    def run(self):
        self.preprocess()
        
        while self.pc < len(self.code):
            
            pc_increment = self.operation()
            if pc_increment != -1:
                self.pc += pc_increment
                continue
            else:
                pc_increment = 1

            command = self.code[self.pc]
            
            if command == self.loop_begin_op or command == self.loop_end_op:
                self.jump(command)

            self.pc += pc_increment

    #################### convert ####################

    def convert(self, input_file, output_file):
        # convert 모드를 명시하지 않고 사용하는 경우 대비
        if input_file.split('.')[-1] == self.extension:
            self.convert_i2b(input_file, output_file)
        elif output_file.split('.')[-1] == self.extension:
            self.convert_b2i(input_file, output_file)
        else:
            raise ValueError("error: a valid command is required\n\t"
                "please refrain from using `convert` method. "
                "use either `convert_b2i` method or `convert_i2b` method if you must use Python class directly.")

    def convert_b2i(self, input_file, output_file):
        with open(input_file, 'r') as fb:
            lines = fb.read().replace('\n', '')
        with open(output_file, 'w', encoding=self.encoding) as fi:
            fi.write(self.start_string + "\n\n")
            for command in lines:
                if command == '>':
                    fi.write(self.inc_ptr_op + ' ')
                elif command == '<':
                    fi.write(self.dec_ptr_op + ' ')
                elif command == '+':
                    fi.write(self.inc_val_op + ' ')
                elif command == '-':
                    fi.write(self.dec_val_op + ' ')
                elif command == '.':
                    fi.write(self.print_op + ' ')
                elif command == ',':
                    fi.write(self.store_op + ' ')
                elif command == '[':
                    fi.write(self.loop_begin_op + ' ')
                elif command == ']':
                    fi.write(self.loop_end_op + ' ')
            fi.write("\n\n" + self.end_string)
    
    def convert_i2b(self, input_file, output_file):
        with open(input_file, 'r', encoding=self.encoding) as fi:
            tokens = fi.read()
            try:
                start_idx = tokens.index(self.start_string) + len(self.start_string)
                end_idx = tokens.index(self.end_string)
            except:
                raise Exception("error: Syntax Error\n\t"
                    f"check the content of your script file: {input_file}\n"
                    f"the content of {self.lang_name} script must start with \"{self.start_string}\" "
                    f"and end with \"{self.end_string}\".")
            tokens = tokens[start_idx:end_idx]
        
        op_dict = {
            self.inc_ptr_op     : '>', 
            self.dec_ptr_op     : '<', 
            self.inc_val_op     : '+', 
            self.dec_val_op     : '-',
            self.print_op       : '.', 
            self.store_op       : ',', 
            self.loop_begin_op  : '[', 
            self.loop_end_op    : ']'
        }
        with open(output_file, 'w') as fb:
            ind = 0
            while ind < len(tokens):
                is_unknown = True
                for operator_str in op_dict:
                    if tokens[ind] == operator_str[0]:
                        if tokens[ind:ind+len(operator_str)] == operator_str:
                            fb.write(op_dict[operator_str])
                            ind += len(operator_str)
                            is_unknown = False
                            break
                if is_unknown: ind += 1
