
from utils import *


class TAttachmentStatus(Enum):
    _enum_ = ([('apiAttachUnknown', 'UNKNOWN', -1),
               ('apiAttachSuccess', 'SUCCESS', 0),
               ('apiAttachPendingAuthorization', 'PENDING', 1),
               ('apiAttachRefused', 'REFUSED', 2),
               ('apiAttachNotAvailable', 'NOT_AVAILABLE', 3),
               ('apiAttachAvailable', 'AVAILABLE', 0x8001)])


class TConnectionStatus(Enum):
    _enum_ = ([('conUnknown', 'UNKNOWN'),
               ('conOffline', 'OFFLINE'),
               ('conConnecting', 'CONNECTING'),
               ('conPausing', 'PAUSING'),
               ('conOnline', 'ONLINE')])


class TUserStatus(Enum):
    _enum_ = ([('cusUnknown', 'UNKNOWN'),
               ('cusOffline', 'OFFLINE'),
               ('cusOnline', 'ONLINE'),
               ('cusAway', 'AWAY'),
               ('cusNotAvailable', 'NA'),
               ('cusDoNotDisturb', 'DND'),
               ('cusInvisible', 'INVISIBLE'),
               ('cusLoggedOut', 'LOGGEDOUT'),
               ('cusSkypeMe', 'SKYPEME')])


class TCallFailureReason(Enum):
    _enum_ = ([('cfrUnknown', 'UNKNOWN', 0),
               ('cfrMiscError', 'MISCERROR', 1),
               ('cfrUserDoesNotExist', 'USER_DOES_NOT_EXIST', 2),
               ('cfrUserIsOffline', 'USER_IS_OFFLINE', 3),
               ('cfrNoProxyFound', 'NO_PROXY_FOUND', 4),
               ('cfrSessionTerminated', 'SESSION_TERMINATED', 5),
               ('cfrNoCommonCodec', 'NO_COMMON_CODEC', 6),
               ('cfrSoundIOError', 'SOUNDIO_ERROR', 7),
               ('cfrRemoteDeviceError', 'REMOTE_DEVICE_ERROR', 8),
               ('cfrBlockedByRecipient', 'BLOCKED_BY_RECIPIENT', 9),
               ('cfrRecipientNotFriend', 'RECIPIENT_NOT_FRIEND', 10),
               ('cfrNotAuthorizedByRecipient', 'NOT_AUTHORIZED_BY_RECIPIENT', 11),
               ('cfrSoundRecordingError', 'SOUND_RECORDING_ERROR', 12)])


class TCallStatus(Enum):
    _enum_ = ([('clsUnknown', 'NOT_AVAILABLE'),
               ('clsUnplaced', 'UNPLACED'),
               ('clsRouting', 'ROUTING'),
               ('clsEarlyMedia', 'EARLYMEDIA'),
               ('clsFailed', 'FAILED'),
               ('clsRinging', 'RINGING'),
               ('clsInProgress', 'INPROGRESS'),
               ('clsOnHold', 'ONHOLD'),
               ('clsFinished', 'FINISHED'),
               ('clsMissed', 'MISSED'),
               ('clsRefused', 'REFUSED'),
               ('clsBusy', 'BUSY'),
               ('clsCancelled', 'CANCELLED'),
               ('clsLocalHold', 'REDIAL_PENDING'),
               ('clsRemoteHold', 'WAITING_REDIAL_COMMAND'),
               ('clsVoicemailBufferingGreeting', 'VM_BUFFERING_GREETING'),
               ('clsVoicemailPlayingGreeting', 'VM_PLAYING_GREETING'),
               ('clsVoicemailRecording', 'VM_RECORDING'),
               ('clsVoicemailUploading', 'VM_UPLOADING'),
               ('clsVoicemailSent', 'VM_SENT'),
               ('clsVoicemailCancelled', 'VM_CANCELLED'),
               ('clsVoicemailFailed', 'VM_FAILED'),
               ('clsTransferring', 'TRANSFERRING'),
               ('clsTransferred', 'TRANSFERRED')])


class TCallType(Enum):
    _enum_ = ([('cltUnknown', 'UNKNOWN'),
               ('cltIncomingPSTN', 'INCOMING_PSTN'),
               ('cltOutgoingPSTN', 'OUTGOING_PSTN'),
               ('cltIncomingP2P', 'INCOMING_P2P'),
               ('cltOutgoingP2P', 'OUTGOING_P2P')])


class TCallHistory(Enum):
    _enum_ = ([('chsAllCalls', 'ALL'),
               ('chsMissedCalls', 'MISSED'),
               ('chsIncomingCalls', 'INCOMING'),
               ('chsOutgoingCalls', 'OUTGOING')])


