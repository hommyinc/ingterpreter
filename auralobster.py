import msvcrt

class AuraLobster:
    def __init__(self):
        self.memory = [0 for i in range(32768)]
        self.pointer = 0
        self.pc = 0
        self.code = ''
        self.start_string = '뭐야 방금 아버지 식사하시는데 콩자반 안 집어 지셔서'
        self.end_string = '라고 하셨어'
        self.jump_to = {}

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
            if command == '~':
                stack.append(i)
            elif command == '!':
                if len(stack) == 0:
                    raise Exception("Syntax Error")
                self.jump_to[i] = stack.pop(-1)
                self.jump_to[self.jump_to[i]] = i

        if len(stack) > 0:
            raise Exception("Syntax Error")

    def jump(self, command):
        if command == '~' and self.memory[self.pointer] == 0:
            self.pc = self.jump_to[self.pc]
        elif command == '!' and self.memory[self.pointer] != 0:
            self.pc = self.jump_to[self.pc]
            

    def run(self):
        self.preprocess()
        
        while self.pc < len(self.code):
            command = self.code[self.pc]

            if command == '어':
                self.increase_pointer()
            elif command == '라':
                self.decrease_pointer()
            elif command == '랍':
                self.increase_value()
            elif command == '타':
                self.decrease_value()
            elif command == '스':
                self.print_value()
            elif command == '?':
                self.store_value()
            elif command == '~' or command == '!':
                self.jump(command)

            self.pc += 1

    def load(self, file_name:str):
        f = open(file_name, 'r')
        lines = f.read().replace('\n', '')
        f.close()
        if self.start_string in lines:
            start = lines.index(self.start_string) + 29
            if self.end_string in lines[start:]:
                end = lines.index(self.end_string)
        self.code = lines[start:end]

    def convert(self, input_file, output_file):
        f = open(input_file, 'r')
        lines = f.read().replace('\n', '')
        f.close()
        fw = open(output_file, 'w')
        fw.write(self.start_string + '\n\n')
        for command in lines:
            if command == '>':
                fw.write('어')
            elif command == '<':
                fw.write('라')
            elif command == '+':
                fw.write('랍')
            elif command == '-':
                fw.write('타')
            elif command == '.':
                fw.write('스')
            elif command == ',':
                fw.write('?')
            elif command == '[':
                fw.write('~')
            elif command == ']':
                fw.write('!')
        fw.write('\n\n' + self.end_string)

al = AuraLobster()
# al.convert('helloworld.bf', 'helloworld.auralob')
al.load('factorial.auralob')
al.run()
