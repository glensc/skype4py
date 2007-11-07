'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *
from errors import *


class IVoicemail(Cached):
    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('VOICEMAIL', self._Id, PropName, Set, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('VOICEMAIL', self._Id, AlterName, Args)

    def Open(self):
        '''Opens voicemail.'''
        self._Skype._DoCommand('OPEN VOICEMAIL %s' % self._Id)

    def StartPlayback(self):
        '''Starts voicemail playback.'''
        self._Alter('STARTPLAYBACK')

    def StopPlayback(self):
        '''Stops voicemail playback.'''
        self._Alter('STOPPLAYBACK')

    def StartPlaybackInCall(self):
        '''Starts playback in call.'''
        self._Alter('STARTPLAYBACKINCALL')

    def Upload(self):
        '''Uploads voicemail.'''
        self._Alter('UPLOAD')

    def Download(self):
        '''Downloads voicemail.'''
        self._Alter('DOWNLOAD')

    def StartRecording(self):
        '''Starts voicemail recording.'''
        self._Alter('STARTRECORDING')

    def StopRecording(self):
        '''Stops voicemail recording.'''
        self._Alter('STOPRECORDING')

    def Delete(self):
        '''Deletes voicemail.'''
        self._Alter('DELETE')

    def SetUnplayed(self):
        '''Changes played voicemail status back to unplayed.'''
        self._Property('STATUS', vmsUnplayed)

    def InputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound input device.

        @param DeviceType: Sound input device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('INPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
                elif t == callIoDeviceTypeFile:
                    args[t] = args[t].encode(sys.getfilesystemencoding())
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_INPUT', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def OutputDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the sound output device.

        @param DeviceType: Sound output device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('OUTPUT', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
                elif t == callIoDeviceTypeFile:
                    args[t] = args[t].encode(sys.getfilesystemencoding())
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_OUTPUT', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def CaptureMicDevice(self, DeviceType=None, Set=None):
        '''Queries or sets the mic capture device.

        @param DeviceType: Mic capture device type.
        @type DeviceType: L{Call IO device type<enums.callIoDeviceTypeUnknown>}
        @param Set: Value the device should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Device value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        if Set == None: # get
            args = args2dict(self._Property('CAPTURE_MIC', Cache=False))
            for t in args:
                if t == callIoDeviceTypePort:
                    args[t] = int(args[t])
                elif t == callIoDeviceTypeFile:
                    args[t] = args[t].encode(sys.getfilesystemencoding())
            if DeviceType == None: # get active devices
                return args
            return args.get(DeviceType, None)
        elif DeviceType != None: # set
            self._Alter('SET_CAPTURE_MIC', '%s=%s' % (DeviceType, quote(unicode(Set), True)))
        else:
            raise TypeError('DeviceType must be specified if Set is used')

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _GetPartnerHandle(self):
        return self._Property('PARTNER_HANDLE')

    PartnerHandle = property(_GetPartnerHandle)

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName)

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus)

    def _GetFailureReason(self):
        return self._Property('FAILUREREASON')

    FailureReason = property(_GetFailureReason)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime)

    def _GetDuration(self):
        return int(self._Property('DURATION'))

    Duration = property(_GetDuration)

    def _GetAllowedDuration(self):
        return int(self._Property('ALLOWED_DURATION'))

    AllowedDuration = property(_GetAllowedDuration)
