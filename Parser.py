from Interpreter import *
from lexer import *
from BST import *

class pRes:
    def __init__(self):
        self.error = None
        self.node = None

    def store(self, res):
        if isinstance(res, pRes):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

class parse:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.adv()

    def adv(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != end:
            return res.failure(synErr(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res


    def atom(self):
        res = pRes()
        tok = self.current_tok

        if tok.type in (Integer, decimal):
            res.store(self.adv())
            return res.success(NumberNode(tok))

        elif tok.type == leftClose:
            res.store(self.adv())
            expr = res.store(self.expr())
            if res.error: return res
            if self.current_tok.type == rightClose:
                res.store(self.adv())
                return res.success(expr)
            else:
                return res.failure(synErr(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(synErr(
            tok.pos_start, tok.pos_end,
            "Expected int, decimal, '+', '-' or '('"
        ))

    def power(self):
        return self.bOp(self.atom, (power,), self.factor)

    def factor(self):
        res = pRes()
        tok = self.current_tok

        if tok.type in (add, subtract):
            res.store(self.adv())
            factor = res.store(self.factor())
            if res.error: return res
            return res.success(uOps(tok, factor))

        return self.power()

    def term(self):
        return self.bOp(self.factor, (multiply, division))

    def expr(self):
        return self.bOp(self.term, (add, subtract))

    def bOp(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = pRes()
        left = res.store(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            tokenOp = self.current_tok
            res.store(self.adv())
            right = res.store(func_b())
            if res.error: return res
            left = bOps(left, tokenOp, right)

        return res.success(left)
