'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *
import os
import sys


class IFileTransfer(Cached):
    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('FILETRANSFER', self._Id, PropName, Set)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('FILETRANSFER', self._Id, AlterName, Args)

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus)

    def _GetFailureReason(self):
        return self._Property('FAILUREREASON')

    FailureReason = property(_GetFailureReason)

    def _GetPartnerHandle(self):
        return self._Property('PARTNER_HANDLE')

    PartnerHandle = property(_GetPartnerHandle)

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName)

    def _GetStartTime(self):
        return float(self._Property('STARTTIME'))

    StartTime = property(_GetStartTime)

    def _GetFinishTime(self):
        return float(self._Property('FINISHTIME'))

    FinishTime = property(_GetFinishTime)

    def _GetFilePath(self):
        return self._Property('FILEPATH').decode(sys.getfilesystemencoding())

    FilePath = property(_GetFilePath)

    def _GetFileName(self):
        return os.path.split(self._Property('FILEPATH'))[1]

    FileName = property(_GetFileName)

    def _GetBytesPerSecond(self):
        return int(self._Property('BYTESPERSECOND'))

    BytesPerSecond = property(_GetBytesPerSecond)

    def _GetBytesTransferred(self):
        return long(self._Property('BYTESTRANSFERRED'))

    BytesTransferred = property(_GetBytesTransferred)

    # Custom
    def _GetFileSize(self):
        return long(self._Property('FILESIZE'))

    FileSize = property(_GetFileSize)
