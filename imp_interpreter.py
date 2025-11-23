import lexer
import parser

class IMPInterpreter:
    def __init__(self, input_text: str):
        try:
            self.lexer = lexer.Lexer(input_text)
            self.tokens = self.lexer.lex()
            self.parser = parser.Parser(self.tokens)
            self.ast = self.parser.parse()
        except Exception as e:
            raise Exception(f"IMPInterpreter parsing error: {str(e)}")

    def run(self, memory: dict):
        '''
        Run the IMP program represented by the AST on the given memory.
        '''
        self.ast.eval(memory)
        return memory