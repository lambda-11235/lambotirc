
import re
import socket

from message import *


class Bot:
    def __init__(self, name, server, port, channel, comandSymbol='~'):
        self.name = name
        self.server = server
        self.port = port
        self.channel = channel
        self.comandSymbol = comandSymbol

        self.commands = {}
        self.reactions = []

        self.msgQueue = []
        self.unparsed = ""


    def mainLoop(self):
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
                        if len(msg.trailing) > 0 and msg.trailing[0] == self.comandSymbol:
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
        while len(self.msgQueue) == 0:
            self.unparsed += self.socket.recv(256).decode('utf-8')

            pos = self.unparsed.find('\r\n')
            while pos > 0:
                self.msgQueue.append(Message.fromString(self.unparsed[:pos]))
                self.unparsed = self.unparsed[(pos+2):]
                print("RCV  " + str(self.msgQueue[-1]))
                pos = self.unparsed.find('\r\n')

        msg = self.msgQueue[0]
        self.msgQueue = self.msgQueue[1:]
        return msg

    def sendMsg(self, msg):
        print("SEND " + str(msg))
        self.socket.send(bytearray(str(msg) + '\r\n', 'utf-8'))


    def say(self, msg):
            self.sendMsg(Message('PRIVMSG', [self.channel], trailing = msg))
    def action(self, msg):
            self.sendMsg(Message('PRIVMSG', [self.channel], trailing = '\x01ACTION ' + msg + '\x01'))

    def handleCommand(self, msg):
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
        for (regex, action) in self.reactions:
            if regex.match(msg.trailing):
                action(msg, self)

    def registerCommand(self, name, action):
        self.commands[name] = action

    def registerReaction(self, regex, action, ignoreCase=False):
        flags = 0

        if ignoreCase:
            flags = flags | re.IGNORECASE

        self.reactions.append((re.compile(regex, flags), action))
