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
    POP x1
    JMP end

end:
    HALT