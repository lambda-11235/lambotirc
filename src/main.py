
from bot import Bot
import commands

bot = Bot("lambotirc", "card.freenode.net", 6666, "#redeclipse", comandSymbol = '^')

bot.registerCommand('dice', commands.dice)
bot.registerCommand('icecream', commands.icecream)
bot.registerCommand('surprise', commands.surprise)
bot.registerCommand('uuid', commands.uuidC)
bot.registerCommand('shrug', lambda msg, arg, bot: bot.say("¯\_(ツ)_/¯"))
bot.registerCommand('music', lambda msg, arg, bot: bot.say("do re mi fa sol la ti do"))
bot.registerCommand('divby0', lambda msg, arg, bot: 1/0)

bot.registerReaction(bot.name + ':.*', lambda msg, bot:
        bot.say(f"{msg.sender.nick}: Me no speak human language"))

bot.registerReaction(' *where *am *i\\?? *', lambda msg, bot:
        bot.say(f"{msg.sender.nick}: You're on {bot.channel}"),
        True)

bot.mainLoop()
