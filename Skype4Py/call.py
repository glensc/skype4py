'''Calls, conferences.
'''
__docformat__ = 'restructuredtext en'


from utils import *
from enums import *


class Call(Cached):
    '''Represents a voice/video call.
    '''
    _HandleCast = int

    def __repr__(self):
        return '<%s with Id=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Id))

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CALL', self.Id, AlterName, Args)
        
    def _Init(self, Owner, Handle):
        self._Skype = Owner
        self._Id = Handle

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('CALL', self.Id, PropName, Set, Cache)

    def Answer(self):
        '''Answers the call.
        '''
        self._Property('STATUS', 'INPROGRESS')

    def CanTransfer(self, Target):
        '''Queries if a call can be transferred to a contact or phone number.

        :Parameters:
          Target : str
            Skypename or phone number the call is to be transferred to.

        :return: True if call can be transferred, False otherwise.
        :rtype: bool
        '''
        return self._Property('CAN_TRANSFER %s' % Target) == 'TRUE'

    def CaptureMicDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the mic capture device.

        :Parameters:
          DeviceType : `enums`.callIoDeviceType* or None
            Mic capture device type or None.
          Set : unicode, int or None
            Value the device should be set to or None.

        :return: If DeviceType and Set are None, returns a dictionary of device types and their
                 values. Dictionary contains only those device types, whose values were set. If the
                 DeviceType is not None but Set is None, returns the current value of the device or
                 None if the device wasn't set. If Set is not None, sets a new value for the device.
        :rtype: unicode, dict or None

        :note: This command functions for active calls only.
        '''
        if Set is None: # get
            args = args2dict(self._Property('CAPTURE_MIC', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType is None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType is not None: # set
            self._Alter('SET_CAPTURE_MIC', '%s=%s' % (DeviceType, quote(tounicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def Finish(self):
        '''Ends the call.
        '''
        self._Property('STATUS', 'FINISHED')

    def Forward(self):
        '''Forwards a call.
        '''
        self._Alter('END', 'FORWARD_CALL')

    def Hold(self):
        '''Puts the call on hold.
        '''
        self._Property('STATUS', 'ONHOLD')

    def InputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound input device.

        :Parameters:
          DeviceType : `enums`.callIoDeviceType* or None
            Sound input device type or None.
          Set : unicode, int or None
            Value the device should be set to or None.

        :return: If DeviceType and Set are None, returns a dictionary of device types and their
                 values. Dictionary contains only those device types, whose values were set. If the
                 DeviceType is not None but Set is None, returns the current value of the device or
                 None if the device wasn't set. If Set is not None, sets a new value for the device.
        :rtype: unicode, dict or None

        :note: This command functions for active calls only.
        '''
        if Set is None: # get
            args = args2dict(self._Property('INPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType is None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType is not None: # set
            self._Alter('SET_INPUT', '%s=%s' % (DeviceType, quote(tounicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def Join(self, Id):
        '''Joins with another call to form a conference.

        :Parameters:
          Id : int
            Call Id of the other call to join to the conference.

        :return: Conference object.
        :rtype: `Conference`
        '''
        reply = self._Skype._DoCommand('SET CALL %s JOIN_CONFERENCE %s' % (self.Id, Id),
            'CALL %s CONF_ID' % self.Id)
        return Conference(self._Skype, reply.split()[-1])

    def MarkAsSeen(self):
        '''Marks the call as seen.
        '''
        self.Seen = True

    def OutputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound output device.

        :Parameters:
          DeviceType : `enums`.callIoDeviceType* or None
            Sound output device type or None.
          Set : unicode, int or None
            Value the device should be set to or None.

        :return: If DeviceType and Set are None, returns a dictionary of device types and their
                 values. Dictionary contains only those device types, whose values were set. If the
                 DeviceType is not None but Set is None, returns the current value of the device or
                 None if the device wasn't set. If Set is not None, sets a new value for the device.
        :rtype: unicode, dict or None

        :note: This command functions for active calls only.
        '''
        if Set is None: # get
            args = args2dict(self._Property('OUTPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType is None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType is not None: # set
            self._Alter('SET_OUTPUT', '%s=%s' % (DeviceType, quote(tounicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def RedirectToVoicemail(self):
        '''Redirects a call to voicemail.
        '''
        self._Alter('END', 'REDIRECT_TO_VOICEMAIL')

    def Resume(self):
        '''Resumes the held call.
        '''
        self.Answer()

    def StartVideoReceive(self):
        '''Starts video receive.
        '''
        self._Alter('START_VIDEO_RECEIVE')

    def StartVideoSend(self):
        '''Starts video send.
        '''
        self._Alter('START_VIDEO_SEND')

    def StopVideoReceive(self):
        '''Stops video receive.
        '''
        self._Alter('STOP_VIDEO_RECEIVE')

    def StopVideoSend(self):
        '''Stops video send.
        '''
        self._Alter('STOP_VIDEO_SEND')

    def Transfer(self, *Targets):
        '''Transfers a call to one or more contacts or phone numbers.

        :Parameters:
          Targets : str
            one or more phone numbers or Skypenames the call is being transferred to.

        :note: You can transfer an incoming call to a group by specifying more than one target,
               first one of the group to answer will get the call.
        :see: `CanTransfer`
        '''
        self._Alter('TRANSFER', ', '.join(Targets))

    def _GetConferenceId(self):
        return int(self._Property('CONF_ID'))

    ConferenceId = property(_GetConferenceId,
    doc='''ConferenceId.

    :type: int
    ''')

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc='''Date and time of the call.

    :type: datetime.datetime

    :see: `Timestamp`
    ''')

    def _SetDTMF(self, Value):
        self._Alter('DTMF', Value)

    DTMF = property(fset=_SetDTMF,
    doc='''Set this property to send DTMF codes. Permitted symbols are: [0..9, #, \*]. 

    :type: str

    :note: This command functions for active calls only.
    ''')

    def _GetDuration(self):
        return int(self._Property('DURATION', Cache=False))

    Duration = property(_GetDuration,
    doc='''Duration of the call in seconds.

    :type: int
    ''')

    def _GetFailureReason(self):
        return int(self._Property('FAILUREREASON'))

    FailureReason = property(_GetFailureReason,
    doc='''Call failure reason. Read if `Status` == `enums.clsFailed`.

    :type: `enums`.cfr*
    ''')

    def _GetForwardedBy(self):
        return str(self._Property('FORWARDED_BY'))

    ForwardedBy = property(_GetForwardedBy,
    doc='''Skypename of the user who forwarded a call.

    :type: str
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Call Id.

    :type: int
    ''')

    def _GetInputStatus(self):
        return (self._Property('VAA_INPUT_STATUS') == 'TRUE')

    InputStatus = property(_GetInputStatus,
    doc='''True if call voice input is enabled.

    :type: bool
    ''')

    def _GetParticipants(self):
        count = int(self._Property('CONF_PARTICIPANTS_COUNT'))
        return gen(Participant((self.Id, x), self._Skype) for x in xrange(count))

    Participants = property(_GetParticipants,
    doc='''Participants of a conference call not hosted by the user.

    :type: tuple of `Participant`
    ''')

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName,
    doc='''The DisplayName of the remote caller.

    :type: unicode
    ''')

    def _GetPartnerHandle(self):
        return str(self._Property('PARTNER_HANDLE'))

    PartnerHandle = property(_GetPartnerHandle,
    doc='''The Skypename of the remote caller.

    :type: str
    ''')

    def _GetPstnNumber(self):
        return str(self._Property('PSTN_NUMBER'))

    PstnNumber = property(_GetPstnNumber,
    doc='''PSTN number of the call.

    :type: str
    ''')

    def _GetPstnStatus(self):
        return self._Property('PSTN_STATUS')

    PstnStatus = property(_GetPstnStatus,
    doc='''PSTN number status.

    :type: unicode
    ''')

    def _GetRate(self):
        return int(self._Property('RATE'))

    Rate = property(_GetRate,
    doc='''Call rate. Expressed using `RatePrecision`. If you're just interested in the call rate
    expressed in current currency, use `RateValue` instead.

    :type: int

    :see: `RateCurrency`, `RatePrecision`, `RateToText`, `RateValue`
    ''')

    def _GetRateCurrency(self):
        return self._Property('RATE_CURRENCY')

    RateCurrency = property(_GetRateCurrency,
    doc='''Call rate currency.

    :type: unicode

    :see: `Rate`, `RatePrecision`, `RateToText`, `RateValue`
    ''')

    def _GetRatePrecision(self):
        return int(self._Property('RATE_PRECISION'))

    RatePrecision = property(_GetRatePrecision,
    doc='''Call rate precision. Expressed as a number of times the call rate has to be divided by 10.

    :type: int

    :see: `Rate`, `RateCurrency`, `RateToText`, `RateValue`
    ''')

    def _GetRateToText(self):
        return (u'%s %.3f' % (self.RateCurrency, self.RateValue)).strip()

    RateToText = property(_GetRateToText,
    doc='''Returns the call rate as a text with currency and properly formatted value.

    :type: unicode

    :see: `Rate`, `RateCurrency`, `RatePrecision`, `RateValue`
    ''')

    def _GetRateValue(self):
        if self.Rate < 0:
            return 0.0
        return float(self.Rate) / (10 ** self.RatePrecision)

    RateValue = property(_GetRateValue,
    doc='''Call rate value. Expressed in current currency.

    :type: float

    :see: `Rate`, `RateCurrency`, `RatePrecision`, `RateToText`
    ''')

    def _GetSeen(self):
        return self._Property('SEEN') == 'TRUE'

    def _SetSeen(self, Value):
        self._Property('SEEN', cndexp(Value, 'TRUE', 'FALSE'))

    Seen = property(_GetSeen, _SetSeen,
    doc='''Queries/sets the seen status of the call. True if the call was seen, False otherwise.

    :type: bool

    :note: You cannot alter the call seen status from seen to unseen.
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    def _SetStatus(self, Value):
        self._Property('STATUS', str(Value))

    Status = property(_GetStatus, _SetStatus,
    doc='''The call status.

    :type: `enums`.cls*
    ''')

    def _GetSubject(self):
        return self._Property('SUBJECT')

    Subject = property(_GetSubject,
    doc='''Call subject.

    :type: unicode
    ''')

    def _GetTargetIdentify(self):
        return str(self._Property('TARGET_IDENTIFY'))

    TargetIdentify = property(_GetTargetIdentify,
    doc='''Target number for incoming SkypeIn calls.

    :type: str
    ''')

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc='''Call date and time expressed as a timestamp.

    :type: float

    :see: `Datetime`
    ''')

    def _GetTransferActive(self):
        return self._Property('TRANSFER_ACTIVE') == 'TRUE'

    TransferActive = property(_GetTransferActive,
    doc='''Returns True if the call has been transferred.

    :type: bool
    ''')

    def _GetTransferredBy(self):
        return str(self._Property('TRANSFERRED_BY'))

    TransferredBy = property(_GetTransferredBy,
    doc='''Returns the Skypename of the user who transferred the call.

    :type: str
    ''')

    def _GetTransferredTo(self):
        return str(self._Property('TRANSFERRED_TO'))

    TransferredTo = property(_GetTransferredTo,
    doc='''Returns the Skypename of the user or phone number the call has been transferred to.

    :type: str
    ''')

    def _GetTransferStatus(self):
        return str(self._Property('TRANSFER_STATUS'))

    TransferStatus = property(_GetTransferStatus,
    doc='''Returns the call transfer status.

    :type: `enums`.cls*
    ''')

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc='''Call type.

    :type: `enums`.clt*
    ''')

    def _GetVideoReceiveStatus(self):
        return str(self._Property('VIDEO_RECEIVE_STATUS'))

    VideoReceiveStatus = property(_GetVideoReceiveStatus,
    doc='''Call video receive status.

    :type: `enums`.vss*
    ''')

    def _GetVideoSendStatus(self):
        return str(self._Property('VIDEO_SEND_STATUS'))

    VideoSendStatus = property(_GetVideoSendStatus,
    doc='''Call video send status.

    :type: `enums`.vss*
    ''')

    def _GetVideoStatus(self):
        return str(self._Property('VIDEO_STATUS'))

    VideoStatus = property(_GetVideoStatus,
    doc='''Call video status.

    :type: `enums`.cvs*
    ''')

    def _GetVmAllowedDuration(self):
        return int(self._Property('VM_ALLOWED_DURATION'))

    VmAllowedDuration = property(_GetVmAllowedDuration,
    doc='''Returns the permitted duration of a voicemail in seconds.

    :type: int
    ''')

    def _GetVmDuration(self):
        return int(self._Property('VM_DURATION'))

    VmDuration = property(_GetVmDuration,
    doc='''Returns the duration of a voicemail.

    :type: int
    ''')


class Participant(Cached):
    '''Represents a conference call participant.
    '''
    _HandleCast = int

    def __repr__(self):
        return '<%s with Id=%s, Idx=%s, Handle=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Id), repr(self.Idx), repr(self.Handle))

    def _Init(self, Owner, Handle):
        self._Call = Owner
        self._Idx = Handle

    def _Property(self, Prop):
        reply = self._Skype._Property('CALL', self.Id, 'CONF_PARTICIPANT %d' % self.Idx)
        return chop(reply, 3)[Prop]

    def _GetCall(self):
        return self._Call

    Call = property(_GetCall,
    doc='''Call object.

    :type: `Call`
    ''')

    def _GetCallStatus(self):
        return str(self._Property(2))

    CallStatus = property(_GetCallStatus,
    doc='''Call status of a participant in a conference call.

    :type: `enums`.cls*
    ''')

    def _GetCallType(self):
        return str(self._Property(1))

    CallType = property(_GetCallType,
    doc='''Call type in a conference call.

    :type: `enums`.clt*
    ''')

    def _GetDisplayName(self):
        return self._Property(3)

    DisplayName = property(_GetDisplayName,
    doc='''DisplayName of a participant in a conference call.

    :type: unicode
    ''')

    def _GetHandle(self):
        return str(self._Property(0))

    Handle = property(_GetHandle,
    doc='''Skypename of a participant in a conference call.

    :type: str
    ''')

    def _GetId(self):
        return self._Call.Id

    Id = property(_GetId,
    doc='''Call Id.

    :type: int
    ''')

    def _GetIdx(self):
        return self._Idx

    Idx = property(_GetIdx,
    doc='''Call participant index.

    :type: int
    ''')


class Conference(Cached):
    '''Represents a conference call.
    '''
    _HandleCast = int

    def __repr__(self):
        return '<%s with Id=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Id))

    def _Init(self, Owner, Handle):
        self._Skype = Owner
        self._Id = Handle

    def Finish(self):
        '''Finishes a conference so all active calls have the status
        `enums.clsFinished`.
        '''
        for c in self._GetCalls():
            c.Finish()

    def Hold(self):
        '''Places all calls in a conference on hold so all active calls
        have the status `enums.clsLocalHold`.
        '''
        for c in self._GetCalls():
            c.Hold()

    def Resume(self):
        '''Resumes a conference that was placed on hold so all active calls
        have the status `enums.clsInProgress`.
        '''
        for c in self._GetCalls():
            c.Resume()

    def _GetActiveCalls(self):
        return gen(x for x in self._Skype.ActiveCalls if x.ConferenceId == self.Id)

    ActiveCalls = property(_GetActiveCalls,
    doc='''Active calls with the same conference ID.

    :type: tuple of `Call`
    ''')

    def _GetCalls(self):
        return gen(x for x in self._Skype.Calls() if x.ConferenceId == self.Id)

    Calls = property(_GetCalls,
    doc='''Calls with the same conference ID.

    :type: tuple of `Call`
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id of a conference.

    :type: int
    ''')