class TCallVideoStatus(Enum):
    _enum_ = ([('cvsUnknown', 'UNKNOWN'),
               ('cvsNone', 'VIDEO_NONE'),
               ('cvsSendEnabled', 'VIDEO_SEND_ENABLED'),
               ('cvsReceiveEnabled', 'VIDEO_RECV_ENABLED'),
               ('cvsBothEnabled', 'VIDEO_BOTH_ENABLED')])


class TCallVideoSendStatus(Enum):
    _enum_ = ([('vssUnknown', 'UNKNOWN'),
               ('vssNotAvailable', 'NOT_AVAILABLE'),
               ('vssAvailable', 'AVAILABLE'),
               ('vssStarting', 'STARTING'),
               ('vssRejected', 'REJECTED'),
               ('vssRunning', 'RUNNING'),
               ('vssStopping', 'STOPPING'),
               ('vssPaused', 'PAUSED')])


class TCallIoDeviceType(Enum):
    _enum_ = ([('callIoDeviceTypeUnknown', 'UNKNOWN'),
               ('callIoDeviceTypeSoundcard', 'SOUNDCARD'),
               ('callIoDeviceTypePort', 'PORT'),
               ('callIoDeviceTypeFile', 'FILE')])


class TChatMessageType(Enum):
    _enum_ = ([('cmeUnknown', 'UNKNOWN'),
               ('cmeCreatedChatWith', 'CREATEDCHATWITH'),
               ('cmeSawMembers', 'SAWMEMBERS'),
               ('cmeAddedMembers', 'ADDEDMEMBERS'),
               ('cmeSetTopic', 'SETTOPIC'),
               ('cmeSaid', 'SAID'),
               ('cmeLeft', 'LEFT'),
               ('cmeEmoted', 'EMOTED'),
               ('cmePostedContacts', 'POSTEDCONTACTS'),
               ('cmeGapInChat', 'GAP_IN_CHAT'),
               ('cmeSetRole', 'SETROLE'),
               ('cmeKicked', 'KICKED'),
               ('cmeKickBanned', 'KICKBANNED'),
               ('cmeSetOptions', 'SETOPTIONS'),
               ('cmeSetPicture', 'SETPICTURE'),
               ('cmeSetGuidelines', 'SETGUIDELINES'),
               ('cmeJoinedAsApplicant', 'JOINEDASAPPLICANT'),
               ])


class TChatMessageStatus(Enum):
    _enum_ = ([('cmsUnknown', 'UNKNOWN'),
               ('cmsSending', 'SENDING'),
               ('cmsSent', 'SENT'),
               ('cmsReceived', 'RECEIVED'),
               ('cmsRead', 'READ')])


class TUserSex(Enum):
    _enum_ = ([('usexUnknown', 'UNKNOWN'),
               ('usexMale', 'MALE'),
               ('usexFemale', 'FEMALE')])


class TBuddyStatus(Enum):
    _enum_ = ([('budUnknown', 'UNKNOWN'),
               ('budNeverBeenFriend', 'NEVER_BEEN_FRIEND', 0),
               ('budDeletedFriend', 'DELETED_FRIEND', 1),
               ('budPendingAuthorization', 'PENDING', 2),
               ('budFriend', 'FRIEND', 3)])


class TOnlineStatus(Enum):
    _enum_ = ([('olsUnknown', 'UNKNOWN'),
               ('olsOffline', 'OFFLINE'),
               ('olsOnline', 'ONLINE'),
               ('olsAway', 'AWAY'),
               ('olsNotAvailable', 'NA'),
               ('olsDoNotDisturb', 'DND'),
               ('olsInvisible', 'INVISIBLE'),
               ('olsSkypeOut', 'SkypeOut'),
               ('olsSkypeMe', 'SKYPEME')])


class TChatLeaveReason(Enum):
    _enum_ = ([('leaUnknown', ''),
               ('leaUserNotFound', 'USER_NOT_FOUND'),
               ('leaUserIncapable', 'USER_INCAPABLE'),
               ('leaAdderNotFriend', 'ADDER_MUST_BE_FRIEND'),
               ('leaAddedNotAuthorized', 'ADDED_MUST_BE_AUTHORIZED'),
               ('leaAddDeclined', 'ADD_DECLINED'),
               ('leaUnsubscribe', 'UNSUBSCRIBE')])


class TChatStatus(Enum):
    _enum_ = ([('chsUnknown', 'UNKNOWN'),
               ('chsLegacyDialog', 'LEGACY_DIALOG'),
               ('chsDialog', 'DIALOG'),
               ('chsMultiNeedAccept', 'MULTI_NEED_ACCEPT'),
               ('chsMultiSubscribed', 'MULTI_SUBSCRIBED'),
               ('chsUnsubscribed', 'UNSUBSCRIBED')])


