from AssemblerV2 import AssemblerV2
from CPU import Register, Operand, Flags, Registers, Instruction, Instructions
from Memory import Memory, Segment
from Dbg import dbg
from enum import Enum
class EmulatorV1:
    def __init__(self, assembler_obj :AssemblerV2) -> None:
        """Create a new emulator object from an assembler

        Args:
            assembler_obj (AssemblerV2): your assembler
        """
        self.regs :Registers = Registers()
        self.flags :Flags = Flags()
        self.memory :Memory = assembler_obj.memory
        self.symbol_map = assembler_obj.symbol_map
        self.regs[Register.PC] = 0
        self.regs[Register.AR] = 0
        
        self.is_halted = False
    
    def read_pc_offset(self, idx):
        return self.memory[Segment.CODE][self.regs[Register.PC] + idx]
    
    def execute(self, instruction):
        match instruction:
            case Instructions.NONE:
                self.is_halted = True
            case Instructions.HALT:
                self.is_halted = True
                
            case Instructions.JMP:
                label_idx = self.memory[Segment.CODE][self.regs[Register.PC] + 2]
                label_name = self.symbol_map.get_symbol_name_from_index(label_idx)
                label_location = self.symbol_map.get_symbol(label_name)
                dbg(f"jumping to {label_location}")
                self.regs[Register.PC] = label_location
                self.regs[Register.AR] = self.regs[Register.PC]
                return

            case Instructions.MOV:
                op_type1 :Operand = Operand.from_value(self.read_pc_offset(1))
                op_type2 :Operand = Operand.from_value(self.read_pc_offset(2))
                op1 :int = self.read_pc_offset(3)
                op2 :int = self.read_pc_offset(4)
                if op_type1 == Operand.REGISTER:
                    reg :Register = Register.from_index(op1)
                    if op_type2 == Operand.REGISTER or Operand.ADDRESS or Operand.INTEGER:
                        self.regs[reg] = op2
                    elif op_type2 == Operand.VALUE:
                        location = self.symbol_map.get_symbol(self.symbol_map.get_symbol_name_from_index(op2))
                        value = self.memory[Segment.DATA][location]
                        self.regs[reg] = value

                
        if not self.is_halted:
            self.regs[Register.PC] += (1 + instruction.value.nargs*2)
            self.regs[Register.AR] = self.regs[Register.PC]
        
    def cycle(self):
        while input("stop ? ") != "stop":
            if self.is_halted:
                break
            inst :int = self.memory[Segment.CODE][self.regs[Register.AR]]
            dbg(f"Executing instruction {inst} at address {self.regs[Register.AR]}")
            inst :Enum[Instruction] = Instructions.from_index(inst)
            self.execute(inst)
            
        print("================[DUMP]=========================")
        for i,value in enumerate(self.regs):
            reg :Register = Register.from_index(i)
            print(f"{reg.name} {value}")
        print("Halt = Exiting")
        exit()
        
        
        
import argparse
import sys
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OpenArchitecture Assembler', description="Assembler of an open architecture")
    parser.add_argument('filein', help="your microcode file which contains instructions")
    args = parser.parse_args(sys.argv[1:])
    print("================[ASSEMBLER]====================")
    assm :AssemblerV2 = AssemblerV2(args.filein)
    emu :EmulatorV1 = EmulatorV1(assm)
    print("================[MEMORY DUMP]==================")
    print(emu.memory.hexdump(emu.memory.code.memory, 16, 0, 20))
    print(emu.memory.hexdump(emu.memory.data.memory, 16, 0, 10))
    print("================[Symbol Table]=================")
    emu.symbol_map.quick_dump()
    print("================[CPU START]====================")
    emu.cycle()