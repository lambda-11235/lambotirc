
class Reaction:
    """
    Base class that allows the bot to react to arbitrary IRC messages.
    """
    def getDocumentation(self):
        """
        A one line documentation string.
        """
        return "Undocumented"

    def shouldRun(self, msg, bot):
        """
        Determines if the bot should react to a message.

        msg: The Message object under scrutiny.
        bot: A reference to the current Bot instance.
        """
        return False

    def run(self, msg, bot):
        """
        The action to take when the bot reacts.

        msg: The Message object associated with the reaction.
        bot: A reference to the current Bot instance.
        """
        pass


class Respond(Reaction):
    def getDocumentation(self):
        return "responds to mentions of the bot"

    def shouldRun(self, msg, bot):
        return msg.command == 'PRIVMSG' and msg.trailing.find(bot.name + ':') == 0

    def run(self, msg, bot):
        bot.say(f"{msg.sender.nick}: Me no speak human language")


class Kick(Reaction):
    def getDocumentation(self):
        return "reacts to someone getting kicked"

    def shouldRun(self, msg, bot):
        return msg.command == 'KICK' and msg.params[0] == bot.channel

    def run(self, msg, bot):
        bot.say(f"{msg.params[1]} is outta here")
