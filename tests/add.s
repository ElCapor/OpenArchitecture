JMP start ; this is always the first instruction ;

; Declaring my symbols;
first_var: di 200

; This is a multiline comment
I can be on multiple lines first
then you can catch me;
start:
    HALT

end:
    MOV x0, 12
    HALT