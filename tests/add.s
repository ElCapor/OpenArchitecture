JMP start ; this is always the first instruction ;

; Declaring my symbols;
first_var: di 200

; This is a multiline comment
I can be on multiple lines first
then you can catch me ;
start:
    MOV x0, 12
    HALT

MOV x1, 12 ; this will be never executed but you can keep it ;

end:
    HALT