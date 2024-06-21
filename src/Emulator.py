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
    print(emu.memory.hexdump(emu.memory.code.memory, 16, 0, 10))
    print(emu.memory.hexdump(emu.memory.data.memory, 16, 0, 10))
    print("================[Symbol Table]=================")
    emu.symbol_map.quick_dump()
    print("================[CPU START]====================")
    
    emu.cycle()