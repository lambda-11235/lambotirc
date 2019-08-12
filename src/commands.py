
import uuid
import random
import time

def uuidC(sender, arg, bot):
    bot.say(f"{sender['nick']}: {uuid.uuid1()}")

def dice(sender, arg, bot):
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

    bot.say(f"{sender['nick']} rolled {res}/{spec}")

def surprise(sender, arg, bot):
    args = arg.split()

    if len(args) > 0:
        bot.say("you get a car, you get a car, you get a car, ...")
        time.sleep(2)
        bot.say(f"{args[0]} gets a goat")
