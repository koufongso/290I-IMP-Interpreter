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
        # Hint: Execute the 'first' node, then execute the 'second' node.
        # Remember that commands modify 'memory' in place, they don't return values.
        raise NotImplementedError("Sequence evaluation not implemented yet.")

    def __str__(self):
        return f"({self.first.__str__()}; {self.second.__str__()})"

class NodeIdentifier(Node):
    def __init__(self, var_name):
        super().__init__()
        self.name = var_name
    
    def eval(self, memory: dict):
        # Hint: 'memory' is a dictionary. If the variable name (self.name)
        # is not in the dictionary, raise a KeyError or return a default value (like 0).
        raise NotImplementedError("Indentifier evaluation not implemented yet.")
    
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
        # TODO: implement the assignment  semantics
        # Hint: Evaluate the expression (self.expr) first.
        # Then, update the 'memory' dictionary: memory[key] = value
        raise NotImplementedError("Assignment evaluation not implemented yet.")
    
    def __str__(self):
        return f"({self.var_name} := {self.expr.__str__()})"
    
class NodeIf(Node):
    def __init__(self, condition: Node, then_branch: Node, else_branch: Node):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def eval(self, memory: dict):
        # TODO: implement the if condition semantics
        # Hint: If self.condition evaluates to True, run self.then_branch.
        # Otherwise, run self.else_branch.
        raise NotImplementedError("If evaluation not implemented yet.")
        
    def __str__(self):
        return f"(if {self.condition.__str__()} then {self.then_branch.__str__()} else {self.else_branch.__str__()})"
        

class NodeWhile(Node):
    def __init__(self, condition: Node, body: Node):
        super().__init__()
        self.condition = condition
        self.body = body

    def eval(self, memory: dict):
        # TODO: implement the while semantics
        # Requirement: Map <while b do c> to <if b then (c; while b do c) else skip>
        #
        # Steps:
        # 1. Create a NodeSequence that contains: (self.body) and (self).
        #    (Passing 'self' as the second part of the sequence creates the recursion!)
        # 2. Create a NodeIf:
        #      - condition: self.condition
        #      - then_branch: The NodeSequence you just created
        #      - else_branch: NodeSkip()
        # 3. Call .eval(memory) on that new NodeIf object.
        #
        # DO NOT use a python 'while' loop.
        raise NotImplementedError("While evaluation not implemented yet.")

    def __str__(self):
        return f"(while {self.condition.__str__()} do {self.body.__str__()})"
