
class Filter:
    """
    Changes messages in some arbitrary way.
    """
    def getDocumentation(self):
        """
        A one line documentation string.
        """
        return "Undocumented"

    def shouldRun(self, msg, bot):
        """
        Determines if this filter should be applied to a message.

        msg: The Message object under scrutiny.
        """
        return False

    def run(self, msg):
        """
        Modifies a message in some way.

        msg: The Message object associated with the reaction.
        """
        pass


class REDiscord(Filter):
    # Example message from rediscord
    # :rediscord!~rediscord@icculus.org PRIVMSG #redeclipse :<user> msg

    def getDocumentation(self):
        return "Changes messages from Discord(tm) to IRC messages for #redeclipse"

    def shouldRun(self, msg):
        return (msg.sender is not None
                and msg.sender.nick == "rediscord"
                and msg.sender.user == '~rediscord'
                and msg.trailing[0] == '<'
                and msg.trailing.find('> ') >= 0)

    def run(self, msg):
        pos = msg.trailing.find('> ')
        msg.sender.nick = '@' + msg.trailing[1:pos]
        msg.trailing = msg.trailing[(pos+2):]
