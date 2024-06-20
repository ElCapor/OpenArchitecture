from typing import List, Dict, Type
from Dbg import dbg, dbgassert
from CPU import Register, Symbol, Instructions, Instruction, Operand
from Memory import Memory, Segment
from SymbolMap import SymbolMap
from enum import Enum

class BlockType(Enum):
    CODE, DATA, LABEL = range(0,3)

class BlockParser:
    """Parse and split a file into blocks
    """
    def __init__(self, filein):
        self.blocks :List[List[str]] = []
        self.filein = filein
        self.filedata :List[str] = self.parse_blocks()
        
    def strip_comments(self, block :List[str]):
        ret = []
        is_comment = False
        for i, line in enumerate(block):
            if line[0] ==  ";" and line[-1] == ";": # full line comment
                continue
            elif line.count(";") == 2:
                line = line.split(";", 1)[0].strip()
            elif line.count(";") == 1:
                if not is_comment:
                    is_comment = True
                else:
                    is_comment = False
                continue
            elif is_comment:
                continue
            
            ret.append(line)
        return ret
    
    def parse_blocks(self):
        try:
            with open(self.filein, 'r') as file:
                lines = file.readlines()
                
                blocks = []
                current_block = []

                for line in lines:
                    if not line.strip():
                        if current_block:
                            blocks.append(self.strip_comments(current_block))
                            current_block = []
                    else:
                        current_block.append(line.strip())

                # Add the last block if there is one
                if current_block:
                    blocks.append(self.strip_comments(current_block))

                self.blocks = blocks
                file.close()
            
        except FileNotFoundError:
            print(f"The file {self.filein} is not in scope.")
            exit()
            
