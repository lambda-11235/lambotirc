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
import reactions
from mathCommand import Math

bot = Bot("lambotirc", "card.freenode.net", 6666, "#redeclipse", commandSymbol = '!')

bot.registerCommand(commands.Action())
bot.registerCommand(commands.Dice())
bot.registerCommand(commands.Help())
bot.registerCommand(commands.Hug())
bot.registerCommand(commands.Icecream())
bot.registerCommand(commands.Kick())
bot.registerCommand(commands.Pray())
bot.registerCommand(commands.Postfix())
bot.registerCommand(commands.Say())
bot.registerCommand(commands.Shrug())
bot.registerCommand(commands.Surprise())
bot.registerCommand(commands.UUID())

bot.registerCommand(Math())

bot.registerReaction(reactions.Respond())
bot.registerReaction(reactions.Kick())
bot.registerReaction(reactions.BotKick())

bot.mainLoop()
