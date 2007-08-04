'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

class IFileTransfer(object):
    pass
'''
BSTR Id
TFileTransferType Type
TFileTransferStatus Status
TFileTransferFailureReason FailureReason
BSTR PartnerHandle
BSTR PartnerDisplayName
DATE StartTime
DATE FinishTime
BSTR FilePath
BSTR FileName
BSTR BytesPerSecond
BSTR BytesTransferred
'''
