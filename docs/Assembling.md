# Assembling

This is how the assembling of a program takes place :

## Basics
The whole program is divided into blocks. A block is either a series of instructions with a label OR a series of symbol declarations.
You can have as many blocks as you like and as many labels / instructions as you want. Just make sure to allocate enough memory
A program must start with the instruction JMP label, where label is where your main routine is. This is a convention because the emulator will always start reading code at the memory location 0

**Only one label per block allowed for now**

**Register Names are reserved symbols**

## Features
- Type check

## First Pass
All the comments are stripped as a first step.

Then , all the symbols get parsed in the first place, every symbol , except labels, are parsed, declared to the assembler and allocated in memory. The labels are saved in a global table but their code is not declared yet, to prevent the assembler for erroring when processing code that uses an undiscovered symbol. 

## Second Pass
Instructions are parsed and written in memory, labels get defined. At first, i though of writing the memory location of labels next to the corresponding instruction , for example JMP label , with label being at index 5 of memory would be written , 01 (MOV OpCode) 16 (Operand.SYMBOL) 05 (memory location). if the label's index in the symbol map is 2, then writing 01 16 02 would be better, as the emulator shares the same symbol map as the assembler, and allow it to retrieve the memory location at run time which is better since all the parsing would have been done, and we would get no unresolved symbol error.

## Third Pass
The emulator soon hopefully