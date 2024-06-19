from enum import Enum, auto, IntFlag
from typing import List
from Dbg import dbgassert
class Register(Enum):
    PC, AR, ST, SB, FT, FB, DS, DE, CT, CB = range(0,10)
    x0,x1,x2 = range(10, 13)

# symbol type
class Symbol(Enum):
    LABEL, BYTE, SHORT, INTEGER, DOUBLE, STRING = range(0,6)

class Operand(IntFlag):
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
        self.size = 1 + nargs
        self.nargs = nargs
        self.operand_types : List[Operand]= operand_types
        dbgassert(len(self.operand_types) == nargs, "You must specify allowed operand types")
    
class Instructions(Enum):
    HALT = Instruction()
    JMP = Instruction(1, [Operand.SYMBOL])
    MOV = Instruction(2, [Operand.ALL, Operand.ALL])