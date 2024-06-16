from typing import List, Dict
from enum import Enum

class Segment(Enum):
    STACK,DATA,CODE = range(0,3)

# A stack is just a special memory that can hold frames and local variables
class Stack:
    def __init__(self, size :int):
        self.size = size
        self.memory : Dict[int, int] = {}
    
    def __getitem__(self, index :int):
        if (index >= 0 and index < self.size):
            return self.memory[index]
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
    
    def __getitem__(self, index :int):
        if (index >= 0 and index < self.size):
            return self.memory[index]
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
    
    def __getitem__(self, index :int):
        if (index >= 0 and index < self.size):
            return self.memory[index]
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
    
    def __getitem__(self, segment :Segment) -> Stack | DataSegment | CodeSegment:
        match segment:
            case Segment.STACK:
                return self.stack
            case Segment.DATA:
                return self.data
            case Segment.CODE:
                return self.code
        raise IndexError()
    
    def __setitem__(self, segment :Segment, value :List[int,int]) -> None:
        match segment:
            case Segment.STACK:
                self.stack.__setitem__(value[0], value[1])
            case Segment.DATA:
                self.data.__setitem__(value[0], value[1])
            case Segment.CODE:
                self.code.__setitem__(value[0], value[1])
        raise IndexError()
        