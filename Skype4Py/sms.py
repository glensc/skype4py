'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *


class ISmsChunk(object):
    def __init__(self, Id, Message):
        self._Id = Id
        self._Message = Message

    def _GetCharactersLeft(self):
        count, left = map(int, chop(self._Message._Property('CHUNKING', Cache=False)))
        if self._Id == count - 1:
            return left
        return 0

    Id = property(lambda self: self._Id)
    CharactersLeft = property(_GetCharactersLeft)
    Text = property(lambda self: self._Message._Property('CHUNK %s' % self._Id))
    Message = property(lambda self: self._Message)


class ISmsMessage(Cached):
    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('SMS', self._Id, PropName, Set, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('SMS', self._Id, AlterName, Args)

    def Send(self):
        '''Sends the message.'''
        self._Alter('SEND')

    def Delete(self):
        '''Deletes the message.'''
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
    Chunks = property(lambda self: map(lambda x: ISmsChunk(x, self), range(int(chop(self._Property('CHUNKING', Cache=False))[0]))))


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
