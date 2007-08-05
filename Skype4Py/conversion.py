'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from enums import *
from errors import *
import os


class IConversion(object):
    def __init__(self, Skype):
        self._Skype = Skype
        self._Language = u''
        self._Dict = {}
        self._SetLanguage('en')

    def _ToText(self, prefix, value):
        for id_ in self._Dict:
            value_, txt = self._Dict[id_]
            if id_.startswith(prefix) and value_ == value:
                return txt
        raise ISkypeError(0, 'Identifier not found')

    def _TextTo(self, prefix, txt):
        for id_ in self._Dict:
            value, txt_ = self._Dict[id_]
            if id_.startswith(prefix) and txt_.lower() == txt.lower():
                return value
        raise ISkypeError(0, 'Text not found')

    def _SetLanguage(self, Language):
        path = os.path.join(os.path.split(__file__)[0], 'Languages')
        try:
            f = file(os.path.join(path, Language), 'rb')
            data = f.read().decode('utf-16')
            f.close()
        except:
            return
        self._Dict = {}
        self._Language = unicode(Language)
        for ln in data.replace('\r\n', '\n').split('\n'):
            ln = ln.strip()
            if not ln:
                continue
            p = ln.find('=')
            if p < 0:
                raise ISkypeError(0, 'Error in language %s: Missing \'=\' char' % Language)
            id_ = ln[:p].strip()
            try:
                value = globals()[id_]
            except KeyError:
                raise ISkypeError(0, 'Error in language %s: Unknown identifier' % Language)
            txt = ln[p + 1:].strip()
            self._Dict[str(id_)] = value, txt

    def OnlineStatusToText(self, status):
        return self._ToText('ols', status)

    def TextToOnlineStatus(self, Text):
        return self._TextTo('ols', Text)

    def BuddyStatusToText(self, status):
        return self._ToText('bud', status)

    def TextToBuddyStatus(self, Text):
        return self._TextTo('bud', Text)

    def CallStatusToText(self, Status):
        return self._ToText('cls', Status)

    def TextToCallStatus(self, Text):
        return self._TextTo('cls', Text)

    def CallTypeToText(self, CallType):
        return self._ToText('clt', CallType)

    def TextToCallType(self, Text):
        return self._TextTo('clt', Text)

    def UserSexToText(self, Sex):
        return self._ToText('usex', Sex)

    def UserSexToText(self, Text):
        return self._ToText('usex', Text)

    def ConnectionStatusToText(self, Status):
        return self._ToText('con', Status)

    def ConnectionStatusToText(self, Text):
        return self._ToText('con', Text)

    def UserStatusToText(self, Status):
        return self._ToText('cus', Status)

    def TextToUserStatus(self, Text):
        return self._TextTo('cus', Text)

    def CallFailureReasonToText(self, reason):
        return self._ToText('cfr', reason)

    def AttachmentStatusToText(self, status):
        return self._ToText('api', status)

    def ChatLeaveReasonToText(self, reason):
        return self._ToText('lea', reason)

    def ChatStatusToText(self, status):
        return self._ToText('chs', status)

    def VoicemailTypeToText(self, type_):
        return self._ToText('vmt', type_)

    def VoicemailStatusToText(self, status):
        return self._ToText('vms', status)

    def TextToVoicemailStatus(self, Text):
        return self._TextTo('vms', Text)

    def VoicemailFailureReasonToText(self, reason):
        return self._ToText('vmr', reason)

    def ChatMessageStatusToText(self, Status):
        return self._ToText('cms', Status)

    def TextToChatMessageStatus(self, Text):
        return self._TextTo('cms', Text)

    def ChatMessageTypeToText(self, Type):
        return self._ToText('cme', Type)

    def TextToChatMessageType(self, Text):
        return self._TextTo('cme', Text)

    def TextToAttachmentStatus(self, Text):
        return self._TextTo('api', Text)

    def GroupTypeToText(self, Type):
        return self._ToText('grp', Type)

    def TextToGroupType(self, Text):
        return self._TextTo('grp', Text)

    def CallVideoStatusToText(self, Status):
        return self._ToText('cvs', Status)

    def CallVideoSendStatusToText(self, Status):
        return self._ToText('vss', Status)

    def SmsMessageStatusToText(self, status):
        return self._ToText('smsMessageStatus', status)

    def SmsMessageTypeToText(self, type_):
        return self._ToText('smsMessageType', type_)

    def SmsTargetStatusToText(self, status):
        return self._ToText('smsTargetStatus', status)

    Language = property(lambda self: self._Language, _SetLanguage)
