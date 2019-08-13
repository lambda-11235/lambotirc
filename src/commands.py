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

import uuid
import random
import time

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

    res = 0
    for _ in range(n):
        res += random.randint(1, sides)

    bot.say(f"{msg.sender.nick} rolled {res}/{spec}")

def surprise(msg, arg, bot):
    args = arg.split()

    if len(args) > 0:
        bot.say("you get a car, you get a car, you get a car, ...")
        time.sleep(2)
        bot.say(f"{args[0]} gets a goat")

def uuidC(msg, arg, bot):
    bot.say(f"{msg.sender.nick}: {uuid.uuid1()}")
