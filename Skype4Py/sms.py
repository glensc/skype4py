'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *


class ISmsChunk(Cached):
    def _Init(self, (Id, Message)):
        self._Id = Id
        self._Message = Message

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetCharactersLeft(self):
        count, left = map(int, chop(self._Message._Property('CHUNKING', Cache=False)))
        if self._Id == count - 1:
            return left
        return 0

    CharactersLeft = property(_GetCharactersLeft)

    def _GetText(self):
        return self._Message._Property('CHUNK %s' % self._Id)

    Text = property(_GetText)

    def _GetMessage(self):
        return self._Message

    Message = property(_GetMessage)


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

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, value):
        self._Property('BODY', value)

    Body = property(_GetBody, _SetBody)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus)

    def _GetFailureReason(self):
        return self._Property('FAILUREREASON')

    FailureReason = property(_GetFailureReason)

    def _GetIsFailedUnseen(self):
        return self._Property('IS_FAILED_UNSEEN') == 'TRUE'

    IsFailedUnseen = property(_GetIsFailedUnseen)

    def _SetSeen(self, value):
        self._Property('SEEN', cndexp(value, 'TRUE', 'FALSE'))

    Seen = property(fset=_SetSeen)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime)

    def _GetPrice(self):
        return int(self._Property('PRICE'))

    Price = property(_GetPrice)

    def _GetPricePrecision(self):
        return int(self._Property('PRICE_PRECISION'))

    PricePrecision = property(_GetPricePrecision)

    def _GetPriceCurrency(self):
        return self._Property('PRICE_CURRENCY')

    PriceCurrency = property(_GetPriceCurrency)

    def _GetPriceValue(self):
        return float(self._Property('PRICE')) / (10 ** float(self._Property('PRICE_PRECISION')))

    PriceValue = property(_GetPriceValue)

    def _GetPriceToText(self):
        return (u'%s %.2f' % (self.PriceCurrency, self.PriceValue)).strip()

    PriceToText = property(_GetPriceToText)

    def _GetReplyToNumber(self):
        return self._Property('REPLY_TO_NUMBER')

    def _SetReplyToNumber(self, value):
        self._Property('REPLY_TO_NUMBER', value)

    ReplyToNumber = property(_GetReplyToNumber, _SetReplyToNumber)

    def _GetTargets(self):
        return tuple(ISmsTarget((x, self)) for x in esplit(self._Property('TARGET_NUMBERS'), ', '))

    Targets = property(_GetTargets)

    def _GetTargetNumbers(self):
        return self._Property('TARGET_NUMBERS')

    def _SetTargetNumbers(self, value):
        self._Property('TARGET_NUMBERS', value)

    TargetNumbers = property(_GetTargetNumbers, _SetTargetNumbers)

    def _GetChunks(self):
        return tuple(ISmsChunk((x, self)) for x in range(int(chop(self._Property('CHUNKING', Cache=False))[0])))

    Chunks = property(_GetChunks)


class ISmsTarget(Cached):
    def _Init(self, (Number, Message)):
        self._Number = Number
        self._Message = Message

    def _GetNumber(self):
        return self._Number

    Number = property(_GetNumber)

    def _GetMessage(self):
        return self._Message

    Message = property(_GetMessage)

    def _GetStatus(self):
        for t in esplit(self._Message._Property('TARGET_STATUSES'), ', '):
            number, status = t.split('=')
            if number == self._Number:
                return status

    Status = property(_GetStatus)
