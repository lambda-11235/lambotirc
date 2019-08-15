# Lambda's IRC bot
# Copyright (C) 2019  Taran Lynn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math

from commands import Command


class Math(Command):
    def getName(self):
        return "math"

    def getUsage(self):
        return "math expression..."

    def getDocumentation(self):
        return "evaluates a math expression"

    def run(self, msg, arg, bot):
        bot.say(str(Parser(arg).eval()))


mathConsts = {
    'e': math.e,
    'pi': math.pi,
    'phi': (1 + math.sqrt(5))/2,

    'nice': 69
}

mathFuncs = {
    'abs': abs,
    'exp': math.exp,
    'log': math.log,
    'sqrt': math.sqrt,

    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan
}


class Parser:
    """
    Parser for the following math grammar.

    <expr> := <mult> { ('+'|'-') <mult> } ;
    <mult> := <pow> { '*'|'/') <pow> } ;
    <pow>  := ['-'] <term> [ ^ <term> ] ;
    <term> := <num> | '(' <expr> ')' | <sym> [ '(' <expr> ')' ] ;
    """
    def __init__(self, string):
        self.toks = Lexer(string).lex()
        self.pos = 0

    def hasNext(self):
        return self.pos < len(self.toks)

    def next(self):
        if self.hasNext():
            return self.toks[self.pos]
        else:
            self.fail()

    def consume(self):
        self.pos += 1

    def match(self, ch):
        if self.next() == ch:
            self.consume()
        else:
            self.fail()

    def fail(self, msg=None):
        if msg is None:
            msg = "could not parse math expression"

        raise RuntimeError(msg)


    def eval(self):
        res = self.expr()

        if self.pos < len(self.toks):
            self.fail()

        return res

    def expr(self):
        res = self.mult()

        while self.hasNext() and self.next() in '+-':
            if self.next() == '+':
                self.consume()
                res += self.mult()
            elif self.next() == '-':
                self.consume()
                res -= self.mult()

        return res

    def mult(self):
        res = self.pow()

        while self.hasNext() and self.next() in '*/':
            if self.next() == '*':
                self.consume()
                res *= self.pow()
            elif self.next() == '/':
                self.consume()
                res /= self.pow()

        return res

    def pow(self):
        if self.next() == '-':
            self.consume()
            neg = True
        else:
            neg = False

        res = self.term()

        if self.hasNext() and self.next() in '^':
            self.consume()
            res **= self.term()

        if neg:
            res = -res

        return res

    def term(self):
        if isinstance(self.next(), float):
            res = self.next()
            self.consume()
        elif self.next() == '(':
            self.consume()
            res = self.expr()
            self.match(')')
        elif self.next()[0].isalpha():
            sym = self.next()
            self.consume()

            if self.hasNext() and self.next() == '(':
                self.consume()
                res = self.expr()
                self.match(')')

                func = mathFuncs.get(sym)

                if func is None:
                    self.fail(f"{sym} is not a valid math function")

                res = func(res)
            else:
                res = mathConsts.get(sym)

                if res is None:
                    self.fail(f"{sym} is not a valid math constant")

        return res


class Lexer:
    def __init__(self, string):
        self.string = string
        self.toks = []
        self.num = ""
        self.sym = ""
        self.sawPoint = False

    def lex(self):
        for c in self.string:
            if c in "+-*/^()":
                self.tokNum()
                self.tokSym()
                self.toks.append(c)
            elif c in "abcdefghijklmnopqrstuvwxyz":
                self.tokNum()
                self.sym += c
            elif c in "0123456789":
                self.tokSym()
                self.num += c
            elif c == '.':
                self.tokSym()

                if self.sawPoint:
                    raise RuntimeError(f"unexpected '.' when lexing {self.num}")
                else:
                    self.num += c
                    self.sawPoint = True
            elif c in " \t":
                pass
            else:
                raise RuntimeError(f"unexpected '{c}' when lexing")

        self.tokNum()
        self.tokSym()

        return self.toks

    def tokNum(self):
        if self.num != "":
            self.toks.append(float(self.num))
            self.num = ""
            self.sawPoint = False

    def tokSym(self):
        if self.sym != "":
            self.toks.append(self.sym)
            self.sym = ""
