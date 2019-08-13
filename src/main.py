#!/usr/bin/env python3

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

from bot import Bot
import commands

bot = Bot("lambotirc", "card.freenode.net", 6666, "#redeclipse", commandSymbol = '!')

bot.registerCommand('dice', commands.dice)
bot.registerCommand('icecream', commands.icecream)
bot.registerCommand('help', commands.help)
bot.registerCommand('hug', commands.hug)
bot.registerCommand('kick', commands.kick)
bot.registerCommand('say', commands.say)
bot.registerCommand('surprise', commands.surprise)
bot.registerCommand('uuid', commands.uuidC)
bot.registerCommand('divby0', lambda msg, arg, bot: 1/0)
bot.registerCommand('music', lambda msg, arg, bot: bot.say("do re mi fa sol la ti do"))
bot.registerCommand('shrug', lambda msg, arg, bot: bot.say("¯\_(ツ)_/¯"))

bot.registerReaction(bot.name + ':.*', lambda msg, bot:
        bot.say(f"{msg.sender.nick}: Me no speak human language"))

bot.registerReaction(' *where *am *i\\?? *', lambda msg, bot:
        bot.say(f"{msg.sender.nick}: You're on {bot.channel}"),
        True)

bot.mainLoop()
