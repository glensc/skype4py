'''File transfers.
'''

from utils import *
from enums import *
import os


class IFileTransfer(Cached):
    '''Represents a file transfer.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('FILETRANSFER', self._Id, AlterName, Args)

    def _Init(self, Id, Skype):
        self._Id = int(Id)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('FILETRANSFER', self._Id, PropName, Set)

    def _GetBytesPerSecond(self):
        return int(self._Property('BYTESPERSECOND'))

    BytesPerSecond = property(_GetBytesPerSecond,
    doc='''BytesPerSecond.

    @type: int
    ''')

    def _GetBytesTransferred(self):
        return long(self._Property('BYTESTRANSFERRED'))

    BytesTransferred = property(_GetBytesTransferred,
    doc='''BytesTransferred.

    @type: long
    ''')

    def _GetFailureReason(self):
        return self._Property('FAILUREREASON')

    FailureReason = property(_GetFailureReason,
    doc='''FailureReason.

    @type: ?
    ''')

    def _GetFileName(self):
        return os.path.split(self.FilePath)[1]

    FileName = property(_GetFileName,
    doc='''FileName.

    @type: unicode
    ''')

    def _GetFilePath(self):
        return self._Property('FILEPATH')

    FilePath = property(_GetFilePath,
    doc='''FilePath.

    @type: unicode
    ''')

    def _GetFileSize(self):
        return long(self._Property('FILESIZE'))

    FileSize = property(_GetFileSize,
    doc='''FileSize.

    @type: long
    ''')

    def _GetFinishDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.FinishTime)

    FinishDatetime = property(_GetFinishDatetime,
    doc='''FinishDatetime.

    @type: datetime.datetime
    ''')

    def _GetFinishTime(self):
        return float(self._Property('FINISHTIME'))

    FinishTime = property(_GetFinishTime,
    doc='''FinishTime.

    @type: float
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

    def _GetStartDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.StartTime)

    StartDatetime = property(_GetStartDatetime,
    doc='''StartDatetime.

    @type: datetime.datetime
    ''')

    def _GetStartTime(self):
        return float(self._Property('STARTTIME'))

    StartTime = property(_GetStartTime,
    doc='''StartTime.

    @type: float
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
    ''')

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType,
    doc='''Type.

    @type: ?
    ''')