class TVoicemailType(Enum):
    _enum_ = ([('vmtUnknown', 'UNKNOWN'),
               ('vmtIncoming', 'INCOMING'),
               ('vmtDefaultGreeting', 'DEFAULT_GREETING'),
               ('vmtCustomGreeting', 'CUSTOM_GREETING'),
               ('vmtOutgoing', 'OUTGOING')])


class TVoicemailStatus(Enum):
    _enum_ = ([('vmsUnknown', 'UNKNOWN'),
               ('vmsNotDownloaded', 'NOT_DOWNLOADED'),
               ('vmsDownloading', 'DOWNLOADING'),
               ('vmsUnplayed', 'UNPLAYED'),
               ('vmsBuffering', 'BUFFERING'),
               ('vmsPlaying', 'PLAYING'),
               ('vmsPlayed', 'PLAYED'),
               ('vmsBlank', 'BLANK'),
               ('vmsRecording', 'RECORDING'),
               ('vmsRecorded', 'RECORDED'),
               ('vmsUploading', 'UPLOADING'),
               ('vmsUploaded', 'UPLOADED'),
               ('vmsDeleting', 'DELETING'),
               ('vmsFailed', 'FAILED')])


class TVoicemailFailureReason(Enum):
    _enum_ = ([('vmrUnknown', 'UNKNOWN'),
               ('vmrNoError', 'NO_ERROR'),
               ('vmrMiscError', 'MISC_ERROR'),
               ('vmrConnectError', 'CONNECT_ERROR'),
               ('vmrNoPrivilege', 'NO_PRIVILEGE'),
               ('vmrNoVoicemail', 'NO_VOICEMAIL'),
               ('vmrFileReadError', 'FILE_READ_ERROR'),
               ('vmrFileWriteError', 'FILE_WRITE_ERROR'),
               ('vmrRecordingError', 'RECORDING_ERROR'),
               ('vmrPlaybackError', 'PLAYBACK_ERROR')])


class TGroupType(Enum):
    _enum_ = ([('grpUnknown', 'UNKNOWN'),
               ('grpCustomGroup', 'CUSTOM_GROUP'),
               ('grpAllUsers', 'ALL_USERS'),
               ('grpAllFriends', 'ALL_FRIENDS'),
               ('grpSkypeFriends', 'SKYPE_FRIENDS'),
               ('grpSkypeOutFriends', 'SkypeOut_FRIENDS'),
               ('grpOnlineFriends', 'ONLINE_FRIENDS'),
               ('grpPendingAuthorizationFriends', 'UNKNOWN_OR_PENDINGAUTH_FRIENDS'),
               ('grpRecentlyContactedUsers', 'RECENTLY_CONTACTED_USERS'),
               ('grpUsersWaitingMyAuthorization', 'USERS_WAITING_MY_AUTHORIZATION'),
               ('grpUsersAuthorizedByMe', 'USERS_AUTHORIZED_BY_ME'),
               ('grpUsersBlockedByMe', 'USERS_BLOCKED_BY_ME'),
               ('grpUngroupedFriends', 'UNGROUPED_FRIENDS'),
               ('grpSharedGroup', 'SHARED_GROUP'),
               ('grpProposedSharedGroup', 'PROPOSED_SHARED_GROUP')])


class TCallChannelType(Enum):
    _enum_ = ([('cctUnknown', 'UNKNOWN'),
               ('cctDatagram', 'DATAGRAM'),
               ('cctReliable', 'RELIABLE')])


class TApiSecurityContext(Enum):
    _enum_ = ([('apiContextUnknown', 'UNKNOWN'),
               ('apiContextVoice', 'VOICE'),
               ('apiContextMessaging', 'MESSAGING'),
               ('apiContextAccount', 'ACCOUNT'),
               ('apiContextContacts', 'CONTACTS')])


class TSmsMessageType(Enum):
    _enum_ = ([('smsMessageTypeUnknown', 'UNKNOWN'),
               ('smsMessageTypeIncoming', 'INCOMING'),
               ('smsMessageTypeOutgoing', 'OUTGOING'),
               ('smsMessageTypeCCRequest', 'CC_REQUEST'),
               ('smsMessageTypeCCSubmit', 'CC_SUBMIT')])


