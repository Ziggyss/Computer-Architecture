"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.register = [0] * 8
        self.pc = 0
        self.sp = 0xF4
        self.inc_size = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        

    def ram_read(self, MAR):
            # return the value at the memory address 
            return self.ram[MAR]

    # MAR is the Memory Address Register (the address)
    # MDR is the Memory Data Register (the value)   

    def ram_write(self, MDR, MAR):
        # assign the value to the memory address location
        self.ram[MAR] = MDR

    def handle_ldi(self, operand_a, operand_b):
        self.register[operand_a] = operand_b
        self.inc_size = 3   

    def handle_prn(self, operand_a, operand_b):
        value = self.register[operand_a]
        print(value)
        self.inc_size = 2

    def handle_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.inc_size = 3

    def handle_hlt(self, operand_a, operand_b):
        sys.exit()  


    def handle_push(self, operand_a, operand_b):
        
        #Decrement the sp
        self.sp -= 1

        # Push the value in the register to the address pointed to by sp
        self.ram[self.sp] = self.register[operand_a]
        
        self.inc_size = 2      

    def handle_pop(self, operand_a, operand_b):
    
         # Pop the value at the top of the stack into the register
        self.register[operand_a] = self.ram[self.sp]
        # Increment the sp
        self.sp += 1

        self.inc_size = 2       

              
 

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # program = sys.argv[1]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # split line before and after comment symbol
                    comment_split = line.split("#")

                    # extract our number
                    num = comment_split[0].strip() # trim whitespace

                    if num == '':
                        continue # ignore blank lines

                    # convert our binary string to a number
                    x = int(num, 2)

                    # print the x in bin and dec
                    # print(f"{x:08b}: {x:d}")

                    self.ram_write(x, address)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        if op == "MUL":
           self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
        IR = self.ram[self.pc]
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]

        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)
                self.pc += self.inc_size 
            else:
                print("Invalid instruction")
                running = False   

        # self.pc += self.inc_size         


        #     if cmd == LDI:
        #         # read the values at the next two positions
        #         operand_a = self.ram[self.pc + 1]
        #         operand_b = self.ram[self.pc + 2]
        #         self.register[operand_a] = operand_b
        #         # bypass the three positions that have just been used to move to the next
        #         self.pc += 3

        #     elif cmd == PRN:
        #         register_index = self.ram[self.pc + 1]
        #         value = self.register[register_index]
        #         print(value)
        #         self.pc += 2

        #     elif cmd == MUL:
        #         operand_a = self.ram[self.pc + 1]
        #         operand_b = self.ram[self.pc + 2]
        #         self.alu("MUL", operand_a, operand_b)
        #         self.pc += 3 

        #     elif cmd == PUSH:
     
        #         reg = ram[pc + 1]
        #         val = register[reg]    
        #         register[sp] -= 1
        #         ram[register[sp]] = val
        
        # inc_size = 2
 
                         


        """Run the CPU."""
       

   
# cpu = CPU()
# cpu.load(program)

# cpu.run()

       
