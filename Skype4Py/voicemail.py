'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *


class IVoicemail(Cached):
    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def Open(self):
        pass

    def StartPlayback(self):
        pass

    def StopPlayback(self):
        pass

    def Upload(self):
        pass

    def Download(self):
        pass

    def StartRecording(self):
        pass

    def StopRecording(self):
        pass

    def Delete(self):
        pass

    def StartPlaybackInCall(self):
        pass

    def SetUnplayed(self):
        pass
'''
TVoicemailType Type
BSTR PartnerHandle
BSTR PartnerDisplayName
TVoicemailStatus Status
TVoicemailFailureReason FailureReason
DATE Timestamp
LONG Duration
LONG AllowedDuration
LONG Id
'''
