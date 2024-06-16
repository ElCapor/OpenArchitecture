JMP start

first_var: db 1
second_var: ds 400
third_var: dd 0x400
forth_var: dc "Hello, World!"

struct c1 : [r=255, g=0, b=255, a=255]

start:
    MOV x0, [color::a]
    HALT