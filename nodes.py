class Node:
    def __init__(self):
        pass

    def eval(self, memory: dict):
        pass

    def print(self):
        print(self.__str__())

    def __str__(self):
        return "Node"

class NodeSequence(Node):
    def __init__(self, first: Node, second: Node):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, memory: dict):
        self.first.eval(memory)
        self.second.eval(memory)

    def __str__(self):
        return f"({self.first.__str__()}; {self.second.__str__()})"

class NodeIndetifier(Node):
    def __init__(self, var_name):
        super().__init__()
        self.name = var_name
    
    def eval(self, memory: dict):
        return memory.get(self.name, KeyError(f"Variable '{self.name}' not found in memory"))
    
    def __str__(self):
        return f"({self.name})"


class NodeInteger(Node):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def eval(self, memory: dict):
        return self.value

    def __str__(self):
        return f"({self.value})"
    
class NodePlus(Node):
    def __init__(self, val1: Node, val2: Node):
        super().__init__()
        self.left = val1
        self.right = val2

    def eval(self, memory: dict):
        return self.left.eval(memory) + self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} + {self.right.__str__()})"
    
class NodeMinus(Node):
    def __init__(self, val1: Node, val2: Node):
        super().__init__()
        self.left = val1
        self.right = val2

    def eval(self, memory: dict):
        return self.left.eval(memory) - self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} - {self.right.__str__()})"
    
class NodeMultiply(Node):
    def __init__(self, val1: Node, val2: Node):
        super().__init__()
        self.left = val1
        self.right = val2

    def eval(self, memory: dict):
        return self.left.eval(memory) * self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} * {self.right.__str__()})"
    
class NodeNot(Node):
    def __init__(self, factor: Node):
        super().__init__()
        self.factor = factor

    def eval(self, memory: dict):
        return not self.factor.eval(memory)
    
    def __str__(self):
        return f"(not {self.factor.__str__()})"
    
class NodeBoolean(Node):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def eval(self, memory: dict):
        return self.value
    
    def __str__(self):
        return "(true)" if self.value else "(false)"
    
class NodeLessEqual(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, memory: dict):
        return self.left.eval(memory) <= self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} <= {self.right.__str__()})"
    
class NodeEqual(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, memory: dict):
        return self.left.eval(memory) == self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} = {self.right.__str__()})"

class NodeAnd(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, memory: dict):
        return self.left.eval(memory) and self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} and {self.right.__str__()})"
    
class NodeOr(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, memory: dict):
        return self.left.eval(memory) or self.right.eval(memory)
    
    def __str__(self):
        return f"({self.left.__str__()} or {self.right.__str__()})"
    
class NodeSkip(Node):
    def __init__(self):
        super().__init__()

    def eval(self, memory: dict):
        pass # skip does nothing

    def __str__(self):
        return "(skip)"
    
class NodeAssign(Node):
    def __init__(self, var_name: str, expr: Node):
        super().__init__()
        self.var_name = var_name
        self.expr = expr

    def eval(self, memory: dict):
        memory[self.var_name] = self.expr.eval(memory)
        return 
    
    def __str__(self):
        return f"({self.var_name} := {self.expr.__str__()})"
    
class NodeIf(Node):
    def __init__(self, condition: Node, then_branch: Node, else_branch: Node):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def eval(self, memory: dict):
        if self.condition.eval(memory):
            return self.then_branch.eval(memory)
        else:
            return self.else_branch.eval(memory)
        
    def __str__(self):
        return f"(if {self.condition.__str__()} then {self.then_branch.__str__()} else {self.else_branch.__str__()})"
        

class NodeWhile(Node):
    def __init__(self, condition: Node, body: Node):
        super().__init__()
        self.condition = condition
        self.body = body

    def eval(self, memory: dict):
        # create if node that represents while loop
        while self.condition.eval(memory): 
            self.body.eval(memory)

    def __str__(self):
        return f"(while {self.condition.__str__()} do {self.body.__str__()})"
