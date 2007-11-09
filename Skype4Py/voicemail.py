'''Voicemails.
'''

from utils import *
from enums import *
from errors import *


class IVoicemail(Cached):
    '''Represents a voicemail.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('VOICEMAIL', self._Id, AlterName, Args)

    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('VOICEMAIL', self._Id, PropName, Set, Cache)

    def CaptureMicDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the mic capture device.

        @param DeviceType: Mic capture device type or None.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>} or None
        @param Set: Value the device should be set to or None.
        @type Set: unicode, int or None
        @return: If DeviceType and Set are None, returns a dictionary of device types and their
        values. Dictionary contains only those device types, whose values were set. If the
        DeviceType is not None but Set is None, returns the current value of the device or
        None if the device wasn't set. If Set is not None, sets a new value for the device.
        @rtype: unicode, dict or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('CAPTURE_MIC', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_CAPTURE_MIC', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def Delete(self):
        '''Deletes voicemail.
        '''
        self._Alter('DELETE')

    def Download(self):
        '''Downloads voicemail.
        '''
        self._Alter('DOWNLOAD')

    def InputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound input device.

        @param DeviceType: Sound input device type or None.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>} or None
        @param Set: Value the device should be set to or None.
        @type Set: unicode, int or None
        @return: If DeviceType and Set are None, returns a dictionary of device types and their
        values. Dictionary contains only those device types, whose values were set. If the
        DeviceType is not None but Set is None, returns the current value of the device or
        None if the device wasn't set. If Set is not None, sets a new value for the device.
        @rtype: unicode, dict or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('INPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_INPUT', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def Open(self):
        '''Opens voicemail.
        '''
        self._Skype._DoCommand('OPEN VOICEMAIL %s' % self._Id)

    def OutputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound output device.

        @param DeviceType: Sound output device type or None.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>} or None
        @param Set: Value the device should be set to or None.
        @type Set: unicode, int or None
        @return: If DeviceType and Set are None, returns a dictionary of device types and their
        values. Dictionary contains only those device types, whose values were set. If the
        DeviceType is not None but Set is None, returns the current value of the device or
        None if the device wasn't set. If Set is not None, sets a new value for the device.
        @rtype: unicode, dict or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('OUTPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_OUTPUT', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def SetUnplayed(self):
        '''Changes played voicemail status back to unplayed.
        '''
        self._Property('STATUS', vmsUnplayed)

    def StartPlayback(self):
        '''Starts voicemail playback.
        '''
        self._Alter('STARTPLAYBACK')

    def StartPlaybackInCall(self):
        '''Starts playback in call.
        '''
        self._Alter('STARTPLAYBACKINCALL')

    def StartRecording(self):
        '''Starts voicemail recording.
        '''
        self._Alter('STARTRECORDING')

    def StopPlayback(self):
        '''Stops voicemail playback.
        '''
        self._Alter('STOPPLAYBACK')

    def StopRecording(self):
        '''Stops voicemail recording.
        '''
        self._Alter('STOPRECORDING')

    def Upload(self):
        '''Uploads voicemail.
        '''
        self._Alter('UPLOAD')

    def _GetAllowedDuration(self):
        return int(self._Property('ALLOWED_DURATION'))

    AllowedDuration = property(_GetAllowedDuration,
    doc='''AllowedDuration.

    @type: int
    ''')

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc='''Datetime.

    @type: datetime.datetime
    ''')

    def _GetDuration(self):
        return int(self._Property('DURATION'))

    Duration = property(_GetDuration,
    doc='''Duration.

    @type: int
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

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName,
    doc='''PartnerDisplayName.

    @type: unicode
    ''')

    def _GetPartnerHandle(self):
        return self._Property('PARTNER_HANDLE')

    PartnerHandle = property(_GetPartnerHandle,
    doc='''PartnerHandle.

    @type: unicode
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
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
