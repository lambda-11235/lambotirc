
class Sender:
    def __init__(self, nick, user=None, host=None):
        self.nick = nick
        self.user = user
        self.host = host

    @classmethod
    def fromString(cls, string):
        user = None
        host = None

        pos = string.find('@')
        if pos > 0:
            host = string[(pos+1):]
            string = string[:pos]

        pos = string.find('!')
        if pos > 0:
            user = string[(pos+1):]
            string = string[:pos]

        nick = string

        return Sender (nick, user, host)

    def __repr__(self):
        s = self.nick

        if self.user is not None:
            s += '!' + self.user

        if self.host is not None:
            s += '@' + self.host

        return s


class Message:
    def __init__(self, command, params, trailing=None, sender=None):
        self.command = command
        self.params = params
        self.trailing = trailing
        self.sender = sender

    @classmethod
    def fromString(cls, msg):
        sender = None
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
            sender = Sender.fromString(senderStr)

        command = msg[0]
        params = msg[1:]

        return Message(command, params, trailing, sender)

    def __repr__(self):
        s = ""

        if self.sender is not None:
            s += ':' + str(self.sender) + ' '

        s += self.command

        for p in self.params:
            s += ' ' + str(p)

        if self.trailing is not None:
            s += ' :' + self.trailing

        return s
