

class ProposalProxy(object):
    ''' Proxy object that allows for proposals to have their speaker
    redacted. '''

    def __init__(self, proposal):
        self.__proposal__ = proposal

    def __getattr__(self, attr):
        ''' Overridden __getattr__ that hides the available speakers. '''

        if attr == "speaker":
            return Parrot("Primary Speaker")
        elif attr == "additional_speakers":
            return None
        elif attr == "speakers":
            return self._speakers
        else:
            return getattr(self.__proposal__, attr)

    def _speakers(self):
        for i, j in enumerate(self.__proposal__.speakers()):
            if i == 0:
                yield self.speaker
            else:
                yield Parrot("Additional speaker " + str(i))


class MessageProxy(object):
    ''' Proxy object that allows messages to redact the speaker name. '''

    def __init__(self, message):
        self.__message__ = message

    def __getattr__(self, attr):
        message = self.__message__

        if attr == "user":
            if message.user.speaker_profile in message.proposal.speakers():
                return Parrot("A Speaker")

        return getattr(message, attr)


class Parrot(object):
    ''' Placeholder object for speakers. For *any* __getattr__ call, it will
    repeat back the name it was given. '''

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __getattr__(self, attr):
        return self.name
