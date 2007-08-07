'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *


# TODO
# For future use?
class ISmsChunk(object):
    def __init__(self, Id, Message):
        self._Id = Id
        self._Message = Message

    Id = property(lambda self: self._Id)
    CharactersLeft = property()
    Text = property()
    Message = property(lambda self: self._Message)


class ISmsMessage(Cached):
    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('SMS', self._Id, PropName, Set)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('SMS', self._Id, AlterName, Args)

    def Send(self):
        self._Alter('SEND')

    def Delete(self):
        self._Skype._DoCommand('DELETE SMS %s' % self._Id)

    Id = property(lambda self: self._Id)
    Body = property(lambda self: self._Property('BODY'), lambda self, value: self._Property('BODY', value))
    Type = property(lambda self: self._Property('TYPE'))
    Status = property(lambda self: self._Property('STATUS'))
    FailureReason = property(lambda self: self._Property('FAILUREREASON'))
    IsFailedUnseen = property(lambda self: self._Property('IS_FAILED_UNSEEN') == 'TRUE')
    Seen = property(fset=lambda self, value: self._Property('SEEN', 'TRUE' if value else 'FALSE'))
    Timestamp = property(lambda self: float(self._Property('TIMESTAMP')))
    Price = property(lambda self: int(self._Property('PRICE')))
    PricePrecision = property(lambda self: int(self._Property('PRICE_PRECISION')))
    PriceCurrency = property(lambda self: self._Property('PRICE_CURRENCY'))
    ReplyToNumber = property(lambda self: self._Property('REPLY_TO_NUMBER'),
                             lambda self, value: self._Property('REPLY_TO_NUMBER', value))
    Targets = property(lambda self: map(lambda x: ISmsTarget(x, self), esplit(self._Property('TARGET_NUMBERS'), ', ')))
    TargetNumbers = property(lambda self: self._Property('TARGET_NUMBERS'),
                             lambda self, value: self._Property('TARGET_NUMBERS', value))
    # TODO
    # Chunks? For future use?
    Chunks = property(lambda self: [])


class ISmsTarget(object):
    def __init__(self, Number, Message):
        self._Number = Number
        self._Message = Message

    def _GetStatus(self):
        for t in esplit(self._Message._Property('TARGET_STATUSES'), ', '):
            number, status = t.split('=')
            if number == self._Number:
                return status

    Number = property(lambda self: self._Number)
    Message = property(lambda self: self._Message)
    Status = property(_GetStatus)
