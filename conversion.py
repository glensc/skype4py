
from enums import *


class IConversion(object):
    def __init__(self, Skype):
        self._Skype = Skype
        self.Language = ''

    OnlineStatusToText = str
    TextToOnlineStatus = TOnlineStatus
    BuddyStatusToText = str
    TextToBuddyStatus = TBuddyStatus
    CallStatusToText = str
    TextToCallStatus = TCallStatus
    CallTypeToText = str
    TextToCallType = TCallType
    UserSexToText = str
    TextToUserSex = TUserSex
    ConnectionStatusToText = str
    TextToConnectionStatus = TConnectionStatus
    UserStatusToText = str
    TextToUserStatus = TUserStatus
    CallFailureReasonToText = str
    AttachmentStatusToText = str
    ChatLeaveReasonToText = str
    ChatStatusToText = str
    VoicemailTypeToText = str
    VoicemailStatusToText = str
    TextToVoicemailStatus = TVoicemailStatus
    VoicemailFailureReasonToText = str
    ChatMessageStatusToText = str
    TextToChatMessageStatus = TChatMessageStatus
    ChatMessageTypeToText = str
    TextToChatMessageType = TChatMessageType
    TextToAttachmentStatus = TAttachmentStatus
    GroupTypeToText = str
    TextToGroupType = TGroupType
    CallVideoStatusToText = str
    CallVideoSendStatusToText = str
    SmsMessageStatusToText = str
    SmsMessageTypeToText = str
    SmsTargetStatusToText = str
