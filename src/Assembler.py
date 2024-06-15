from typing import List, Dict

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
            

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OpenArchitecture Assembler', description="Assembler of an open architecture")
    parser.add_argument('filein', help="your microcode file which contains instructions")
    args = parser.parse_args(sys.argv[1:])
    assm :Assembler = Assembler(args.filein)