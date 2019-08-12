
from bot import Bot
import commands

bot = Bot("lambotirc", "card.freenode.net", 6666, "#redeclipse", comandSymbol = '^')

bot.registerCommand('icecream', lambda sender, arg, bot: bot.action(f" gives {arg.split()[0] if len(arg.split()) > 0 else sender['nick']} an icecream"))
bot.registerCommand('shrug', lambda sender, arg, bot: bot.say("¯\_(ツ)_/¯"))
bot.registerCommand('music', lambda sender, arg, bot: bot.say("do re mi fa sol la ti do"))
bot.registerCommand('divby0', lambda sender, arg, bot: 1/0)
bot.registerCommand('dice', commands.dice)
bot.registerCommand('surprise', commands.surprise)
bot.registerCommand('uuid', commands.uuidC)

bot.registerReaction(bot.name + ':.*', lambda sender, arg, bot:
        bot.say(f"{sender['nick']}: Me no speak human language"))

bot.registerReaction(' *where *am *i\\?? *', lambda sender, arg, bot:
        bot.say(f"{sender['nick']}: You're on {bot.channel}"),
        True)

bot.mainLoop()
