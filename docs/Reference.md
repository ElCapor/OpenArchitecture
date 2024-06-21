# OpenArchitecture Reference

# CPU Architecture
## Memory Layout
Note : Even if the size of the regions can be changed, this shouldn't have any side effect on the cpu, because the instructions will rely on the registers to get the start and end of each region

| Address Range | Description    | Usage                                                    |
| ------------- | -------------- | -------------------------------------------------------- |
| [0:255]       | Stack Region   | The memory region that contains the stack                |
| [256:1023]    | Symbols Region | The memory region that contains symbols and their values |
| [1024:inf]    | Code Region    | Holds all the instructions and code                      |

## General Registers
General Purpose Registers

| Name | Index | Description      | x86 equivalent | Usage                  |
| ---- | ----- | ---------------- | -------------- | ---------------------- |
| x0   | idk   | General register | GPR            | store any kind of data |

## Special Registers

| Name | Index | Description           | x86 equivalent | Usage                                                        |
| ---- | ----- | --------------------- | -------------- | ------------------------------------------------------------ |
| PC   | 0     | Program Counter       | EIP            | Stores the next instruction to be executed                   |
| AR   | 1     | Memory Address holder | no             | Stores the current address to read in memory  (= Memory Bus) |
| ST   | 2     | Stack Top             | SP             | Stores the index to the top of the stack                     |
| SB   | 3     | Stack Bottom          | BP             | Stores the inedx to the bottom of the stack                  |
| FT   | 4     | Frame Top             | no             | Stores the index of the top of current stack frame           |
| FB   | 5     | Frame Bottom          | no             | Store the index of the bottom of current stack frame         |
| DS   | 6     | Symbols Region Start  | DS             | Store the index of the top of symbols region                 |
| DE   | 7     | Symbols Region End    | no             | Store the index of the bottom of symbols region              |
| CT   | 8     | Code section top      | CS             | Store the top of the code memory region                      |
| CB   | 9     | Code section Bottom   | CS             | Store the bottom of the code memory region                   |

## CPU Flags
| Name | Index | Description | x86 equivalent  | Usage                                                                          |
| ---- | ----- | ----------- | --------------- | ------------------------------------------------------------------------------ |
| S    | 0     | Stop Flag   | No (maybe TF ?) | If set to 1 emulation is halted                                                |
| ZF   | 1     | Zero Flag   | ZF              | Set if the result of the preceding operation is 0                              |
| PF   | 2     | Parity Flag | PF              | Set if the number of set bits in the least significant byte is a multiple of 2 |
| SF   | 3     | Sign Flag   | SF              | Set if the result of an operation is negative                                  |

## CPU Instructions
Internal means that the instruction is not accessible to the user. For example, all the MOV** Instructions are just compile time generated instructions when you write MOV op1, op2

Instructions that take multiple form of operands, like MOV are written on Instruction.size + nargs*2 bytes, the first byte is the opcode , the next nargs opcodes specify the type of operand that was passed, and the next nargs bytes contains the arguments

NOTE : * HALT IS SET TO 1 , BECAUSE 0 MEANS EMPTY MEMORY BLOCK , AND THE RAM COULD OVERWRITE IT AT ANY MOMENT THINKING THAT IT'S FREE SPACE*

| Name     | Index  | Description                          | x86 equivalent | Usage              | Internal |
| -------- | ------ | ------------------------------------ | -------------- | ------------------ | -------- |
| HALT     | 1      | Stop Execution                       | no             | Halt the execution | no       |
| Reserved | [2:20] | Reserved Instructions                | no             | no                 | no       |
| ADD      | 21     | Add value to register/address/symbol | add            | add value          | no       |
| MOV      | 22     | Mov a value into a register          | mov            | mov fr             | no       |


# Code Implementation
Referene about the python implementation i made for this cpu

## Memory class
Store and handle the cpu memory

## Symbol Table class
Store and handle the symbols data

## Assembler
Convert use assembly into binary representation