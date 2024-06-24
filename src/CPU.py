from enum import Enum, auto, IntFlag
from typing import List
from Dbg import dbgassert,dbg
class Register(Enum):
    PC, AR, ST, SB, FT, FB, DS, DE, CT, CB = range(0,10)
    x0,x1,x2 = range(10, 13)
    
    def index(self):
        return list(Register).index(self)
    
    @staticmethod
    def from_index(index):
        return list(Register)[index]
    
    @staticmethod
    def from_name(name):
        return Register[name]

# symbol type
class Symbol(Enum):
    LABEL, BYTE, SHORT, INTEGER, DOUBLE, STRING = range(0,6)

class Operand(IntFlag):
    @staticmethod
    def from_value(value :int):
        for tType in Operand:
            if tType.value == value:
                return tType
        return Operand.NONE
    
    NONE = 0
    REGISTER = 1 << 0  # 1
    INTEGER  = 1 << 1  # 2
    VALUE    = 1 << 2  # 4
    ADDRESS  = 1 << 3  # 8
    SYMBOL   = 1 << 4  # 16
    ALL = REGISTER | INTEGER | VALUE | ADDRESS | SYMBOL
    
class Instruction:
    def __init__(self, nargs :int = 0, operand_types :List[Operand] = []):
        """Create a new instruction

        Args:
            size (int, optional): size of the instruction in bytes. Defaults to 1.
            nargs (int, optional): number of args for the instruction. Defaults to 0.
        """
        self.size = 1 + nargs * 2
        self.nargs = nargs
        self.operand_types : List[Operand]= operand_types
        dbgassert(len(self.operand_types) == nargs, "You must specify allowed operand types")
    
class Instructions(Enum):
    
    @staticmethod
    def from_index(index :int) -> Instruction:
        for tType in Instructions:
            if index == 0: return tType
            else: index -= 1
            
    NONE = Instruction()
    HALT = Instruction()
    JMP = Instruction(1, [Operand.SYMBOL])
    MOV = Instruction(2, [Operand.ALL, Operand.ALL])
    CMP = Instruction(2, [Operand.ALL, Operand.ALL])
    PUSH = Instruction(1, [Operand.ALL])
    POP = Instruction(1, [Operand.REGISTER])
    ADD = Instruction(2, [Operand.ALL, Operand.ALL])
    SUB = Instruction(2, [Operand.ALL, Operand.ALL])
    CALL = Instruction(1, [Operand.SYMBOL])
    ASSERT = Instruction(2, [Operand.ALL, Operand.ALL])
    
class Flag(Enum):
    S, ZF, PF, SF = range(0, 4)
    
class Flags:
    def __init__(self):
        self.flags :List[int] = [0 for i in range(0, len(Flag))]
    
    def __getitem__(self, flag :Flag) -> int:
        return self.flags[flag.value]

    def __setitem__(self, flag :Flag, value :int) -> int:
        self.flags[flag.value] = value % (2**1)

class Registers:
    def __init__(self):
        self.regs :List[int] = [0 for i in range(0, len(Register))]
    
    def __getitem__(self, register :Register | int) -> int:
        if isinstance(register, Register):
            return self.regs[register.value]
        elif isinstance(register, int):
            return self.regs[register]

    def __setitem__(self, register :Register | int, value :int) -> int:
        if isinstance(register, Register):
            self.regs[register.value] = value % (2**32)
        elif isinstance(register, int):
            self.regs[register] = value % (2**32)
        