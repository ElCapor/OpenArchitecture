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
        self.symbol_table :Dict[str, int] = {}
        # store the type of each symbol
        self.symbol_type :Dict[str, Symbol] = {}
        
    def quick_dump(self):
        for i, symbol in enumerate(self.symbol_table):
            print(f"{i} {symbol} = {self.symbol_table[symbol]}")
    
    def get_symbol_index(self, name :str) -> int:
        return list(self.symbol_table.keys()).index(name)
    
    def get_symbol_name_from_index(self, index :int) -> int:
        try:
            return list(self.symbol_table.keys())[index]
        except IndexError:
            print(f"Failed to get symbol by index {index}")
            exit()
    
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
                return location
            # all of these are stored in data segment
            case Symbol.INTEGER | Symbol.SHORT | Symbol.DOUBLE | Symbol.BYTE | Symbol.STRING:
                return location
    
    def update_symbol(self, name :str, newvalue : int):
        self.symbol_table[name] = newvalue
    
    def add_symbol(self, symtype :Symbol, name :str, value :int | str):
        """Add a new symbol into the symbol table, if it's a label the value will be equal to the size of the block, that way we can correctly allocate size for it

        Args:
            symtype (Symbol): Type of the symbol
            name (str): name of the symbol
            value (int | str): value of the symbol
        """
        match symtype:
            case Symbol.INTEGER | Symbol.SHORT | Symbol.BYTE:
                location = self.mem._alloc(Segment.DATA, 1)
                self.symbol_type[name] = symtype
                self.symbol_table[name] = location
                self.mem[Segment.DATA][location] = value
            case Symbol.DOUBLE:
                location = self.mem._alloc(Segment.DATA, 2)
                self.symbol_type[name] = symtype
                self.symbol_table[name] = location
                self.mem[Segment.DATA][location] = value
            case Symbol.STRING:
                dbg("Not ready yet")
            
            # the caller will provide us with the location inside code segment
            case Symbol.LABEL:
                self.symbol_type[name] = symtype
                self.symbol_table[name] = value
            
                