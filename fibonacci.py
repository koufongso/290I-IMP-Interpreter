# write the fibonacci program using the IMP language

import imp_interpreter

program = """
n := 10;    
a := 0;           
b := 1;           
i := 0;          
while (i <= n) do
    if (i = 0) then
        a := 0
    else
        if (i = 1) then
            a := 1
        else
            temp := a;
            a := b;
            b := (temp + b)
        end
    end;
    i := (i + 1)
end
"""

interpreter = imp_interpreter.IMPInterpreter(program)
memory = {}
result = interpreter.run(memory)
print(f"The Fibonacci number at index {memory['n']} is {memory['a']}")