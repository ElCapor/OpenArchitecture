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
            dbg(block)
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
                          
    def process_symbol_blocks(self):
        for i, block in enumerate(self.parser.blocks):
            if self.blocktypes[i] == BlockType.LABEL:
                self.symbol_map.add_symbol(Symbol.LABEL, self.tokenize_line(block[0])[0][:-1], -1)
            elif self.blocktypes[i] == BlockType.DATA:
                pass

                
    def process_code_blocks(self):
        for i, block in enumerate(self.parser.blocks):
            if self.blocktypes[i] == BlockType.LABEL:
                label_name = self.tokenize_line(block[0])[:-1]
                
                pass
            elif self.blocktypes[i] == BlockType.CODE:
                pass
            else:
                pass
                
    def process_blocks(self):
        self.guess_block_types()
        self.process_symbol_blocks()
        dbg(self.parser.blocks)
        dbg(self.blocktypes)
        dbg(self.symbol_map.symbol_table)
        
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OpenArchitecture Assembler', description="Assembler of an open architecture")
    parser.add_argument('filein', help="your microcode file which contains instructions")
    args = parser.parse_args(sys.argv[1:])
    assm :AssemblerV2 = AssemblerV2(args.filein)