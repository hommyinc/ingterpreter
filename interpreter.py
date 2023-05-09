import msvcrt

class Ingtepreter:
    def __init__(self):
        self.start_string = '말이 너무 심해..'
        self.end_string = '캠 키우고 해라'

        self.inc_ptr_op = '예민하네 화났네'
        self.dec_ptr_op = '장난인데 왜 그래'
        self.inc_val_op = '진지하게 받지마'
        self.dec_val_op = '이 사람 좀 논란 있을듯 ㄷㄷ'
        self.print_op = '안 미안하네'
        self.store_op = '니 취팔러마'
        self.loop_begin_op = '~'
        self.loop_end_op = 'ㅗ'
        
        self.memory = [0 for i in range(32768)]
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

ing = Ingtepreter()
#ing.convert('helloworld.bf', 'helloworld.ing')
ing.load('tictactoe.ing')
ing.run()
