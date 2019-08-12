
import re
import socket


class Bot:
    def __init__(self, name, server, port, channel, comandSymbol='~'):
        self.name = name
        self.server = server
        self.port = port
        self.channel = channel
        self.comandSymbol = comandSymbol

        self.commands = {}
        self.reactions = []


    def mainLoop(self):
        self.socket = socket.socket()
        self.socket.connect((self.server, self.port))

        self.sendMsg('PASS', ['password'])
        self.sendMsg('NICK', [self.name])
        self.sendMsg('USER', [self.name, '8', '*'], trailing='IRC test bot')

        self.sendMsg('JOIN', [self.channel])

        # Wait to be joined
        joined = False
        while not joined:
            msg = self.socket.recv(256).decode('utf-8')[:-2]
            print("RCV  " + msg)

            if msg.find("JOIN " + self.channel) >= 0:
                joined = True
                print("### JOINED")

        while True:
            msg = self.socket.recv(256).decode('utf-8')[:-2]
            print("RCV  " + msg)
            (sender, command, params, trailing) = self.decodeMsg(msg)

            if command == 'PRIVMSG':
                if params == [self.channel]:
                    try:
                        if len(trailing) > 0 and trailing[0] == self.comandSymbol:
                            self.handleCommand(sender, trailing)
                        else:
                            self.handleReaction(sender, trailing)
                    except Exception as err:
                        self.say(f"Error: {err}")
            elif command == 'PING':
                arg = []

                if len(params) > 0:
                    arg = params[0]
                elif trailing is not None:
                    arg = trailing
                elif sender['nick'] is not None:
                    arg = sender['nick']

                self.sendMsg('PONG', [arg])


    def sendMsg(self, command, params, prefix = None, trailing = None):
        msg = ""

        if prefix is not None:
            msg += ':' + prefix + ' '

        msg += command

        for p in params:
            msg += ' ' + p

        if trailing is not None:
            msg += ' :' + trailing

        msg += '\r\n'

        print("SEND " + msg, end='')
        self.socket.send(bytearray(msg, 'utf-8'))


    def say(self, msg):
            self.sendMsg('PRIVMSG', [self.channel], trailing = msg)
    def action(self, msg):
            self.sendMsg('PRIVMSG', [self.channel], trailing = '\x01ACTION ' + msg + '\x01')


    def decodeMsg(self, msg):
        sender = {'nick': None, 'user': None, 'host': None}
        command = None
        params = []
        trailing = None

        pos = msg.find(':', 1)
        if pos > 0:
            trailing = msg[(pos+1):]
            msg = msg[:pos]

        msg = msg.split()

        if msg[0][0] == ':':
            senderStr = msg[0][1:]
            msg = msg[1:]

            pos = senderStr.find('@')
            if pos > 0:
                sender['host'] = senderStr[(pos+1):]
                senderStr = senderStr[:pos]

            pos = senderStr.find('!')
            if pos > 0:
                sender['user'] = senderStr[(pos+1):]
                senderStr = senderStr[:pos]

            sender['nick'] = senderStr

        command = msg[0]
        params = msg[1:]

        return (sender, command, params, trailing)

    def handleCommand(self, sender, trailing):
        pos = trailing.find(' ')

        if pos > 0:
            command = trailing[1:pos]
            arg = trailing[(pos+1):]
        else:
            command = trailing[1:]
            arg = ''

        print(f"### COMMAND ({sender}, {command}, {arg})")

        action = self.commands.get(command)

        if action is not None:
            action(sender, arg, self)

    def handleReaction(self, sender, trailing):
        for (regex, action) in self.reactions:
            if regex.match(trailing):
                action(sender, trailing, self)

    def registerCommand(self, name, action):
        self.commands[name] = action

    def registerReaction(self, regex, action, ignoreCase=False):
        flags = 0

        if ignoreCase:
            flags = flags | re.IGNORECASE

        self.reactions.append((re.compile(regex, flags), action))
