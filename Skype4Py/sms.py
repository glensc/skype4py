'''Short messaging to cell phones.
'''

from utils import *
from enums import *


class ISmsChunk(Cached):
    '''Represents a single chunk of a multi-part SMS message.
    '''

    def _Init(self, (Id, Message)):
        self._Id = int(Id)
        self._Message = Message

    def _GetCharactersLeft(self):
        count, left = map(int, chop(self._Message._Property('CHUNKING', Cache=False)))
        if self._Id == count - 1:
            return left
        return 0

    CharactersLeft = property(_GetCharactersLeft,
    doc='''CharactersLeft.

    @type: int
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: int
    ''')

    def _GetMessage(self):
        return self._Message

    Message = property(_GetMessage,
    doc='''Message.

    @type: L{ISmsMessage}
    ''')

    def _GetText(self):
        return self._Message._Property('CHUNK %s' % self._Id)

    Text = property(_GetText,
    doc='''Text.

    @type: unicode
    ''')


class ISmsMessage(Cached):
    '''Represents an SMS message.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('SMS', self._Id, AlterName, Args)

    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('SMS', self._Id, PropName, Set, Cache)

    def Delete(self):
        '''Deletes the message.
        '''
        self._Skype._DoCommand('DELETE SMS %s' % self._Id)

    def Send(self):
        '''Sends the message.
        '''
        self._Alter('SEND')

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, value):
        self._Property('BODY', value)

    Body = property(_GetBody, _SetBody,
    doc='''Body.

    @type: unicode
    ''')

    def _GetChunks(self):
        return tuple(ISmsChunk((x, self)) for x in range(int(chop(self._Property('CHUNKING', Cache=False))[0])))

    Chunks = property(_GetChunks,
    doc='''Chunks.

    @type: tuple of L{ISmsChunk}
    ''')

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc='''Datetime.

    @type: datetime.datetime
    ''')

    def _GetFailureReason(self):
        return self._Property('FAILUREREASON')

    FailureReason = property(_GetFailureReason,
    doc='''FailureReason.

    @type: ?
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: int
    ''')

    def _GetIsFailedUnseen(self):
        return self._Property('IS_FAILED_UNSEEN') == 'TRUE'

    IsFailedUnseen = property(_GetIsFailedUnseen,
    doc='''IsFailedUnseen.

    @type: bool
    ''')

    def _GetPrice(self):
        return int(self._Property('PRICE'))

    Price = property(_GetPrice,
    doc='''Price.

    @type: int
    ''')

    def _GetPriceCurrency(self):
        return self._Property('PRICE_CURRENCY')

    PriceCurrency = property(_GetPriceCurrency,
    doc='''PriceCurrency.

    @type: unicode
    ''')

    def _GetPricePrecision(self):
        return int(self._Property('PRICE_PRECISION'))

    PricePrecision = property(_GetPricePrecision,
    doc='''PricePrecision.

    @type: int
    ''')

    def _GetPriceToText(self):
        return (u'%s %.2f' % (self.PriceCurrency, self.PriceValue)).strip()

    PriceToText = property(_GetPriceToText,
    doc='''PriceToText.

    @type: unicode
    ''')

    def _GetPriceValue(self):
        if self.Price < 0:
            return 0.0
        return float(self.Price) / (10 ** self.PricePrecision)

    PriceValue = property(_GetPriceValue,
    doc='''PriceValue.

    @type: float
    ''')

    def _GetReplyToNumber(self):
        return self._Property('REPLY_TO_NUMBER')

    def _SetReplyToNumber(self, value):
        self._Property('REPLY_TO_NUMBER', value)

    ReplyToNumber = property(_GetReplyToNumber, _SetReplyToNumber,
    doc='''ReplyToNumber.

    @type: unicode
    ''')

    def _SetSeen(self, value):
        self._Property('SEEN', cndexp(value, 'TRUE', 'FALSE'))

    Seen = property(fset=_SetSeen,
    doc='''Seen.

    @type: bool
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
    ''')

    def _GetTargetNumbers(self):
        return tuple(esplit(self._Property('TARGET_NUMBERS'), ', '))

    def _SetTargetNumbers(self, value):
        self._Property('TARGET_NUMBERS', ', '.join(value))

    TargetNumbers = property(_GetTargetNumbers, _SetTargetNumbers,
    doc='''TargetNumbers.

    @type: tuple of unicode
    ''')

    def _GetTargets(self):
        return tuple(ISmsTarget((x, self)) for x in esplit(self._Property('TARGET_NUMBERS'), ', '))

    Targets = property(_GetTargets,
    doc='''Targets.

    @type: tuple of L{ISmsTarget}
    ''')

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc='''Timestamp.

    @type: float
    ''')

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType,
    doc='''Type.

    @type: ?
    ''')


class ISmsTarget(Cached):
    '''Represents a single target of a multi-target SMS message.
    '''

    def _Init(self, (Number, Message)):
        self._Number = Number
        self._Message = Message

    def _GetMessage(self):
        return self._Message

    Message = property(_GetMessage,
    doc='''Message.

    @type: L{ISmsMessage}
    ''')

    def _GetNumber(self):
        return self._Number

    Number = property(_GetNumber,
    doc='''Number.

    @type: unicode
    ''')

    def _GetStatus(self):
        for t in esplit(self._Message._Property('TARGET_STATUSES'), ', '):
            number, status = t.split('=')
            if number == self._Number:
                return status

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
    ''')
