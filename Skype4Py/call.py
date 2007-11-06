'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *
from errors import *


class ICall(Cached):
    '''Represents a call.'''

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('CALL', self._Id, PropName, Set, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CALL', self._Id, AlterName, Args)

    def Hold(self):
        '''Puts the call on hold.'''
        self._Property('STATUS', 'ONHOLD')

    def Finish(self):
        '''Ends the call.'''
        self._Property('STATUS', 'FINISHED')

    def Answer(self):
        '''Answers the call.'''
        self._Property('STATUS', 'INPROGRESS')

    def Resume(self):
        '''Resumes the held call.'''
        self.Answer()

    def Join(self, Id):
        '''Joins with another call to form a conference.

        @param Id: Call Id of the other call to join to the conference.
        @type Id: int
        @return: Conference object.
        @rtype: L{IConference}
        '''
        self._Property('JOIN_CONFERENCE', Id)
        return IConference(self.ConferenceId, self._Skype)

    def StartVideoSend(self):
        '''Starts video send.'''
        self._Alter('START_VIDEO_SEND')

    def StopVideoSend(self):
        '''Stops video send.'''
        self._Alter('STOP_VIDEO_SEND')

    def StartVideoReceive(self):
        '''Starts video receive.'''
        self._Alter('START_VIDEO_RECEIVE')

    def StopVideoReceive(self):
        '''Stops video receive.'''
        self._Alter('STOP_VIDEO_RECEIVE')

    def RedirectToVoicemail(self):
        '''Redirects a call to voicemail.'''
        self._Alter('END', 'REDIRECT_TO_VOICEMAIL')

    def Forward(self):
        '''Forwards a call.'''
        self._Alter('END', 'FORWARD_CALL')

    def Transfer(self, *Targets):
        '''Transfers a call to one or more contacts or phone numbers.

        @param Targets: one or more phone numbers or Skypenames the call is beeing transferred to.
        @type Targets: unicode
        @see: L{CanTransfer}
        '''
        self._Alter('TRANSFER', Target)

    def InputDevice(self, DeviceType, Set=None):
        '''Queries or sets the sound input device.

        @param DeviceType: Sound input device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None:
            try:
                value = dict([x.split('=') for x in esplit(self._Property('INPUT'), ', ')])[DeviceType]
            except KeyError:
                return u''
            return value[1:-1]
        else:
            self._Alter('SET_INPUT', '%s=\"%s\"' % (DeviceType, Set))

    def OutputDevice(self, DeviceType, Set=None):
        '''Queries or sets the sound output device.

        @param DeviceType: Sound output device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None:
            try:
                value = dict([x.split('=') for x in esplit(self._Property('OUTPUT'), ', ')])[DeviceType]
            except KeyError:
                return u''
            return value[1:-1]
        else:
            self._Alter('SET_OUTPUT', '%s=\"%s\"' % (DeviceType, Set))

    def CaptureMicDevice(self, DeviceType, Set=None):
        '''Queries or sets the mic capture device.

        @param DeviceType: Mic capture device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None:
            try:
                value = dict([x.split('=') for x in esplit(self._Property('CAPTURE_MIC'), ', ')])[DeviceType]
            except KeyError:
                return u''
            return value[1:-1]
        else:
            self._Alter('SET_CAPTURE_MIC', '%s=\"%s\"' % (DeviceType, Set))

    def CanTransfer(self, Target):
        '''Queries if a call can be transferred to a contact or phone number.

        @param Target: Skypename or phone number the call is to be transfered to.
        @type Target: unicode
        @return: True if call can be transfered, False otherwise.
        @rtype: bool
        '''
        return self._Property('CAN_TRANSFER %s' % Target) == 'TRUE'

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp)

    def _GetPartnerHandle(self):
        return self._Property('PARTNER_HANDLE')

    PartnerHandle = property(_GetPartnerHandle)

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName)

    def _GetConferenceId(self):
        return int(self._Property('CONF_ID'))

    ConferenceId = property(_GetConferenceId)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _GetStatus(self):
        return self._Property('STATUS')

    def _SetStatus(self, value):
        self._Property('STATUS', str(value))

    Status = property(_GetStatus, _SetStatus)

    def _GetFailureReason(self):
        return int(self._Property('FAILUREREASON'))

    FailureReason = property(_GetFailureReason)

    def _GetSubject(self):
        return self._Property('SUBJECT')

    Subject = property(_GetSubject)

    def _GetPstnNumber(self):
        return self._Property('PSTN_NUMBER')

    PstnNumber = property(_GetPstnNumber)

    def _GetDuration(self):
        return int(self._Property('DURATION', Cache=False))

    Duration = property(_GetDuration)

    def _GetPstnStatus(self):
        return self._Property('PSTN_STATUS')

    PstnStatus = property(_GetPstnStatus)

    def _GetSeen(self):
        return self._Property('SEEN') == 'TRUE'

    def _SetSeen(self, value):
        self._Property('SEEN', cndexp(value, 'TRUE', 'FALSE'))

    Seen = property(_GetSeen, _SetSeen)

    def _SetDTMF(self, value):
        self._Property('DTMF', value)

    DTMF = property(fset=_SetDTMF)

    def _GetParticipants(self):
        count = int(self._Property('CONF_PARTICIPANTS_COUNT'))
        return tuple(IParticipant((self._Id, x), self._Skype) for x in xrange(1, count + 1))

    Participants = property(_GetParticipants)

    def _GetVmDuration(self):
        return int(self._Property('VM_DURATION'))

    VmDuration = property(_GetVmDuration)

    def _GetVmAllowedDuration(self):
        return int(self._Property('VM_ALLOWED_DURATION'))

    VmAllowedDuration = property(_GetVmAllowedDuration)

    def _GetVideoStatus(self):
        return self._Property('VIDEO_STATUS')

    VideoStatus = property(_GetVideoStatus)

    def _GetVideoSendStatus(self):
        return self._Property('VIDEO_SEND_STATUS')

    VideoSendStatus = property(_GetVideoSendStatus)

    def _GetVideoReceiveStatus(self):
        return self._Property('VIDEO_RECEIVE_STATUS')

    VideoReceiveStatus = property(_GetVideoReceiveStatus)

    def _GetRate(self):
        return int(self._Property('RATE'))

    Rate = property(_GetRate)

    def _GetRatePrecision(self):
        return int(self._Property('RATE_PRECISION'))

    RatePrecision = property(_GetRatePrecision)

    def _GetRateCurrency(self):
        return self._Property('RATE_CURRENCY')

    RateCurrency = property(_GetRateCurrency)

    def _GetRateValue(self):
        return float(self._Property('RATE')) / (10 ** float(self._Property('RATE_PRECISION')))

    RateValue = property(_GetRateValue)

    def _GetRateToText(self):
        return (u'%s %.2f' % (self.RateCurrency, self.RateValue)).strip()

    RateToText = property(_GetRateToText)

    def _GetInputStatus(self):
        return self._Property('VAA_INPUT_STATUS') == 'TRUE'

    InputStatus = property(_GetInputStatus)

    def _GetForwardedBy(self):
        return self._Property('FORWARDED_BY')

    ForwardedBy = property(_GetForwardedBy)

    def _GetTransferStatus(self):
        return self._Property('TRANSFER_STATUS')

    TransferStatus = property(_GetTransferStatus)

    def _GetTransferActive(self):
        return self._Property('TRANSFER_ACTIVE') == 'TRUE'

    TransferActive = property(_GetTransferActive)

    def _GetTransferredBy(self):
        return self._Property('TRANSFERRED_BY')

    TransferredBy = property(_GetTransferredBy)

    def _GetTransferredTo(self):
        return self._Property('TRANSFERRED_TO')

    TransferredTo = property(_GetTransferredTo)

    def _GetTargetIdentify(self):
        return self._Property('TARGET_IDENTIFY')

    TargetIdentify = property(_GetTargetIdentify)


class IParticipant(Cached):
    def _Init(self, (Id, Idx), Skype):
        self._Skype = Skype
        self._Id = Id
        self._Idx = Idx

    def _Property(self, Prop):
        reply = self._Skype._Property('CALL', self._Id, 'CONF_PARTICIPANT %d' % self._Idx)
        return chop(reply, 7)[Prop]

    def _GetHandle(self):
        return self._Property(4)

    Handle = property(_GetHandle)

    def _GetDisplayName(self):
        return self._Property(7)

    DisplayName = property(_GetDisplayName)

    def _GetCallType(self):
        return self._Property(5)

    CallType = property(_GetCallType)

    def _GetCallStatus(self):
        return self._Property(6)

    CallStatus = property(_GetCallStatus)


class IConference(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def Hold(self):
        '''Hold conference.'''
        for c in self._GetCalls():
            c.Hold()

    def Resume(self):
        '''Resume conference.'''
        for c in self._GetCalls():
            c.Resume()

    def Finish(self):
        '''End conference.'''
        for c in self._GetCalls():
            c.Finish()

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetCalls(self):
        return tuple(x for x in self._Skype.Calls() if c.ConferenceId == self._Id)

    Calls = property(_GetCalls)

    def _GetActiveCalls(self):
        return tuple(x for x in self._Skype.ActiveCalls if c.ConferenceId == self._Id)

    ActiveCalls = property(_GetActiveCalls)
