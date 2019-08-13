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

import util


class Command:
    """
    Base class for bot commands.
    """
    def getName(self):
        """
        The name that causes the command to be ran.
        """
        return None

    def getUsage(self):
        """
        A usage string. In the help it will print as `!name usage` where `usage`
        is returned by this function.
        """
        return "args..."

    def getDocumentation(self):
        """
        A one line documentation string.
        """
        return "Undocumented"

    def run(self, msg, arg, bot):
        """
        The action to take when the command is invoked.

        msg: The Message object associated with the command.
        arg: The part of the message that comes after the command.
        bot: A reference to the current Bot instance.
        """
        pass


class Action(Command):
    def getName(self):
        return "action"

    def getUsage(self):
        return "text..."

    def getDocumentation(self):
        return "causes the bot to take action"

    def run(self, msg, arg, bot):
        bot.action(util.sanitise(arg))


class Dice(Command):
    def getName(self):
        return "dice"

    def getUsage(self):
        return "(sides | n'd'sides)"

    def getDocumentation(self):
        return "rolls die"

    def run(self, msg, arg, bot):
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


class Help(Command):
    def getName(self):
        return "help"

    def getUsage(self):
        return "[command]"

    def getDocumentation(self):
        return "lists commands or prints help for a specific one"

    def run(self, msg, arg, bot):
        args = arg.split()
        commands = bot.commands.keys()

        if len(args) > 0:
            if args[0] in commands:
                command = bot.commands[args[0]]
                bot.say(bot.commandSymbol + command.getName() + " " + command.getUsage())
                bot.say(command.getDocumentation())
            else:
                bot.say(args[0] + " is not a recognized command")
        else:
            msg = "Commands:"

            for com in commands:
                msg += " " + com

            bot.say(msg)


class Hug(Command):
    def getName(self):
        return "hug"

    def getUsage(self):
        return "[nick]"

    def getDocumentation(self):
        return "gives someone a hug"

    def run(self, msg, arg, bot):
        args = arg.split()

        if len(args) > 0:
            target = args[0]
        else:
            target = msg.sender.nick

        bot.action(f" gives {target} a hug")


class Icecream(Command):
    def getName(self):
        return "icecream"

    def getUsage(self):
        return "[nick]"

    def getDocumentation(self):
        return "gives someone an icecream"

    def run(self, msg, arg, bot):
        args = arg.split()

        if len(args) > 0:
            target = args[0]
        else:
            target = msg.sender.nick

        bot.action(f" gives {target} an icecream")


class Kick(Command):
    def getName(self):
        return "kick"

    def getUsage(self):
        return "[nick]"

    def getDocumentation(self):
        return "kicks someone"

    def run(self, msg, arg, bot):
        args = arg.split()

        if len(args) > 0:
            target = args[0]
        else:
            target = msg.sender.nick

        bot.action(f" kicks {target} in the jugular")


class Shrug(Command):
    def getName(self):
        return "shrug"

    def getUsage(self):
        return ""

    def getDocumentation(self):
        return "¯\_(ツ)_/¯"

    def run(self, msg, arg, bot):
        bot.say("¯\_(ツ)_/¯")


class Say(Command):
    def getName(self):
        return "say"

    def getUsage(self):
        return "text..."

    def getDocumentation(self):
        return "causes the bot to say something"

    def run(self, msg, arg, bot):
        bot.say(util.sanitise(arg))


class Surprise(Command):
    def getName(self):
        return "surprise"

    def getUsage(self):
        return "[nick]"

    def getDocumentation(self):
        return "it wouldn't be a surprise if I told you what happens"

    def run(self, msg, arg, bot):
        args = arg.split()

        if len(args) > 0:
            bot.say("you get a car, you get a car, you get a car, ...")
            time.sleep(2)
            bot.say(f"{args[0]} gets a goat")


class UUID(Command):
    def getName(self):
        return "uuid"

    def getUsage(self):
        return ""

    def getDocumentation(self):
        return "generates a UUID"

    def run(self, msg, arg, bot):
        bot.say(f"{msg.sender.nick}: {uuid.uuid1()}")


class Postfix(Command):
    def getName(self):
        return "postfix"

    def getUsage(self):
        return "(postfix math expression...)"

    def getDocumentation(self):
        return "evaluates a postfix arithmetic expression"

    def run(self, msg, arg, bot):
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
