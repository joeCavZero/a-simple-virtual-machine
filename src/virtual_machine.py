import time

registers_id = {
    "$zero": 0,
    "$a": 1,
    "$b": 2,
    "$c": 3,
    "$d": 4,
    "$e": 5,
    "$f": 6,
    "$g": 7,
    "$h": 8,
    "$i": 9,
    "$j": 10,
    "$k": 11,
    "$l": 12,
    "$m": 13,
    "$n": 14,
    "$o": 15,
    "$p": 16,
    "$q": 17,
    "$r": 18,
    "$s": 19,
    "$t": 20,
    "$u": 21,
    "$v": 22,
    "$w": 23,
    "$x": 24,
    "$y": 25,
    "$z": 26,
}

class VirtualMachine:
    def __init__(self, path: str):
        self.path = path
        self.registers = [0] * 32
        self.stack = [0] * 1024
        self.symbol_table: dict[str, int] = {}
        self.memory: list[list[str]] = []
        self.pc = 0
        self.sp = 0

    def run(self):
        self.load_memory()
        self.load_symbol_table()
        self.substitute_labels()
        
        self.process()

        print(self.memory)
        print(self.symbol_table)
    
    def load_memory(self):
        with open(self.path, 'r') as file:
            last_label: str = ""
            while True:
                line: str = file.readline()
                if line == "":
                    break
                
                processed_line = self.process_spaces(line)
                
                if processed_line != "":
                    aux = processed_line.split(sep=" ")
                    save = True
                    if aux[0][-1] == ":" and len(aux) == 1:
                        last_label = aux[0]
                        save = False
                    if save == True:
                        if last_label != "":
                            aux.insert(0,last_label)
                            last_label = ""
                            self.memory.append(aux)
                        else:
                            self.memory.append(aux)
                    

            file.close()

    def load_symbol_table(self):
        for index in range(len(self.memory)):
            first_expr = self.memory[index][0]
            if first_expr[-1] == ":":
                label = first_expr[:-1]
                self.symbol_table[label] = index
                self.memory[index].pop(0)

    def substitute_labels(self):
        for command_i in range( len(self.memory) ):
            command = self.memory[command_i]
            operation = command[0]
            match operation:
                case "jump":
                    label = command[1]
                    self.memory[command_i][1] = str(self.symbol_table[label] - command_i)
                case "jeq":
                    label = command[3]
                    self.memory[command_i][3] = str(self.symbol_table[label] - command_i)
    def process(self):
        while self.pc < len(self.memory):
            command: list[str] = self.memory[self.pc]
            operation: str = command[0]
            A: int = 0
            B: int = 0
            C: int = 0

            if len(command) >= 2:
                if command[1][0] == "$":
                    A = self.get_register_id(command[1])
                else:
                    A = int(command[1])

            if len(command) >= 3:
                if command[2][0] == "$":
                    B = self.get_register_id(command[2])
                else:
                    B = int(command[2])
            
            if len(command) >= 4:
                if command[3][0] == "$":
                    C = self.get_register_id(command[3])
                else:
                    C = int(command[3])

            self.execute(operation, A, B, C)

    def execute(self, operation: str, A: int, B: int, C: int):
        match operation:
            case "loadi":
                self.registers[A] = B
                self.pc+=1
            case "jump":
                self.pc += A
            case "jeq":
                if self.registers[A] == self.registers[B]:
                    self.pc += C
                else:
                    pc += 1
            case "sleepi":
                time.sleep(A)
                self.pc += 1
            case "add":
                self.registers[A] = self.registers[B] + self.registers[C]
                self.pc+=1
            case "addi":
                self.registers[A] = self.registers[B] + C
                self.pc+=1
            case "sub":
                self.registers[A] = self.registers[B] - self.registers[C]
                self.pc+=1
            case "subi":
                self.registers[A] = self.registers[B] - C
                self.pc+=1
            case "mul":
                self.registers[A] = self.registers[B] * self.registers[C]
                self.pc+=1
            case "div":
                self.registers[A] = self.registers[B] // self.registers[C]
                self.pc+=1
            case "mv":
                self.registers[A] = self.registers[B]
                self.pc+=1
            case "print":
                print(self.registers[A])
                self.pc+=1
            case "halt":
                exit()
    def process_spaces(self, line:str)->str:
        aux: str = ""
        is_command_started: bool = False

        for i in range(len(line)):
            char: str = line[i]
            next_char: str = ""
            char_to_add: str = ""

            if i+1 < len(line):
                next_char = line[i+1]
            
            if char != " ":
                is_command_started = True
            
            if is_command_started:
                if char == " " and next_char == " " or char == "\n":
                    pass
                else:
                    char_to_add = char
            
            aux += char_to_add
        return aux
    
    def get_register_id(self, register: str)->int:
        return registers_id[register]