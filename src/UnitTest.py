from Memory import UnitTestMemory
from AssemblerV2 import AssemblerV2
from Emulator import EmulatorV1
from Memory import Segment
import os, pathlib
from typing import Dict, List
from Dbg import dbg
import Dbg
Dbg.is_debug = False

unit_tests_folder :str = "\\tests"


def assert_memory(assm :AssemblerV2, segment :Segment, index :int, value :int|List[int]):
    red = assm.memory.read_array(segment, index, len(value))
    if  red == value:
        return True
    else:
        raise Exception(f"ASSERT_MEMORY Failed : Value at index {index} was {red}, expected {value}")

if __name__ == "__main__":
    print("=====================[ASSEMBLER UNIT TESTS]=========================")
    assm :AssemblerV2 = AssemblerV2("JMP start\n\n start:\n HALT\n")
    print(assm.memory.hexdump(assm.memory.code.memory, 16, 0, 10))
    assert_memory(assm, Segment.CODE, 0, [2, 16, 1])
    print("=====================| END ASSEMBLER TEST |=========================")
    cwd = os.getcwd()
    real = cwd + unit_tests_folder
    results : Dict[int, int] = {}
    for i, file in enumerate(os.listdir(real)):
        print(f"==========================[RUNNING UNIT TEST #{i} ({file})]==========================")
        try:
            assembler :AssemblerV2 = AssemblerV2(f"{real}\\{file}")
            emu :EmulatorV1 = EmulatorV1(assembler)
            emu.cycle()
            results[i] = 1
        except Exception as e:
            if isinstance(e, AssertionError):
                print("An assert failed")
                idk :AssertionError = e
                print(idk)
            else:
                print("An error occured ", e.with_traceback)
            results[i] = 0
    
    for result in results:
        print(f"TEST #{result} HAS {"FAILED" if results[result] == 0 else "SUCCEEDED"}")
    
    