from Interpreter import *
from Parser import *
from lexer import *


def run(fn, text):
    lexer = lex(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    p = parse(tokens)
    ast = p.parse()
    if ast.error: return None, ast.error
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
