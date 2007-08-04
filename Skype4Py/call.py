'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *


class ICall(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None):
        return self._Skype._Property('CALL', self._Id, PropName, Value)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CALL', self._Id, AlterName, Args)

    def Hold(self):
        self._Property('STATUS', 'ONHOLD')

    def Finish(self):
        self._Property('STATUS', 'FINISHED')

    def Answer(self):
        self._Property('STATUS', 'INPROGRESS')
    Resume = Answer

    def Join(self, Id):
        self._Property('JOIN_CONFERENCE', Id)

    def StartVideoSend(self):
        self._Property('START_VIDEO_SEND', '')

    def StopVideoSend(self):
        self._Property('STOP_VIDEO_SEND', '')

    def StartVideoReceive(self):
        self._Property('START_VIDEO_RECEIVE', '')

    def StopVideoReceive(self):
        self._Property('STOP_VIDEO_RECEIVE', '')

    def RedirectToVoicemail(self):
        self._Alter('END', 'REDIRECT_TO_VOICEMAIL')

    def Forward(self):
        self._Alter('END', 'FORWARD_CALL')

    def Transfer(self, Target):
        self._Alter('TRANSFER', Target)

    def InputDevice(self, DeviceType=None, Value=None):
        if DeviceType == None and Value == None:
            a, b = self._Property('INPUT').split('=')
            return TCallIoDeviceType(a), b[1:-1]
        elif DeviceType != None and Value != None:
            self.Alter('SET_INPUT', '%s=\"%s\"' % (str(DeviceType), Value))

    def OutputDevice(self, DeviceType=None, Value=None):
        if DeviceType == None and Value == None:
            a, b = self._Property('OUTPUT').split('=')
            return TCallIoDeviceType(a), b[1:-1]
        elif DeviceType != None and Value != None:
            self.Alter('SET_OUTPUT', '%s=\"%s\"' % (str(DeviceType), Value))

    def CaptureMicDevice(self, DeviceType=None, Value=None):
        if DeviceType == None and Value == None:
            a, b = self._Property('CAPTURE_MIC').split('=')
            return TCallIoDeviceType(a), b[1:-1]
        elif DeviceType != None and Value != None:
            self.Alter('SET_CAPTURE_MIC', '%s=\"%s\"' % (str(DeviceType), Value))

    def CanTransfer(self, Target):
        return self._Property('CAN_TRANSFER %s' % Target) == 'TRUE'

    def _GetParticipants(self):
        count = int(self._Property('CONF_PARTICIPANTS_COUNT'))
        parts = []
        for i in xrange(1, count + 1):
            parts.append(IParticipant((self._Id, i), self._Skype))
        return parts

    Id = property(lambda self: self._Id)
    Timestamp = property(lambda self: int(self._Property('TIMESTAMP')))
    PartnerHandle = property(lambda self: self._Property('PARTNER_HANDLE'))
    PartnerDisplayName = property(lambda self: self._Property('PARTNER_DISPNAME'))
    ConferenceId = property(lambda self: int(self._Property('CONF_ID')))
    Type = property(lambda self: TCallType(self._Property('TYPE')))
    Status = property(lambda self: TCallStatus(self._Property('STATUS')),
                      lambda self, value: self._Property('STATUS', str(value)))
    FailureReason = property(lambda self: TCallFailureReason(int(self._Property('FAILUREREASON'))))
    Subject = property(lambda self: self._Property('SUBJECT'))
    PstnNumber = property(lambda self: self._Property('PSTN_NUMBER'))
    Duration = property(lambda self: int(self._Property('DURATION')))
    PstnStatus = property(lambda self: self._Property('PSTN_STATUS'))
    Seen = property(lambda self: self._Property('SEEN') == 'TRUE',
                    lambda self, value: self._Property('SEEN', 'TRUE' if value else 'FALSE'))
    DTMF = property(fset=lambda self, value: self._Property('DTMF', value))
    Participants = property(_GetParticipants)
    VmDuration = property(lambda self: int(self._Property('VM_DURATION')))
    VmAllowedDuration = property(lambda self: int(self._Property('VM_ALLOWED_DURATION')))
    VideoStatus = property(lambda self: TCallVideoStatus(self._Property('VIDEO_STATUS')))
    VideoSendStatus = property(lambda self: TCallVideoSendStatus(self._Property('VIDEO_SEND_STATUS')))
    VideoReceiveStatus = property(lambda self: TCallVideoSendStatus(self._Property('VIDEO_RECEIVE_STATUS')))
    Rate = property(lambda self: int(self._Property('RATE')))
    RateCurrency = property(lambda self: self._Property('RATE_CURRENCY'))
    RatePrecision = property(lambda self: int(self._Property('RATE_PRECISION')))
    InputStatus = property(lambda self: self._Property('VAA_INPUT_STATUS') == 'TRUE')
    ForwardedBy = property(lambda self: self._Property('FORWARDED_BY'))
    TransferStatus = property(lambda self: TCallStatus(self._Property('VIDEO_SEND_STATUS')))
    TransferActive = property(lambda self: self._Property('TRANSFER_ACTIVE') == 'TRUE')
    TransferredBy = property(lambda self: self._Property('TRANSFERRED_BY'))
    TransferredTo = property(lambda self: self._Property('TRANSFERRED_TO'))


class IParticipant(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id, self._Idx = Id

    def _Property(self, Prop):
        reply = self._Skype._Property('CALL', self._Id, 'CONF_PARTICIPANT %d' % self._Idx)
        return chop(reply, 7)[Prop]

    Handle = property(lambda self: self._Property(4))
    DisplayName = property(lambda self: self._Property(7))
    CallType = property(lambda self: self._Property(5))
    CallStatus = property(lambda self: self._Property(6))


# TODO:
class IConference(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None):
        return self._Skype._Property('CALL', self._Id, PropName, Value)

    def Hold(self):
        self._Property('STATUS', 'ONHOLD')

    def Resume(self):
        self._Property('STATUS', 'INPROGRESS')

    def Finish(self):
        self._Property('STATUS', 'FINISHED')

    Id = property(lambda self: self._Id)
'''
ICallCollection Calls
ICallCollection ActiveCalls
'''
