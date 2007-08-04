
class ISmsChunk(object):
    pass
'''
LONG Id
LONG CharactersLeft
BSTR Text
ISmsMessage Message
'''


class ISmsMessage(object):
    def Send(self):
        pass

    def Delete(self):
        pass
'''
LONG Id
TSmsMessageType Type
TSmsMessageStatus Status
TSmsFailureReason FailureReason
VARIANT_BOOL IsFailedUnseen
VARIANT_BOOL Seen
LONG Price
LONG PricePrecision
BSTR PriceCurrency
BSTR ReplyToNumber
ISmsTargetCollection Targets
BSTR Body
ISmsChunkCollection Chunks
DATE Timestamp
BSTR TargetNumbers
'''


class ISmsTarget(object):
    pass
'''
TSmsTargetStatus Status
BSTR Number
ISmsMessage Message
'''
