from typing import List, Dict
from Dbg import dbg, dbgassert
from CPU import Register, Symbol, Instructions, Instruction

class Assembler:
    def __init__(self, microcode) -> None:
        """Create a new Assembler object

        Args:
            microcode : the path of the file containing the asm code
        """
        self.ln = 0 # current line in file
        self.symbol_table :Dict[str, List[int, int]] = {} # symbol table stores the name of the symbol + the type and place in memory
        self.tokenizer(microcode)    
    
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
        
    
    def parse_symbol(self, tokens) -> bool:
        return False
            
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