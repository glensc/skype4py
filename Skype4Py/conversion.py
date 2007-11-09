'''Conversion between constants and text.
'''

import enums
from errors import *
import os


class IConversion(object):
    '''Allows conversion between constants and text. Access using L{ISkype.Convert}.
    '''

    def __init__(self, Skype):
        '''__init__.

        @param Skype: Skype
        @type Skype: ?
        '''
        self._Language = u''
        self._Module = None
        self._SetLanguage('en')

    def _TextTo(self, prefix, value):
        enum = [z for z in [(y, getattr(enums, y)) for y in [x for x in dir(enums) if x.startswith(prefix)]] if z[1] == value]
        if enum:
            return str(value)
        raise ISkypeError(0, 'Bad text')

    def _ToText(self, prefix, value):
        enum = [z for z in [(y, getattr(enums, y)) for y in [x for x in dir(enums) if x.startswith(prefix)]] if z[1] == value]
        if enum:
            try:
                return unicode(getattr(self._Module, enum[0][0]))
            except AttributeError:
                pass
        raise ISkypeError(0, 'Bad identifier')

    def AttachmentStatusToText(self, Status):
        '''Returns attachment status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('api', Status)

    def BuddyStatusToText(self, Status):
        '''Returns buddy status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('bud', Status)

    def CallFailureReasonToText(self, Reason):
        '''Returns failure reason as text.

        @param Reason: Reason
        @type Reason: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cfr', Reason)

    def CallStatusToText(self, Status):
        '''Returns call status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cls', Status)

    def CallTypeToText(self, Type):
        '''Returns call type as text.

        @param Type: Type
        @type Type: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('clt', Type)

    def CallVideoSendStatusToText(self, Status):
        '''Returns call video send status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('vss', Status)

    def CallVideoStatusToText(self, Status):
        '''Returns call video status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cvs', Status)

    def ChatLeaveReasonToText(self, Reason):
        '''Returns leave reason as text.

        @param Reason: Reason
        @type Reason: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('lea', Reason)

    def ChatMessageStatusToText(self, Status):
        '''Returns message status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cms', Status)

    def ChatMessageTypeToText(self, Type):
        '''Returns message type as text.

        @param Type: Type
        @type Type: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cme', Type)

    def ChatStatusToText(self, Status):
        '''Returns chatr status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('chs', Status)

    def ConnectionStatusToText(self, Status):
        '''Returns connection status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('con', Status)

    def GroupTypeToText(self, Type):
        '''Returns group type as text.

        @param Type: Type
        @type Type: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('grp', Type)

    def OnlineStatusToText(self, Status):
        '''Returns online status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('ols', Status)

    def SmsMessageStatusToText(self, Status):
        '''Returns SMS message status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('smsMessageStatus', Status)

    def SmsMessageTypeToText(self, Type):
        '''Returns SMS message type as text.

        @param Type: Type
        @type Type: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('smsMessageType', Type)

    def SmsTargetStatusToText(self, Status):
        '''Returns SMS target status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('smsTargetStatus', Status)

    def TextToAttachmentStatus(self, Text):
        '''Returns attachment status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('api', Text)

    def TextToBuddyStatus(self, Text):
        '''Returns buddy status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('bud', Text)

    def TextToCallStatus(self, Text):
        '''Returns call status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('cls', Text)

    def TextToCallType(self, Text):
        '''Returns call type code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('clt', Text)

    def TextToChatMessageStatus(self, Text):
        '''Returns message status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('cms', Text)

    def TextToChatMessageType(self, Text):
        '''Returns message type code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('cme', Text)

    def TextToConnectionStatus(self, Text):
        '''TextToConnectionStatus.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('con', Text)

    def TextToGroupType(self, Text):
        '''Returns group type code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('grp', Text)

    def TextToOnlineStatus(self, Text):
        '''Returns online status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('ols', Text)

    def TextToUserSex(self, Text):
        '''Returns user sex code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('usex', Text)

    def TextToUserStatus(self, Text):
        '''Returns user status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('cus', Text)

    def TextToVoicemailStatus(self, Text):
        '''Returns voicemail status code.

        @param Text: Text
        @type Text: unicode
        @return: ?
        @rtype: ?
        '''
        return self._TextTo('vms', Text)

    def UserSexToText(self, Sex):
        '''Returns user sex as text.

        @param Sex: Sex
        @type Sex: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('usex', Sex)

    def UserStatusToText(self, Status):
        '''Returns user status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('cus', Status)

    def VoicemailFailureReasonToText(self, Reason):
        '''Returns voicemail failure reason as text.

        @param Reason: Reason
        @type Reason: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('vmr', Reason)

    def VoicemailStatusToText(self, Status):
        '''Returns voicemail status as text.

        @param Status: Status
        @type Status: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('vms', Status)

    def VoicemailTypeToText(self, Type):
        '''Returns voicemail type as text.

        @param Type: Type
        @type Type: ?
        @return: ?
        @rtype: ?
        '''
        return self._ToText('vmt', Type)

    def _GetLanguage(self):
        return self._Language

    def _SetLanguage(self, Language):
        try:
            self._Module = __import__('Languages.%s' % str(Language), globals(), locals(), ['Languages'])
            self._Language = unicode(Language)
        except ImportError:
            pass

    Language = property(_GetLanguage, _SetLanguage,
    doc='''Language.

    @type: ?
    ''')
