class TokenType:
    # Literals
    INT     = 'int'      # integer 
    VAR     = 'var'      # variable name

    # Operators
    PLUS    = '+'
    MINUS   = '-'
    MUL     = '*'
    ASSIGN  = ':='
    LE      = '<='       
    EQ      = '='        # Using = for equality (IMP)
    
    # Keywords
    TRUE    = 'true'
    FALSE   = 'false'
    NOT     = 'not'
    AND     = 'and'
    OR      = 'or'
    SKIP    = 'skip'
    IF      = 'if'
    THEN    = 'then'
    ELSE    = 'else'
    END     = 'end'
    WHILE   = 'while'
    DO      = 'do'

    # Punctuation
    LPAREN  = '('
    RPAREN  = ')'
    SEQ     = ';'

class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        if self.value: return f"Token({self.type}, {repr(self.value)})"
        return f"Token({self.type})"