class AssemblerV2:
    def __init__(self, file) -> None:
        self.parser :BlockParser = BlockParser(file)
        self.blocktypes :Dict[int, BlockType] = {}
        self.memory :Memory = Memory()
        self.symbol_map :SymbolMap = SymbolMap(self.memory)
        self.process_blocks()
    
    def tokenize_line(self, line):
        return line.strip().replace("\t", ' ').split(' ')
    
    def is_symbol_declaration(self, token :str):
        return ":" in token
    
    def is_instruction(self, token :str):
        for tInst in Instructions:
            if tInst.name == token:
                return True
        return False
    
    def guess_block_types(self):
        for i, block in enumerate(self.parser.blocks):
            #dbg(block)
            self.tokenize_line(block[0])[0]
            if self.is_symbol_declaration(self.tokenize_line(block[0])[0]):
                if len(self.tokenize_line(block[0])) > 1:
                    self.blocktypes[i] = BlockType.DATA
                else:
                    self.blocktypes[i] = BlockType.LABEL
                    
            elif self.is_instruction(self.tokenize_line(block[0])[0]):
                self.blocktypes[i] = BlockType.CODE
                
            else:
                print(f"Unknown block type {i}")
                exit()
    
    def symbol_type_to_symbol(self, typ :str):
        if typ == "db":
            return Symbol.BYTE
        elif typ == "ds":
            return Symbol.SHORT
        elif typ == "di":
            return Symbol.INTEGER
        elif typ == "dd":
            return Symbol.DOUBLE
        elif typ == "dc":
            return Symbol.STRING
        else:
            raise NotImplementedError()
    
    def is_symbol_type(self, typ :str):
        return typ in ["db", "di", "dd", "dc", "ds"]
    
    def process_data_block(self, block :str):
        for i, line in enumerate(block):
           tokens = self.tokenize_line(line)
           sym_name = tokens[0]
           if self.is_symbol_declaration(sym_name):
            try:
                typ = tokens[1]
                if self.is_symbol_type(typ):
                    sym :Symbol = self.symbol_type_to_symbol(typ)
                    value :str = tokens[2]
                    if value.startswith("0x"):
                        value = int(value, 16)
                    self.symbol_map.add_symbol(sym, sym_name[0:-1], int(value))
            except IndexError:
                print(f"Symbol {sym_name} was declared incorrectly")
                
    def process_symbol_blocks(self):
        for i, block in enumerate(self.parser.blocks):
            if self.blocktypes[i] == BlockType.LABEL:
                self.symbol_map.add_symbol(Symbol.LABEL, self.tokenize_line(block[0])[0][:-1], -1)
            elif self.blocktypes[i] == BlockType.DATA:
                self.process_data_block(block)

    def remove_comma(self, tokens :List[str]) -> List[str]:
        ret = []
        for token in tokens:
            if token== ",":
                pass
            elif token[-1] == ",": # a single comma can trigger this too , so we supress it first
                ret.append(token[:-1])
            else:
                ret.append(token)
        return ret
    
    def token2instruction(self, token :str) -> Instruction:
        for tType in Instructions:
            if tType.name == token:
                return tType.value
        raise IndexError()
    
    def instruction2name(self, inst :Instruction) -> str:
        for tType in Instructions:
            if tType.value == inst:
                return tType.name
        raise IndexError()
    
    def instruction2opcode(self, inst :str) -> int:
        idx :int = 0
        for tType in Instructions:
            if tType.name == inst:
                return idx
            idx += 1
    
    def is_register(self, token :str):
        for tType in Register:
            if tType.name == token:
                return True
        return False
    
    def is_value(self, token :str):
        return token[0] == "[" and token[-1] == "]"
    
    def is_symbol(self, token :str):
        return token in self.symbol_map.symbol_table
    
    def token2symboltype(self, token :str):
        return self.symbol_map.symbol_type[token]
    
    def token2type(self, token :str) -> None | Operand:
        if self.is_register(token):
            return Operand.REGISTER
        elif self.is_symbol(token):
            if self.is_value(token):
                return Operand.VALUE
            else:
                match self.token2symboltype(token):
                    case Symbol.LABEL:
                        return Operand.SYMBOL
                    case Symbol.BYTE | Symbol.INTEGER | Symbol.SHORT | Symbol.DOUBLE | Symbol.STRING:
                        return Operand.ADDRESS
        elif token.isdigit():
            return Operand.INTEGER
        else:
            return None
    
    def arg2opcode(self, typ :Operand, value :str) -> int:
        match typ:
            case Operand.REGISTER:
                return Register.from_name(value).index()
            case Operand.INTEGER:
                if value.startswith("0x"):
                    return int(value, 16)
                else:
                    return int(value)
            case Operand.VALUE:
                return self.symbol_map.get_symbol_index(value[1:-1])
            case Operand.ADDRESS: # i should add support for manual memory addresses in case u want to add a flag or unmanaged memory space
                return self.symbol_map.get_symbol_index(value)
            case Operand.SYMBOL:
                return self.symbol_map.get_symbol_index(value)
                
    
    # convert a block into a list of opcodes and instructions
    def block2opcode(self, block :List[str]) -> List[int]:
        opcodes = []
        for i,line in enumerate(block):
            tokens = self.tokenize_line(line)
            tokens = self.remove_comma(tokens)
            dbg(tokens)
            inst :Instruction = self.token2instruction(tokens[0])
            dbgassert((len(tokens) -1) == inst.nargs, f"Instruction {tokens[0]} expected {inst.nargs} arguments, but only {len(tokens) - 1} were given")
            if len(tokens) > 1:
                opcodes.append(self.instruction2opcode(tokens[0]))
                argtypes = []
                argvalues = []
                # argument checker and operand type writing
                for j in range(1, len(tokens)):

                    typ :Operand = self.token2type(tokens[j])
                    if typ.value & inst.operand_types[j-1]:
                        #dbg("Type check is cool asf today")
                        argtypes.append(typ.value)
                        argvalues.append(self.arg2opcode(typ, tokens[j]))
                        
                opcodes.extend(argtypes)
                opcodes.extend(argvalues)
            else:
                opcodes.append(self.instruction2opcode(tokens[0]))
                
            return opcodes

        
    def process_code_blocks(self):
        for i, block in enumerate(self.parser.blocks):
            if self.blocktypes[i] == BlockType.LABEL:
                label_name = self.tokenize_line(block[0])[0][:-1]
                opcodes = self.block2opcode(block[1:])
                location :int = self.memory._alloc(Segment.CODE, len(opcodes))
                self.memory.write_array(Segment.CODE, location, opcodes)
                self.symbol_map.update_symbol(label_name, location)
                dbg(opcodes)
                pass
            elif self.blocktypes[i] == BlockType.CODE:
                opcodes = self.block2opcode(block)
                location :int = self.memory._alloc(Segment.CODE, len(opcodes))
                self.memory.write_array(Segment.CODE, location, opcodes)
                dbg(opcodes)
                pass
            else:
                pass
                
    def process_blocks(self):
        self.guess_block_types()
        self.process_symbol_blocks()
        self.process_code_blocks()
        """
        dbg(self.parser.blocks)
        dbg(self.blocktypes)
        dbg(self.symbol_map.symbol_table)
        for symbol in self.symbol_map.symbol_table:
            dbg(self.symbol_map.get_symbol_name_from_index(self.symbol_map.get_symbol_index(symbol)))
        """
        
        
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OpenArchitecture Assembler', description="Assembler of an open architecture")
    parser.add_argument('filein', help="your microcode file which contains instructions")
    args = parser.parse_args(sys.argv[1:])
    assm :AssemblerV2 = AssemblerV2(args.filein)