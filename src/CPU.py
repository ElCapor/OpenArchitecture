from enum import Enum, auto
from typing import List
from Dbg import dbgassert
class Register(Enum):
    PC, AR, ST, SB, FT, FB, DS, DE, CT, CB = range(0,10)

# symbol type
class Symbol(Enum):
    LABEL, BYTE, SHORT, INTEGER, DOUBLE, STRING = range(0,6)

class Operand(Enum):
    REGISTER, INTEGER, VALUE, ADDRESS, SYMBOL = range(0, 5)
    
class Instruction:
    def __init__(self, nargs :int = 0, operand_types :List[Operand] = []):
        """Create a new instruction

        Args:
            size (int, optional): size of the instruction in bytes. Defaults to 1.
            nargs (int, optional): number of args for the instruction. Defaults to 0.
        """
        self.size = 1 + nargs
        self.nargs = nargs
        self.operand_types = operand_types
        dbgassert(len(self.operand_types) == nargs, "You must specify operand types")
    
class Instructions(Enum):
    HALT = Instruction()
    JMP = Instruction(1, [Operand.SYMBOL])