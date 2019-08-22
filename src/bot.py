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
import traceback

from message import *
import util


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
        self.filters = []
        self.reactions = []

        self.msgQueue = []
        self.unparsed = bytearray()

        self.running = False


    def mainLoop(self):
        """
        Opens a socket, registers the nick, connects to the channel, and starts
        fielding commands.
        """
        self.running = True

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

        while self.running:
            msg = self.getMsg()

            self.handleFilters(msg)

            try:
                if msg.command == 'PRIVMSG':
                    if msg.params == [self.channel] and len(msg.trailing) > 0 and msg.trailing[0] == self.commandSymbol:
                        self.handleCommand(msg)
                elif msg.command == 'PING':
                    arg = []

                    if len(msg.params) > 0:
                        arg = msg.params[0]
                    elif msg.trailing is not None:
                        arg = msg.trailing
                    elif msg.sender.nick is not None:
                        arg = msg.sender.nick

                    self.sendMsg(Message('PONG', [arg]))

                self.handleReaction(msg)
            except Exception as err:
                self.say(f"Error: {err}")
                print(traceback.format_exc())

        self.sendMsg(Message('QUIT', []))
        self.socket.close()


    def halt(self):
        """
        Halt the main loop.
        """
        self.running = False


    def getMsg(self):
        """
        Get the next available message.
        """
        while len(self.msgQueue) == 0:
            self.unparsed += self.socket.recv(256)

            try:
                pos = self.unparsed.find(bytearray('\r\n', 'utf-8'))
                while pos > 0:
                    self.msgQueue.append(Message.fromString(self.unparsed[:pos].decode('utf-8', 'replace')))
                    self.unparsed = self.unparsed[(pos+2):]
                    print("RCV  " + str(self.msgQueue[-1]))
                    pos = self.unparsed.find(bytearray('\r\n', 'utf-8'))
            except:
                self.unparsed = bytearray()

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

        arg = util.sanitise(arg)

        print(f"### COMMAND ({msg.sender}, {command}, {arg})")

        com = self.commands.get(command)

        if com is not None:
            com.run(msg, arg, self)
        else:
            self.say(f"{command} is not a recognized command")


    def handleFilters(self, msg):
        """
        Applies all relevant filters to a message and returns it.
        """
        hasFiltered = False

        for filt in self.filters:
            if filt.shouldRun(msg):
                filt.run(msg)
                hasFiltered = True

        if hasFiltered:
            print(f"FLT  {msg}")


    def handleReaction(self, msg):
        """
        Checks for reactions to a post.
        """
        for react in self.reactions:
            if react.shouldRun(msg, self):
                react.run(msg, self)


    def registerCommand(self, command):
        """
        Registers a command.

        command: An object of type Command.
        """
        self.commands[command.getName()] = command


    def registerFilter(self, filt):
        """
        Registers a filter. Please note, the order of filters matters! Filters
        are applied in the order they are registered.

        command: An object of type Filter.
        """
        self.filters.append(filt)


    def registerReaction(self, reaction):
        """
        Registers a reaction to certain posts.

        reaction: An object of type reaction.
        """
        self.reactions.append(reaction)
