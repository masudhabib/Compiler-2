from ErrorClass import *
from Token import *
from position import *

numbers = '0123456789'
Integer = 'integer'
decimal = 'decimal'
add = 'addition'
subtract = 'subtraction'
multiply = 'Multiply'
division = 'division'
power = 'power'
leftClose = 'leftParenthesis'
rightClose = 'RightParenthesis'
end = 'End'


class lex:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = pos(-1, 0, -1, fn, text)
        self.curChar = None
        self.adv()

    def adv(self):
        self.pos.adv(self.curChar)
        self.curChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.curChar != None:
            if self.curChar in ' \t':
                self.adv()
            elif self.curChar in numbers:
                tokens.append(self.make_number())
            elif self.curChar == '+':
                tokens.append(tkn(add, pos_start=self.pos))
                self.adv()
            elif self.curChar == '-':
                tokens.append(tkn(subtract, pos_start=self.pos))
                self.adv()
            elif self.curChar == '*':
                tokens.append(tkn(multiply, pos_start=self.pos))
                self.adv()
            elif self.curChar == '/':
                tokens.append(tkn(division, pos_start=self.pos))
                self.adv()
            elif self.curChar == '^':
                tokens.append(tkn(power, pos_start=self.pos))
                self.adv()
            elif self.curChar == '(':
                tokens.append(tkn(leftClose, pos_start=self.pos))
                self.adv()
            elif self.curChar == ')':
                tokens.append(tkn(rightClose, pos_start=self.pos))
                self.adv()
            else:
                pos_start = self.pos.copy()
                char = self.curChar
                self.adv()
                return [], err_illegal(pos_start, self.pos, "'" + char + "'")

        tokens.append(tkn(end, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.curChar != None and self.curChar in numbers + '.':
            if self.curChar == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.curChar
            self.adv()

        if dot_count == 0:
            return tkn(Integer, int(num_str), pos_start, self.pos)
        else:
            return tkn(decimal, float(num_str), pos_start, self.pos)
