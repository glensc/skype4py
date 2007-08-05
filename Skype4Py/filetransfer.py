'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *
import os


class IFileTransfer(Cached):
    def _Init(self, Id, Skype):
        self._Id = Id
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('FILETRANSFER', self._Id, PropName, Set)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('FILETRANSFER', self._Id, AlterName, Args)

    Id = property(lambda self: self._Id)
    Type = property(lambda self: self._Property('TYPE'))
    Status = property(lambda self: self._Property('STATUS'))
    FailureReason = property(lambda self: self._Property('FAILUREREASON'))
    PartnerHandle = property(lambda self: self._Property('PARTNER_HANDLE'))
    PartnerDisplayName = property(lambda self: self._Property('PARTNER_DISPNAME'))
    StartTime = property(lambda self: float(self._Property('STARTTIME')))
    FinishTime = property(lambda self: float(self._Property('FINISHTIME')))
    FilePath = property(lambda self: self._Property('FILEPATH'))
    FileName = property(lambda self: os.path.split(self._Property('FILEPATH'))[1])
    BytesPerSecond = property(lambda self: int(self._Property('BYTESPERSECOND')))
    BytesTransferred = property(lambda self: long(self._Property('BYTESTRANSFERRED')))

    # Custom
    FileSize = property(lambda self: long(self._Property('FILESIZE')))