class TSmsMessageStatus(Enum):
    _enum_ = ([('smsMessageStatusUnknown', 'UNKNOWN'),
               ('smsMessageStatusReceived', 'RECEIVED'),
               ('smsMessageStatusRead', 'READ'),
               ('smsMessageStatusComposing', 'COMPOSING'),
               ('smsMessageStatusSendingToServer', 'SENDING'),
               ('smsMessageStatusSentToServer', 'SENT'),
               ('smsMessageStatusDelivered', 'DELIVERED'),
               ('smsMessageStatusSomeTargetsFailed', 'SOME_TARGETS_FAILED'),
               ('smsMessageStatusFailed', 'FAILED')])


class TSmsFailureReason(Enum):
    _enum_ = ([('smsFailureReasonUnknown', 'UNKNOWN'),
               ('smsFailureReasonMiscError', 'MISC_ERROR'),
               ('smsFailureReasonServerConnectFailed', 'FAILED'),
               ('smsFailureReasonNoSmsCapability', 'NO_SMS_CAPABILITY'),
               ('smsFailureReasonInsufficientFunds', 'INSUFFICENT_FUNDS'),
               ('smsFailureReasonInvalidConfirmationCode', 'INVALID_CONFIRMATION_CODE'),
               ('smsFailureReasonUserBlocked', 'USER_BLOCKED'),
               ('smsFailureReasonIPBlocked', 'IP_BLOCKED'),
               ('smsFailureReasonNodeBlocked', 'NODE_BLOCKED')])


class TSmsTargetStatus(Enum):
    _enum_ = ([('smsTargetStatusUnknown', 'UNKNOWN'),
               ('smsTargetStatusUndefined', 'UNDEFINED'),
               ('smsTargetStatusAnalyzing', 'ANALYZING'),
               ('smsTargetStatusAcceptable', 'ACCEPTABLE'),
               ('smsTargetStatusNotRoutable', 'NO_ROUTABLE'),
               ('smsTargetStatusDeliveryPending', 'PENDING'),
               ('smsTargetStatusDeliverySuccessful', 'SUCCESSFUL'),
               ('smsTargetStatusDeliveryFailed', 'FAILED')])


class TPluginContext(Enum):
    _enum_ = ([('pluginContextUnknown', 'UNKNOWN'),
               ('pluginContextChat', 'CHAT'),
               ('pluginContextCall', 'CALL'),
               ('pluginContextContact', 'CONTACT'),
               ('pluginContextMyself', 'MYSELF'),
               ('pluginContextTools', 'TOOLS')])


class TPluginContactType(Enum):
    _enum_ = ([('pluginContactTypeUnknown', 'UNKNOWN'),
               ('pluginContactTypeAll', 'ALL'),
               ('pluginContactTypeSkype', 'SKYPE'),
               ('pluginContactTypeSkypeOut', 'SKYPEOUT')])


class TFileTransferType(Enum):
    _enum_ = ([('fileTransferTypeIncoming', 'INCOMING', 0),
               ('fileTransferTypeOutgoing', 'OUTGOING', 1)])


class TFileTransferStatus(Enum):
    _enum_ = ([('fileTransferStatusNew', 'NEW'),
               ('fileTransferStatusConnecting', 'CONNECTING'),
               ('fileTransferStatusWaitingForAccept', 'WAITING_FOR_ACCEPT'),
               ('fileTransferStatusTransferring', 'TRANSFERRING'),
               ('fileTransferStatusTransferringOverRelay', 'TRANSFERRING_OVER_RELAY'),
               ('fileTransferStatusPaused', 'PAUSED'),
               ('fileTransferStatusRemotelyPaused', 'REMOTELY_PAUSED'),
               ('fileTransferStatusCancelled', 'CANCELLED'),
               ('fileTransferStatusCompleted', 'COMPLETED'),
               ('fileTransferStatusFailed', 'FAILED')])


class TFileTransferFailureReason(Enum):
    _enum_ = ([('fileTransferFailureReasonSenderNotAuthorized', 'SENDER_NOT_AUTHORIZED'),
               ('fileTransferFailureReasonRemotelyCancelled', 'REMOTELY_CANCELLED'),
               ('fileTransferFailureReasonFailedRead', 'FAILED_READ'),
               ('fileTransferFailureReasonFailedRemoteRead', 'FAILED_REMOTE_READ'),
               ('fileTransferFailureReasonFailedWrite', 'FAILED_WRITE'),
               ('fileTransferFailureReasonFailedRemoteWrite', 'FAILED_REMOTE_WRITE'),
               ('fileTransferFailureReasonRemoteDoesNotSupportFT', 'REMOTE_DOES_NOT_SUPPORT_FT'),
               ('fileTransferFailureReasonRemoteOfflineTooLong', 'REMOTE_OFFLINE_TOO_LONG')])
