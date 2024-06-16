from CPU import Symbol
from Memory import Memory, Segment
from typing import Dict
from Dbg import dbg, dbgassert
class SymbolMap():
    """Symbol Map to store information about program symbols
    """
    def __init__(self, mem :Memory) -> None:
        self.mem = mem
        # store the location of each symbol inside memory
        self.symbol_table :Dict[str, int]
        # store the type of each symbol
        self.symbol_type :Dict[str, Symbol]
    
    def get_symbol(self, name :str):
        if name not in self.symbol_table or name not in self.symbol_type:
            dbg("Symbol not found ", name)
            raise IndexError()
        typ :Symbol = self.symbol_type[name]
        location :int = self.symbol_table[name]
        match typ:
            # labels are stored in code
            # return the start of the label code
            case Symbol.LABEL:
                return self.mem[Segment.CODE][location]
            # all of these are stored in data segment
            case Symbol.INTEGER | Symbol.SHORT | Symbol.DOUBLE | Symbol.BYTE | Symbol.STRING:
                return self.mem[Segment.DATA][location]