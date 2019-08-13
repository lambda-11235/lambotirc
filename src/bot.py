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

import re
import socket

from message import *


class Bot:
    def __init__(self, name, server, port, channel, commandSymbol='~'):
        """
        Create a new bot instance.

        name: The bot's nick.
        server: The IRC server's address.
        port: The port to connect to. Must be an int.
        channel: The channel to listen on.
        commandSymbol: The symbol that triggers the start of a command.
        """
        self.name = name
        self.server = server
        self.port = port
        self.channel = channel
        self.commandSymbol = commandSymbol

        self.commands = {}
        self.reactions = []

        self.msgQueue = []
        self.unparsed = bytearray()


    def mainLoop(self):
        """
        Opens a socket, registers the nick, connects to the channel, and starts
        fielding commands.
        """
        self.socket = socket.socket()
        self.socket.connect((self.server, self.port))

        self.sendMsg(Message('PASS', ['password']))
        self.sendMsg(Message('NICK', [self.name]))
        self.sendMsg(Message('USER', [self.name, '*', '*'], trailing='IRC test bot'))

        self.sendMsg(Message('JOIN', [self.channel]))

        # Wait to be joined
        joined = False
        while not joined:
            msg = self.getMsg()

            if msg.command == 'JOIN' and msg.params == [self.channel]:
                joined = True
                print("### JOINED")

        while True:
            msg = self.getMsg()

            if msg.command == 'PRIVMSG':
                if msg.params == [self.channel]:
                    try:
                        if len(msg.trailing) > 0 and msg.trailing[0] == self.commandSymbol:
                            self.handleCommand(msg)
                        else:
                            self.handleReaction(msg)
                    except Exception as err:
                        self.say(f"Error: {err}")
            elif msg.command == 'PING':
                arg = []

                if len(msg.params) > 0:
                    arg = msg.params[0]
                elif msg.trailing is not None:
                    arg = msg.trailing
                elif msg.sender.nick is not None:
                    arg = msg.sender.nick

                self.sendMsg(Message('PONG', [arg]))


    def getMsg(self):
        """
        Get the next available message.
        """
        while len(self.msgQueue) == 0:
            self.unparsed += self.socket.recv(256)

            pos = self.unparsed.find(bytearray('\r\n', 'utf-8'))
            while pos > 0:
                self.msgQueue.append(Message.fromString(self.unparsed[:pos].decode('utf-8', 'replace')))
                self.unparsed = self.unparsed[(pos+2):]
                print("RCV  " + str(self.msgQueue[-1]))
                pos = self.unparsed.find(bytearray('\r\n', 'utf-8'))

        msg = self.msgQueue[0]
        self.msgQueue = self.msgQueue[1:]
        return msg

    def sendMsg(self, msg):
        """
        Send a message to the server.
        """
        print("SEND " + str(msg))
        self.socket.send(bytearray(str(msg) + '\r\n', 'utf-8'))


    def say(self, msg):
        """
        Makes the bot say something in the channel.
        """
        self.sendMsg(Message('PRIVMSG', [self.channel], trailing = msg))

    def action(self, msg):
        """
        Makes the bot say something in the third person.

        Example:
        python > bot.say(" lands on face")
        channel> * bot lands on face
        """
        self.sendMsg(Message('PRIVMSG', [self.channel], trailing = '\x01ACTION ' + msg + '\x01'))


    def handleCommand(self, msg):
        """
        Passes off a command to one of the registered actions.
        """
        pos = msg.trailing.find(' ')

        if pos > 0:
            command = msg.trailing[1:pos]
            arg = msg.trailing[(pos+1):]
        else:
            command = msg.trailing[1:]
            arg = ''

        print(f"### COMMAND ({msg.sender}, {command}, {arg})")

        action = self.commands.get(command)

        if action is not None:
            action(msg, arg, self)
        else:
            self.say(f"{command} is not a recognized command")


    def handleReaction(self, msg):
        """
        Checks for reactions to a post.
        """
        for (regex, action) in self.reactions:
            if regex.match(msg.trailing):
                action(msg, self)


    def registerCommand(self, name, action):
        """
        Registers a command.

        name: The text the user enter for the command.
        action: A function of the form `foo(msg, arg, bot)`.
            The parameters meanings are a follows.
            msg: The Message object associated with the command.
            arg: The part of the message that comes after the command.
            bot: A reference to the current Bot instance.
        """
        self.commands[name] = action


    def registerReaction(self, regex, action, ignoreCase=False):
        """
        Registers a reaction to certain posts.

        regex: A regular expression that triggers the reaction if it matches a
            post.
        action: A function of the form `foo(msg, bot)`.
            The parameters meanings are a follows.
            msg: The Message object that triggered the reaction.
            bot: A reference to the current Bot instance.
        ignoreCase: Whether the regex should ignore letter case in the message.
        """
        flags = 0

        if ignoreCase:
            flags = flags | re.IGNORECASE

        self.reactions.append((re.compile(regex, flags), action))
