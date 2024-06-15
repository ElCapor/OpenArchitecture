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

| Name | Index | Description          | x86 equivalent | Usage                                                |
| ---- | ----- | -------------------- | -------------- | ---------------------------------------------------- |
| PC   | 0     | Program Counter      | EIP            | Stores the next instruction to be executed           |
| ST   | 1     | Stack Top            | SP             | Stores the index to the top of the stack             |
| SB   | 2     | Stack Bottom         | BP             | Stores the inedx to the bottom of the stack          |
| FT   | 3     | Frame Top            | no             | Stores the index of the top of current stack frame   |
| FB   | 4     | Frame Bottom         | no             | Store the index of the bottom of current stack frame |
| DS   | 5     | Symbols Region Start | DS             | Store the index of the top of symbols region         |
| DE   | 6     | Symbols Region End   | no             | Store the index of the bottom of symbols region      |
| CT   | 7     | Code section top     | CS             | Store the top of the code memory region              |
| CB   | 8     | Code section Bottom  | CS             | Store the bottom of the code memory region           |

## CPU Flags
| Name | Index | Description | x86 equivalent  | Usage                                                                          |
| ---- | ----- | ----------- | --------------- | ------------------------------------------------------------------------------ |
| S    | 0     | Stop Flag   | No (maybe TF ?) | If set to 1 emulation is halted                                                |
| ZF   | 1     | Zero Flag   | ZF              | Set if the result of the preceding operation is 0                              |
| PF   | 2     | Parity Flag | PF              | Set if the number of set bits in the least significant byte is a multiple of 2 |
| SF   | 3     | Sign Flag   | SF              | Set if the result of an operation is negative                                  |

## CPU Instructions
Internal means that the instruction is not accessible to the user. For example, all the MOV** Instructions are just compile time generated instructions when you write MOV op1, op2

Note 1 : MOVA* instructions only support symbols for now, but soon it will support manual addresses through specialized registers


| Name     | Index  | Description                            | x86 equivalent | Usage                 | Internal |
| -------- | ------ | -------------------------------------- | -------------- | --------------------- | -------- |
| HALT     | 0      | Stop Execution                         | no             | Halt the execution    | no       |
| Reserved | [1:20] | Reserved Instructions                  | no             | no                    | no       |
| MOVXA    | 21     | Move Address of symbol into register   | mov            | MOV reg, symbol       | yes      |
| MOVXI    | 22     | Move Integer into register             | mov            | MOV reg, 12           | yes      |
| MOVXV    | 23     | Move value of symbol into register     | mov            | MOV reg, [symbol]     | yes      |
| MOVXX    | 24     | Move content of register into another  | mov            | MOV reg1, reg2        | yes      |
| MOVSA    | 25     | Move address of symbol into an symbol | mov            | MOV symbol, symbol2   | yes      |
| MOVSI    | 26     | Mov integer into symbol               | mov            | mov symbol, 12        | yes      |
| MOVSV    | 27     | Mov value of symbol into symbol       | mov            | mov symbol, [symbol2] | yes      |
| MOVSX    | 28     | Mov content of register into symbol   | mov            | mov symbol, x0        | yes      |
| MOVAS    | 25     | Move address of symbol into an address | mov            | MOV symbol, symbol2   | yes      |
| MOVAI    | 26     | Mov integer into address               | mov            | mov symbol, 12        | yes      |
| MOVAV    | 27     | Mov value of symbol into address       | mov            | mov symbol, [symbol2] | yes      |
| MOVAX    | 28     | Mov content of register into address   | mov            | mov symbol, x0        | yes      |

# UML Diagram