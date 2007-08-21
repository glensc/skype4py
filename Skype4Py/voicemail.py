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

    def _Property(self, PropName, SET=None, Cache=True):
        return self._Skype._Property('VOICEMAIL', self._Id, PropName, Set, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype.Alter('VOICEMAIL', self._Id, AlterName, Args)

    def Open(self):
        self._Skype._DoCommand('OPEN VOICEMAIL %s' % self._Id)

    def StartPlayback(self):
        self._Alter('STARTPLAYBACK')

    def StopPlayback(self):
        self._Alter('STOPPLAYBACK')

    def Upload(self):
        self._Alter('UPLOAD')

    def Download(self):
        self._Alter('DOWNLOAD')

    def StartRecording(self):
        self._Alter('STARTRECORDING')

    def StopRecording(self):
        self._Alter('STOPRECORDING')

    def Delete(self):
        self._Alter('DELETE')

    def StartPlaybackInCall(self):
        # TODO
        raise ISkypeError(0, 'Not implemented')

    def SetUnplayed(self):
        self._Property('STATUS', vmsUnplayed)

    def InputDevice(self, DeviceType=None, Set=None):
        if DeviceType == None and Set == None:
            a, b = self._Property('INPUT').split('=')
            return a, b[1:-1]
        elif DeviceType != None and Set != None:
            self._Alter('SET_INPUT', '%s=\"%s\"' % (DeviceType, Set))
        else:
            raise TypeError('too much or too little arguments specified')

    def OutputDevice(self, DeviceType=None, Set=None):
        if DeviceType == None and Set == None:
            a, b = self._Property('OUTPUT').split('=')
            return a, b[1:-1]
        elif DeviceType != None and Set != None:
            self._Alter('SET_OUTPUT', '%s=\"%s\"' % (DeviceType, Set))
        else:
            raise TypeError('too much or too little arguments specified')

    def CaptureMicDevice(self, DeviceType=None, Set=None):
        if DeviceType == None and Set == None:
            a, b = self._Property('CAPTURE_MIC').split('=')
            return a, b[1:-1]
        elif DeviceType != None and Set != None:
            self._Alter('SET_CAPTURE_MIC', '%s=\"%s\"' % (DeviceType, Set))
        else:
            raise TypeError('too much or too little arguments specified')

    Id = property(lambda self: self._Id)
    Type = property(lambda self: self._Property('TYPE'))
    PartnerHandle = property(lambda self: self._Property('PARTNER_HANDLE'))
    PartnerDisplayName = property(lambda self: self._Property('PARTNER_DISPNAME'))
    Status = property(lambda self: self._Property('STATUS'))
    FailureReason = property(lambda self: self._Property('FAILUREREASON'))
    Timestamp = property(lambda self: float(self._Property('TIMESTAMP')))
    Duration = property(lambda self: int(self._Property('DURATION')))
    AllowedDuration = property(lambda self: int(self._Property('ALLOWED_DURATION')))
