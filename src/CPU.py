from enum import Enum, auto

class Register(Enum):
    PC, AR, ST, SB, FT, FB, DS, DE, CT, CB = range(0,10)

# symbol type
class Symbol(Enum):
    LABEL, BYTE, SHORT, INTEGER, DOUBLE, STRING = range(0,6)