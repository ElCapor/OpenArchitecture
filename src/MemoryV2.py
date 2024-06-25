from typing import List, Dict
from enum import Enum
from Dbg import dbg, dbgassert

class Segment(Enum):
    STACK,DATA,CODE=range(0,3)

class MemoryBlockState(Enum):
    FREE,COMMITED,RESERVED,PRIVATE = range(0,4)

class MemoryBlock:
    def __init__(self, index :int, size :int, state : MemoryBlockState):
        self.index = index
        self.size = size
        self.state = state
        
    def __repr__(self) -> str:
        return f"MemoryBlock({self.index}, {self.size}, {self.state.name})"
        
    def Relocate(self, newindex :int):
        self.index = newindex
    
    def Resize(self, newsize :int):
        self.size = newsize
        
    def __eq__(self, value: object) -> bool:
        match type(value):
            case MemoryBlock:
                return self.index == value.index and self.size == value.size and self.state.value == value.state.value
        
        raise ArithmeticError()
    
        
    
class MemorySegment:
    def __init__(self, size :int) -> None:
        self.size = size
        self.memory :List[int] = [0 for i in range(0, size)]
        self.memory_blocks :List[MemoryBlock] = [MemoryBlock(0, size, MemoryBlockState.FREE)]
    
    def get_blocks(self, index, size) -> List[MemoryBlock]:
        """Get the blocks that occupy the range from index to index+size

        Args:
            index (int): your index
            size (int): size of your data
        """
        blocks = []
        for block in self.memory_blocks:
            dbg(f"{index};{index+size} == {block.index};{block.index+block.size}")
            if index >= block.index and index+size <= block.index + block.size:
                blocks.append(block) # push the last block
                return blocks # return all
            elif index >= block.index and index+size > block.index + block.size: # get the next block
                index+=block.size # rebase the index and size
                size-=block.size
                blocks.append(block) # we're inside this block, but there's another one next to us
                        
        return blocks

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
    
    def __setitem__(self, index :int, value :int | slice):
        if isinstance(index, slice):
            if (index.step and index.step > 1):
                raise IndexError()
            if (index.start >= 0 and index.stop < self.size):
                self.memory[index] = value
            else:
                raise IndexError()
        elif isinstance(index, int):
            if (index >= 0 and index < self.size):
                self.memory[index] = value
            else:
                raise IndexError()
        else:
            raise IndexError()
    
    def write(self, index, value):
        blocks = self.get_blocks(index, size)            
    
    # defragment memory segments
    def defragment(self):
        pass
    
    def _reserve(self, index :int, size :int):
        blocks :List[MemoryBlock] = self.get_blocks(index, size)
        for block in blocks:
            if block.state != MemoryBlockState.FREE:
                print("failed to reserve memory , block is not free")
                return
    
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

def MemoryV2UnitTests():
    seg = MemorySegment(32)
    seg.memory_blocks = [MemoryBlock(0, 8, MemoryBlockState.FREE), MemoryBlock(8, 8, MemoryBlockState.FREE), MemoryBlock(16, 8, MemoryBlockState.FREE), MemoryBlock(24, 8, MemoryBlockState.FREE)]
    blocks = seg.get_blocks(0, 24)
    assert  blocks == [MemoryBlock(0, 8, MemoryBlockState.FREE), MemoryBlock(8, 8, MemoryBlockState.FREE), MemoryBlock(16, 8, MemoryBlockState.FREE)], ("ERROR in get_blocks")
    

    
if __name__ == "__main__":
    MemoryV2UnitTests() 