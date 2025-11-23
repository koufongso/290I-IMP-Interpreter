# write the fibonacci program using the IMP language

import imp_interpreter

program = """
TODO: write your fibonacci program here to compute the 10th Fibonacci number, the reuslt should be 55.
"""

interpreter = imp_interpreter.IMPInterpreter(program)
memory = {}
result = interpreter.run(memory)
print(f"The Fibonacci number at index {memory['n']} is {memory['a']}")