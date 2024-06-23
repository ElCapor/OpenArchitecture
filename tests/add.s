JMP start ; this is always the first instruction ;

; Declaring my symbols;
first_var: di 200

; This is a multiline comment
I can be on multiple lines first
then you can catch me;
start:
    MOV x0, 12
    MOV x1, 14
    PUSH x0
    PUSH x1
    MOV x0, 20
    MOV x1, 6
    CALL func1
    JMP end

end:
    HALT

func1:
PUSH ST ;4;
MOV FT, ST
SUB FT, 3
PUSH x0
PUSH x1
MOV ST, FT
POP x0
ADD FT, 1
MOV ST, FT
POP x1
ADD FT, 1
MOV ST, FT ;reset st back to default;
POP ST
POP x2

