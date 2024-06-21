from typing import List, Dict
from enum import Enum
from Dbg import dbg, dbgassert

class Segment(Enum):
    STACK,DATA,CODE = range(0,3)

# A stack is just a special memory that can hold frames and local variables
class Stack:
    def __init__(self, size :int):
        self.size = size
        self.memory : List[int] = [0 for i in range(0, size)]
    
    def __getitem__(self, index :int | slice):
        if isinstance(index, slice):
            if (index.step and index.step > 1):
                raise IndexError()
            if (index.start >= 0 and index.stop < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        elif isinstance(index, int):
            if (index >= 0 and index < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        else:
            raise IndexError()
    
    def __setitem__(self, index :int, value :int):
        if (index >= 0 and index < self.size):
            self.memory[index] = value
        else:
            raise IndexError()
            
        
class DataSegment:
    def __init__(self, size :int):
        self.size = size
        self.memory :List[int] = [0 for i in range(0, size)]
    
    def __getitem__(self, index :int | slice):
        if isinstance(index, slice):
            if (index.step and index.step > 1):
                raise IndexError()
            if (index.start >= 0 and index.stop < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        elif isinstance(index, int):
            if (index >= 0 and index < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        else:
            raise IndexError()
    
    def __setitem__(self, index :int, value :int):
        if (index >= 0 and index < self.size):
            self.memory[index] = value
        else:
            raise IndexError()

class CodeSegment:
    def __init__(self, size :int):
        self.size = size
        self.memory :List[int] = [0 for i in range(0, size)]
    
    def __getitem__(self, index :int | slice):
        if isinstance(index, slice):
            if (index.step and index.step > 1):
                raise IndexError()
            if (index.start >= 0 and index.stop < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        elif isinstance(index, int):
            if (index >= 0 and index < self.size):
                return self.memory[index]
            else:
                raise IndexError()
        else:
            raise IndexError()
    
    def __setitem__(self, index :int, value :int):
        if (index >= 0 and index < self.size):
            self.memory[index] = value
        else:
            raise IndexError()
        
class Memory:
    def __init__(self, stack_size :int = 256, data_size :int = 1024, code_size :int = 4096) -> None:        
        self.stack = Stack(stack_size)
        self.data = DataSegment(data_size)
        self.code = CodeSegment(code_size)
        self.stack_selector = 0
        self.data_selector = 0
        self.code_selector = 0
    
    def __getitem__(self, segment :Segment) -> Stack | DataSegment | CodeSegment:
        match segment:
            case Segment.STACK:
                return self.stack
            case Segment.DATA:
                return self.data
            case Segment.CODE:
                return self.code
        raise IndexError()
    
    def __setitem__(self, segment :Segment, value :List[int]) -> None:
        match segment:
            case Segment.STACK:
                self.stack.__setitem__(value[0], value[1])
            case Segment.DATA:
                self.data.__setitem__(value[0], value[1])
            case Segment.CODE:
                self.code.__setitem__(value[0], value[1])
                    
    def write(self, segment :Segment, index :int, value :int):
        self.__setitem__(segment, [index, value])
    
    def write_array(self, segment :Segment, index :int, values :List[int]):
        idx = index
        for value in values:
            self.write(segment, idx, value)
            idx+=1
        
    def read(self, segment :Segment, index: int) -> int:
        return self.__getitem__(segment)[index]
    
    def read_array(self, segment :Segment, index :int, size :int) -> List[int]:
        return self.__getitem__(segment)[index:index+size]
    # returns a location in the given segment that has enough size
    def _alloc(self, segment :Segment, size :int):
        block = [0 for i in range(0, size)] # search block by blocks
        selector = self.stack_selector if segment == Segment.STACK else self.data_selector if segment == Segment.DATA else self.code_selector
        current_segment = self.stack if segment == Segment.STACK else self.data if segment == Segment.DATA else self.code
        while not self.read_array(segment, selector, size) == block:
            dbg(f" Reading block at index {selector}, searching for {block}, got {self.read_array(segment, selector, size)}")
            selector += 1
            if selector + size > current_segment.size:
                dbg("Buffer overflow be careful ", selector)
                break
        return selector
    
    def _reserve(self, segment :Segment, size :int) -> int:
        """Allocate and reserve a memory block for later usage

        Args:
            segment (Segment): the target segment
            size (int): size of the block
        Returns:
            The reserved location
        """
        block = self._alloc(segment, size)
        self.write_array(segment, block, [0xCC for i in range(size)]) # OxCC means the block is reserved
        return block
    

    def hexdump(self, memory, width=16, index=0, max_size=None):
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        if max_size is not None:
            memory = memory[index:index + max_size]
        else:
            memory = memory[index:]

        lines = []
        for i, chunk in enumerate(chunker(memory, width)):
            hex_values = ' '.join(f'{byte:02X}' for byte in chunk)
            ascii_values = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk)
            lines.append(f'{index + i * width:08X}  {hex_values:<{width * 3}}  {ascii_values}')

        return '\n'.join(lines)
    
def UnitTestMemory():
    mem :Memory = Memory()
    mem.write_array(Segment.DATA, 0, [10, 30, 45, 78])
    print(mem._alloc(Segment.DATA, 5))