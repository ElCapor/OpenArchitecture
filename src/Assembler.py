from typing import List, Dict, Type
from Dbg import dbg, dbgassert
from CPU import Register, Symbol, Instructions, Instruction, Operand
from Memory import Memory, Segment
from SymbolMap import SymbolMap


class BlockParser:
    """Parse a assembly file into blocks 
    """
    def __init__(self, filein):
        self.Blocks :List[List[str]] = [] # A block is just a list of instructions
        self.fileint = filein
        self.filedata :List[str] = self.parse_blocks(filein)
        
    def parse_blocks(self, filein):
        try:
            with open(filein, 'r') as file:
                lines = file.readlines()
                
                blocks = []
                current_block = []

                for line in lines:
                    if not line.strip():
                        if current_block:
                            blocks.append(current_block)
                            current_block = []
                    else:
                        current_block.append(line.strip())

                # Add the last block if there is one
                if current_block:
                    blocks.append(current_block)

                self.Blocks = blocks
                file.close()
        except FileNotFoundError:
            print(f"The file {filein} is not in scope.")
            exit()

class Assembler:
    def __init__(self, microcode) -> None:
        """Create a new Assembler object

        Args:
            microcode : the path of the file containing the asm code
        """
        self.ln = 0 # current line in file
        self.symbol_table :Dict[str, List[int, int]] = {} # symbol table stores the name of the symbol + the type and place in memory
        self.memory = Memory()
        self.is_symbol_table_ready = False
        self.parser = BlockParser(microcode)
        self.symbol_map = SymbolMap(self.memory)
        self.code_blocks_queued :List[int] = [] # the queued code blocks to treat
        self.process_blocks()
        #self.tokenizer(microcode)    

    def strip_comments(self, block :List[str]):
        ret = []
        for line in block:
            if line[0] != ";" and ";" in line:
                line = line.split(";")[0]
            elif line[0] == ";":
                continue
            ret.append(line)
        return ret
    
    def tokenize_line(self, line):
        return line.strip().replace("\t", ' ').split(' ')
    
    def check_d_type(self, token :str):
        return token in ["db", "ds", "di", "dd", "dc"]
    
    def typ2symbol(self, typ :str):
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
    # return the memory location
    def parse_code_block(self, block :List[str]) -> int:
        opcodes = [] #  opcodes of the current block
        for line in block:
            tokens = self.tokenize_line(line)
            tokens = self.remove_comma(tokens)
            inst :Instruction= self.token2instruction(tokens[0])
            dbgassert((len(tokens) -1) == inst.nargs, f"Instruction {tokens[0]} expected {inst.nargs} arguments, but only {len(tokens) - 1} were given")
            if len(tokens) > 1:
                for i in range(1, len(tokens)):
                    typ = self.token2type(tokens[i])
                    if typ.value & inst.operand_types[i-1]:
                        pass
                    else:
                        dbg(f"Have type {typ}, expected {inst.operand_types[i-1]}")
            else:
                return
        
        
    def populate_symbol_table(self, block):
        if self.is_symbol_declaration(self.tokenize_line(block[0])[0]) and len(self.tokenize_line(block[0])) == 1:
            self.symbol_map.add_symbol(Symbol.LABEL, block[0][0:-1], -1) # -1 because not initialized yet
            return

        for line in block:
            tokens = self.tokenize_line(line)
            dbg(tokens)
            sym_name = tokens[0]
            if self.is_symbol_declaration(sym_name):
                typ = tokens[1]
                if self.check_d_type(typ):
                    sym :Symbol = self.typ2symbol(typ)
                    value :str= tokens[2]
                    if value.startswith("0x"):
                        value = int(value, 16)
                    self.symbol_map.add_symbol(sym, sym_name[0:-1], int(value))
                    
    def process_blocks(self):
        for block in self.parser.Blocks:
            dbg(block)
            block = self.strip_comments(block)
            self.populate_symbol_table(block)
        dbg(self.symbol_map.symbol_table)     
               
    """ Each line of the file is delimited by a space and checked if it is empty, then passed to the token parser. """
    def tokenizer(self, fn):
        try:
            with open(fn, 'r') as file:
                for line in file.readlines():
                    self.ln += 1
                    tokens : List[str] = line.strip().replace("\t", ' ').split(' ')
                    if tokens and tokens != ['']:
                        self.parse_tokens(tokens)
        except FileNotFoundError:
            print(f"The file {fn} is not in scope.")
            exit()
            
    def is_instruction(self, token) -> bool:
        for tType in Instructions:
            if tType.name == token:
                return True
        return False
    
    def is_symbol_declaration(self, token :str) -> bool:
        return ':' in token
    
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
    
    def remove_comma(self, tokens :List[str]) -> List[str]:
        ret = []
        for token in tokens:
            if token== ",":
                pass
            elif token[-1] == ",": # a single comma can trigger this too , so we supress it first
                ret.append(token[:-1])
            else:
                ret.append(token)
        dbg(ret)
        return ret
    
    def is_register(self, token :str):
        for tType in Register:
            if tType.name == token:
                return True
        return False
    
    def token2register(self, token :str) -> Register:
        if self.is_register(token):
            return Instructions[token]
    
    def register2opcode(self, reg: str):
        return list(Register).index(self.token2register(reg))
    
    def parse_args(self, inst: Instruction, tokens :List[str]):
        dbg(f"Parsing args {tokens}")
        
    def write_instruction(self, inst : Instruction, tokens :List[str]):
        dbg(f"Writing instruction {tokens[0]}")
        opcodes = []
        opcodes.extend([self.instruction2opcode(tokens[0])])
        if inst.nargs > 0:
            self.parse_args(inst, tokens[1:])
        else:
            return
        
    def parse_instruction(self, tokens) -> bool:
        """Parse an instruction based on the given tokens

        Args:
            tokens (List[str]): Tokens

        Returns:
            bool: Parse successfull or not
        """
        dbg(tokens)
        inst :Instruction= self.token2instruction(tokens[0])
        dbgassert((len(tokens) -1) == inst.nargs, f"Instruction {tokens[0]} expected {inst.nargs} arguments, but only {len(tokens) - 1} were given")
        self.write_instruction(inst, tokens)
    
    def parse_symbol(self, tokens) -> bool:
        return False
    
    # i should parse symbols before instructions
    def parse_tokens(self, tokens :List[str]):
        t1 :str = tokens[0] # the instruction
        if self.is_instruction(t1):
            self.parse_instruction(self.remove_comma(tokens))
        elif self.is_symbol_declaration(t1):
            pass
        else:
            print(f"Unknown token {t1}")
            

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OpenArchitecture Assembler', description="Assembler of an open architecture")
    parser.add_argument('filein', help="your microcode file which contains instructions")
    args = parser.parse_args(sys.argv[1:])
    assm :Assembler = Assembler(args.filein)