from token import TokenType, Token
import token
from lexer import Lexer
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.length = len(tokens)

    def parse(self):
        cst =  self.parse_Command()
        # it should reach the end of Command parsing
        if self._get_next_token() is not None:
            raise SyntaxError("Unexpected token after parsing Command")
        
        return cst

    def _has_next_token(self):
        return (self.pos + 1 < self.length)   

    def _get_next_token(self):
        return self.tokens[self.pos + 1] if self._has_next_token() else None
    
    def _advance(self):
        self.pos += 1
    
    def parse_AExpression(self):
        '''
        AExpression ::= INT | VAR | '(' AExpression '+/*/-' AExpression ')'
        '''
        token = self._get_next_token()
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing AExpression")
        
        if token.type == TokenType.INT:
            self._advance() # consume INT
            return NodeInteger(token.value)
        
        if token.type == TokenType.VAR:
            self._advance() # consume VAR
            return NodeIndetifier(token.value)
        
        if token.type == TokenType.LPAREN:
            self._advance() # consume '('
            left_node = self.parse_AExpression()
            op_token = self._get_next_token()
            if op_token is None or op_token.type not in {TokenType.PLUS, TokenType.MINUS, TokenType.MUL}:
                raise SyntaxError(f"Invalid operator {op_token} in AExpression")
            self._advance() # consume operator
            right_node = self.parse_AExpression()
            closing_token = self._get_next_token()
            if closing_token is None or closing_token.type != TokenType.RPAREN:
                raise SyntaxError("Expected ')' at the end of AExpression")
            self._advance() # consume ')'

            # valid expression, create corresponding node
            if op_token.type == TokenType.PLUS:
                return NodePlus(left_node, right_node)
            elif op_token.type == TokenType.MINUS:
                return NodeMinus(left_node, right_node)
            elif op_token.type == TokenType.MUL:
                return NodeMultiply(left_node, right_node)
            
        return None # we should not raise error here, since it may be part of BExpression

    def parse_BExpression(self):
        '''
        BExpression ::= 'true' | 'false' | '(' AExpression '<=/=' AExpression ')' | '(' BExpression 'and/or' BExpression ')' |  'not' '(' BExpression ')'
        '''
        token = self._get_next_token()
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing BExpression")
        
        if token.type == TokenType.TRUE:
            self._advance() # consume 'true'
            return NodeBoolean(True)
        
        if token.type == TokenType.FALSE:
            self._advance() # consume 'false'
            return NodeBoolean(False)
        
        if token.type == TokenType.NOT:
            self._advance() # consume 'not'
            if self._get_next_token() is None or self._get_next_token().type != TokenType.LPAREN:
                raise SyntaxError("Expected '(' after 'not' in BExpression")
            factor_node = self.parse_BExpression()
            if self._get_next_token() is None or self._get_next_token().type != TokenType.RPAREN:
                raise SyntaxError("Expected ')' after BExpression in 'not' operation")
            self._advance() # consume ')'
            return NodeNot(factor_node)
        

        if token.type == TokenType.LPAREN:
            # hit '(' it could be '(' AExpression '<=/=' AExpression ')' or '(' BExpression 'and/or' BExpression ')'
            # try one of them, if one fails, need to rollback and try other options
            
            current_pos = self.pos # save current position for rollback

             # try '(' AExpression '<=/=' AExpression ')'
            self._advance() # consume '('
            left_aexpr = self.parse_AExpression()
            if left_aexpr is None:
                # rollback, try '(' BExpression 'and/or' BExpression ')'
                self.pos = current_pos
                self._advance() # consume '('
                left_bexpr = self.parse_BExpression()
                if left_bexpr is None:
                    raise SyntaxError("Invalid BExpression after '('")
                op_token = self._get_next_token()
                if op_token is None or op_token.type not in {TokenType.AND, TokenType.OR}:
                    raise SyntaxError(f"Invalid operator {op_token} in BExpression")
                self._advance() # consume operator
                right_bexpr = self.parse_BExpression()
                closing_token = self._get_next_token()
                if closing_token is None or closing_token.type != TokenType.RPAREN:
                    raise SyntaxError("Expected ')' at the end of BExpression")
                self._advance() # consume ')'

                # valid expression, create corresponding node
                if op_token.type == TokenType.AND:
                    return NodeAnd(left_bexpr, right_bexpr)
                elif op_token.type == TokenType.OR:
                    return NodeOr(left_bexpr, right_bexpr)
            else:
                # success parsing left AExpression
                op_token = self._get_next_token()
                if op_token is None or op_token.type not in {TokenType.LE, TokenType.EQ}:
                    raise SyntaxError(f"Invalid operator {op_token} in BExpression")
                self._advance() # consume operator
                right_aexpr = self.parse_AExpression()
                closing_token = self._get_next_token()
                if closing_token is None or closing_token.type != TokenType.RPAREN:
                    raise SyntaxError("Expected ')' at the end of BExpression")
                self._advance() # consume ')'

                # valid expression, create corresponding node
                if op_token.type == TokenType.LE:
                    return NodeLessEqual(left_aexpr, right_aexpr)
                elif op_token.type == TokenType.EQ:
                    return NodeEqual(left_aexpr, right_aexpr)
        
        return None
    

    def parse_Command(self):
        '''
        Command ::=  Command ';' Command
        '''
        left_node = self.parse_Atomic_Command()
        token = self._get_next_token()
        while token is not None and token.type == TokenType.SEQ:
            self._advance() # consume ';'
            right_node = self.parse_Atomic_Command()
            if right_node is None:
                raise SyntaxError(f"Invalid Command after ';' in sequence at position {self.pos}")
            left_node = NodeSequence(left_node, right_node)
            token = self._get_next_token()

        return left_node

    def parse_Atomic_Command(self):
        '''
        'skip' | VAR ':=' AExpression | 'if' BExpression 'then' Command 'else' Command 'end' | 'while' BExpression 'do' Command 'end' 
        '''
        token = self._get_next_token()
        print(token)

        if token is None:
            raise SyntaxError("Unexpected end of input while parsing Command")
        
        if token.type == TokenType.SKIP:
            self._advance() # consume 'skip'
            return NodeSkip()
        
        if token.type == TokenType.VAR:
            var_name = token.value
            self._advance() # consume VAR
            assign_token = self._get_next_token()
            if assign_token is None or assign_token.type != TokenType.ASSIGN:
                raise SyntaxError("Expected ':=' after variable in assignment")
            self._advance() # consume ':='
            aexpr_node = self.parse_AExpression()
            if aexpr_node is None:
                raise SyntaxError("Invalid AExpression in assignment")
            return NodeAssign(var_name, aexpr_node)
        
        if token.type == TokenType.IF:
            self._advance() # consume 'if'
            bexpr_node = self.parse_BExpression()
            if bexpr_node is None:
                raise SyntaxError("Invalid BExpression in if statement")
            then_token = self._get_next_token()
            if then_token is None or then_token.type != TokenType.THEN:
                raise SyntaxError("Expected 'then' after BExpression in if statement")
            self._advance() # consume 'then'
            then_command = self.parse_Command()
            else_token = self._get_next_token()
            if else_token is None or else_token.type != TokenType.ELSE:
                raise SyntaxError("Expected 'else' after then Command in if statement")
            self._advance() # consume 'else'
            else_command = self.parse_Command() # use parse_Command since it can be a sequence of commands
            end_token = self._get_next_token()
            if end_token is None or end_token.type != TokenType.END:
                raise SyntaxError("Expected 'end' at the end of if statement")
            self._advance() # consume 'end'
            return NodeIf(bexpr_node, then_command, else_command)
        
        if token.type == TokenType.WHILE:
            self._advance() # consume 'while'
            bexpr_node = self.parse_BExpression()
            if bexpr_node is None:
                raise SyntaxError("Invalid BExpression in while statement")
            do_token = self._get_next_token()
            if do_token is None or do_token.type != TokenType.DO:
                raise SyntaxError("Expected 'do' after BExpression in while statement")
            self._advance() # consume 'do'
            do_command = self.parse_Command() # use parse_Command since it can be a sequence of commands
            end_token = self._get_next_token()
            if end_token is None or end_token.type != TokenType.END:
                raise SyntaxError("Expected 'end' at the end of while statement")
            self._advance() # consume 'end'
            return NodeWhile(bexpr_node, do_command)
            
        return None
    

if __name__ == "__main__":
    # simple test
    input_text = "x := 10; if (x <= 20) then skip else x := (x + 1) end; while (x <= 20) do x := (x+1) end" # result should be x = 21
    import lexer
    lexer = Lexer(input_text)
    tokens = lexer.lex()
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    ast.print()
    memory = {}
    ast.eval(memory)
    print(memory) 