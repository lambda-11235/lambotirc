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
import random
import time
import uuid

def icecream(msg, arg, bot):
    args = arg.split()

    if len(args) > 0:
        target = args[0]
    else:
        target = msg.sender.nick

    bot.action(f" gives {target} an icecream")

def dice(msg, arg, bot):
    args = arg.split()

    n = 1
    sides = 6

    if len(args) > 0:
        args = args[0].split('d')

        if len(args) > 1:
            n = int(args[0])
            sides = int(args[1])
        else:
            sides = int(args[0])

    if n == 1:
        spec = f"{sides}"
    else:
        spec = f"{n}d{sides}"

    if n > 100 or sides > 100:
        bot.say(f"{msg.sender.nick}: count or sides are too big")
        return

    res = 0
    for _ in range(n):
        res += random.randint(1, sides)

    bot.say(f"{msg.sender.nick} rolled {res}/{spec}")

def help(msg, arg, bot):
    commands = bot.commands.keys()

    msg = "Commands:"

    for com in commands:
        msg += " " + com

    bot.say(msg)

def hug(msg, arg, bot):
    args = arg.split()

    if len(args) > 0:
        target = args[0]
    else:
        target = msg.sender.nick

    bot.action(f" gives {target} a hug")

def kick(msg, arg, bot):
    args = arg.split()

    if len(args) > 0:
        target = args[0]
    else:
        target = msg.sender.nick

    bot.action(f" kicks {target} in the jugular")

def say(msg, arg, bot):
    bot.say(arg)

def surprise(msg, arg, bot):
    args = arg.split()

    if len(args) > 0:
        bot.say("you get a car, you get a car, you get a car, ...")
        time.sleep(2)
        bot.say(f"{args[0]} gets a goat")

def uuidC(msg, arg, bot):
    bot.say(f"{msg.sender.nick}: {uuid.uuid1()}")


def postfix(msg, arg, bot):
    """
    Executes simple postfix arithmetic. i.e. 1 2.3 + 4 - 2 3 * *
    """
    stack = []
    num = ""

    digits = "e.0123456789"

    for c in arg:
        if c in digits:
            num += c
        else:
            if len(num) > 0:
                stack.append(float(num))
                num = ""

        if c == '+':
            stack[-2] = stack[-2] + stack[-1]
            stack = stack[:-1]
        elif c == '-':
            stack[-2] = stack[-2] - stack[-1]
            stack = stack[:-1]
        elif c == '*':
            stack[-2] = stack[-2] * stack[-1]
            stack = stack[:-1]
        elif c == '/':
            stack[-2] = stack[-2] / stack[-1]
            stack = stack[:-1]
        elif c == '^':
            stack[-2] = stack[-2] ** stack[-1]
            stack = stack[:-1]
        elif c == 'x':
            stack[-1] = math.exp(stack[-1])
        elif c == 'l':
            stack[-1] = math.log(stack[-1])
        elif c == 's':
            stack[-1] = math.sin(stack[-1])
        elif c == 'c':
            stack[-1] = math.cos(stack[-1])
        elif c == 't':
            stack[-1] = math.tan(stack[-1])
        elif c == 'a':
            stack[-1] = math.atan(stack[-1])
        elif c not in " \t" + digits:
            raise RuntimeError(f"bad math symbol {c}")

    if len(num) > 0:
        stack.append(float(num))

    bot.say(f"{msg.sender.nick}: {stack[-1]}")
