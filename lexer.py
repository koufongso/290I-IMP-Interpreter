from token import Token, TokenType

# we implmenet the lexer as a state machine
# a more advanced implementation could use regexes or similar techniques
class Lexer:
    def __init__(self, input_text):
        self.text = input_text
        self.length = len(input_text)
        self.pos = -1 # "reading head" position in input text
        self.state = 'NEXT'
        self.buffer = ''
        self.lexeme = []

    def get_lexeme(self):
        return self.lexeme

    def lex(self):
        while True:
            self._step()
            if self.state == 'EOF':
                break   
        return self.lexeme
    
    def _step(self):
        if self.state == 'NEXT':           # starting state
            self._handle_next_state()
        elif self.state == 'READING_INT':   # integer literal
            self._handle_int_state()
        elif self.state == 'READING_LETTER': # variable/identifier or keyword
            self._handle_letter_state()
        elif self.state == 'READING_OPERATOR': # operator
            self._handle_operator_state()
        elif self.state == 'EOF':           # end of file/input
            return
        
    def _handle_next_state(self):
        # check if next char is punctuation: ";()"
        c = self._get_next_char()

        if c is None:
            # end of input
            self._set_state('EOF')
        elif c.isspace():
            # white space, skip it
            self.pos += 1
        elif self._is_punctuation(c):
            # punctuation, create token
            self._create_punctuation_token(c)
            self.pos += 1
        elif c.isdigit():
            # start reading integer literal
            self._set_state('READING_INT')
            self.buffer = c # add first char to buffer
            self.pos += 1 # move head
        elif c.isalpha():
            # start reading variable/identifier or keyword (must start with letter)
            self._set_state('READING_LETTER')
            self.buffer = c # add first char to buffer
            self.pos += 1   # move head
        elif self._is_operator_char(c):
            # start reading operator (since there could be multi-char operators)
            self._set_state('READING_OPERATOR')
            self.buffer = c # add first char to buffer
            self.pos += 1   # move head
        else:
            raise Exception(f"Lexer error: unexpected character '{c}' at position {self.pos+1}")



    def _handle_int_state(self):
        c = self._get_next_char()

        if c is not None:
            # has next
            if c.isdigit():
                # next is still digit, keep reading
                self.buffer += c
                self.pos += 1
            else:
                # end of integer literal, create token
                self._create_int_token(self.buffer)
                self.buffer = ''
                self._set_state('NEXT')
        else:
            # end of input, create token
            self._create_int_token(self.buffer)
            self.buffer = ''
            self._set_state('EOF')


    def _handle_letter_state(self):
        c = self._get_next_char()

        if c is not None:
            # has next
            if c.isalnum() or c == '_':
                # next is still letter or digit or underscore, keep reading
                self.buffer += c
                self.pos += 1
            else:
                # end of variable/identifier or keyword, create token
                if self._is_keyword(self.buffer):
                    self._create_keyword_token(self.buffer)
                else:
                    self._create_var_token(self.buffer)
                self.buffer = ''
                self._set_state('NEXT')
        else:
            # end of input, create token
            if self._is_keyword(self.buffer):
                self._create_keyword_token(self.buffer)
            else:
                self._create_var_token(self.buffer)
            self.buffer = ''
            self._set_state('EOF')

    def _handle_operator_state(self):
        # we only have maximum 2-char operators, so we check next char to see if it forms a valid operator
        c = self._get_next_char()

        if c is not None:
            # has next
            potential_op = self.buffer + c
            if self._is_operator(potential_op):
                # next char forms a valid operator, consume it
                self._create_operator_token(potential_op)
                self.buffer = ''
                self.pos += 1
                self._set_state('NEXT')
            else:
                # does not form operator, only use the current buffer
                # optional: we can do the sanity check here if (self._is_operator(self.buffer)) before creating token
                self._create_operator_token(self.buffer)
                self.buffer = ''
                self._set_state('NEXT')
        else:
            # end of input, create token, 
            # optional: we can do the sanity check here if (self._is_operator(self.buffer)) before creating token
            self._create_operator_token(self.buffer)
            self.buffer = ''
            self._set_state('EOF')

    def _is_punctuation(self, c: str) -> bool:
        return c in ';()'

    def _create_punctuation_token(self, c: str):
        if c == ';':
            self.lexeme.append(Token(TokenType.SEQ, c))
        elif c == '(':
            self.lexeme.append(Token(TokenType.LPAREN, c))
        elif c == ')':
            self.lexeme.append(Token(TokenType.RPAREN, c))

    def _is_operator_char(self, op_char: str) -> bool:
        # check if char is one of the first char of an operator
        return op_char in '+-*:=<'
    
    def _is_operator(self, op_str: str) -> bool:
        # check if string is a valid operator
        return op_str in ['+', '-', '*', ':=', '<=', '=']
    
    def _create_operator_token(self, op_str: str):
        if op_str == '+':
            self.lexeme.append(Token(TokenType.PLUS, op_str))
        elif op_str == '-':
            self.lexeme.append(Token(TokenType.MINUS, op_str))
        elif op_str == '*':
            self.lexeme.append(Token(TokenType.MUL, op_str))
        elif op_str == ':=':
            self.lexeme.append(Token(TokenType.ASSIGN, op_str))
        elif op_str == '<=':
            self.lexeme.append(Token(TokenType.LE, op_str))
        elif op_str == '=':
            self.lexeme.append(Token(TokenType.EQ, op_str))

    def _create_int_token(self, int_str: str):
        self.lexeme.append(Token(TokenType.INT, int(int_str)))

    def _is_keyword(self, letter_str: str) -> bool:
        keywords = {
            'true', 'false', 'not', 'and', 'or',
            'skip', 'if', 'then', 'else', 'end',
            'while', 'do'
        }
        return letter_str in keywords

    def _create_keyword_token(self, letter_str: str):
        if letter_str == 'true':
            self.lexeme.append(Token(TokenType.TRUE, letter_str))
        elif letter_str == 'false':
            self.lexeme.append(Token(TokenType.FALSE, letter_str))
        elif letter_str == 'not':
            self.lexeme.append(Token(TokenType.NOT, letter_str))
        elif letter_str == 'and':
            self.lexeme.append(Token(TokenType.AND, letter_str))
        elif letter_str == 'or':
            self.lexeme.append(Token(TokenType.OR, letter_str))
        elif letter_str == 'skip':
            self.lexeme.append(Token(TokenType.SKIP, letter_str))
        elif letter_str == 'if':
            self.lexeme.append(Token(TokenType.IF, letter_str))
        elif letter_str == 'then':
            self.lexeme.append(Token(TokenType.THEN, letter_str))
        elif letter_str == 'else':
            self.lexeme.append(Token(TokenType.ELSE, letter_str))
        elif letter_str == 'end':
            self.lexeme.append(Token(TokenType.END, letter_str))
        elif letter_str == 'while':
            self.lexeme.append(Token(TokenType.WHILE, letter_str))
        elif letter_str == 'do':
            self.lexeme.append(Token(TokenType.DO, letter_str))
        else:
            raise Exception(f"Lexer error: unknown keyword '{letter_str}'")


    def _create_var_token(self, letter_str: str):
        self.lexeme.append(Token(TokenType.VAR, letter_str))

    def _set_state(self, new_state):
        self.state = new_state

    def _has_next_char(self):
        return self.pos + 1 < self.length
    
    def _get_next_char(self):
        # read next char without advancing position, return None if at EOF
        if self._has_next_char():
            return self.text[self.pos+1]
        return None


if __name__ == "__main__":
    # simple test
    input_text = "x := b1_0; if (x <= 20) then skip else x := (x + 1) end"
    lexer = Lexer(input_text)
    tokens = lexer.lex()
    print(tokens)

