'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *


# TAttachmentStatus
apiAttachUnknown = -1
apiAttachSuccess = 0
apiAttachPendingAuthorization = 1
apiAttachRefused = 2
apiAttachNotAvailable = 3
apiAttachAvailable = 0x8001


# TConnectionStatus
conUnknown = 'UNKNOWN'
conOffline = 'OFFLINE'
conConnecting = 'CONNECTING'
conPausing = 'PAUSING'
conOnline = 'ONLINE'


# TUserStatus
cusUnknown = 'UNKNOWN'
cusOffline = 'OFFLINE'
cusOnline = 'ONLINE'
cusAway = 'AWAY'
cusNotAvailable = 'NA'
cusDoNotDisturb = 'DND'
cusInvisible = 'INVISIBLE'
cusLoggedOut = 'LOGGEDOUT'
cusSkypeMe = 'SKYPEME'


# TCallFailureReason
cfrUnknown = -1
cfrMiscError = 1
cfrUserDoesNotExist = 2
cfrUserIsOffline = 3
cfrNoProxyFound = 4
cfrSessionTerminated = 5
cfrNoCommonCodec = 6
cfrSoundIOError = 7
cfrRemoteDeviceError = 8
cfrBlockedByRecipient = 9
cfrRecipientNotFriend = 10
cfrNotAuthorizedByRecipient = 11
cfrSoundRecordingError = 12


# TCallStatus
clsUnknown = 'NOT_AVAILABLE'
clsUnplaced = 'UNPLACED'
clsRouting = 'ROUTING'
clsEarlyMedia = 'EARLYMEDIA'
clsFailed = 'FAILED'
clsRinging = 'RINGING'
clsInProgress = 'INPROGRESS'
clsOnHold = 'ONHOLD'
clsFinished = 'FINISHED'
clsMissed = 'MISSED'
clsRefused = 'REFUSED'
clsBusy = 'BUSY'
clsCancelled = 'CANCELLED'
clsLocalHold = 'REDIAL_PENDING'
clsRemoteHold = 'WAITING_REDIAL_COMMAND'
clsVoicemailBufferingGreeting = 'VM_BUFFERING_GREETING'
clsVoicemailPlayingGreeting = 'VM_PLAYING_GREETING'
clsVoicemailRecording = 'VM_RECORDING'
clsVoicemailUploading = 'VM_UPLOADING'
clsVoicemailSent = 'VM_SENT'
clsVoicemailCancelled = 'VM_CANCELLED'
clsVoicemailFailed = 'VM_FAILED'
clsTransferring = 'TRANSFERRING'
clsTransferred = 'TRANSFERRED'


# TCallType
cltUnknown = 'UNKNOWN'
cltIncomingPSTN = 'INCOMING_PSTN'
cltOutgoingPSTN = 'OUTGOING_PSTN'
cltIncomingP2P = 'INCOMING_P2P'
cltOutgoingP2P = 'OUTGOING_P2P'


# TCallHistory
chsAllCalls = 'ALL'
chsMissedCalls = 'MISSED'
chsIncomingCalls = 'INCOMING'
chsOutgoingCalls = 'OUTGOING'


# TCallVideoStatus
cvsUnknown = 'UNKNOWN'
cvsNone = 'VIDEO_NONE'
cvsSendEnabled = 'VIDEO_SEND_ENABLED'
cvsReceiveEnabled = 'VIDEO_RECV_ENABLED'
cvsBothEnabled = 'VIDEO_BOTH_ENABLED'


# TCallVideoSendStatus
vssUnknown = 'UNKNOWN'
vssNotAvailable = 'NOT_AVAILABLE'
vssAvailable = 'AVAILABLE'
vssStarting = 'STARTING'
vssRejected = 'REJECTED'
vssRunning = 'RUNNING'
vssStopping = 'STOPPING'
vssPaused = 'PAUSED'


# TCallIoDeviceType
callIoDeviceTypeUnknown = 'UNKNOWN'
callIoDeviceTypeSoundcard = 'SOUNDCARD'
callIoDeviceTypePort = 'PORT'
callIoDeviceTypeFile = 'FILE'


# TChatMessageType
cmeUnknown = 'UNKNOWN'
cmeCreatedChatWith = 'CREATEDCHATWITH'
cmeSawMembers = 'SAWMEMBERS'
cmeAddedMembers = 'ADDEDMEMBERS'
cmeSetTopic = 'SETTOPIC'
cmeSaid = 'SAID'
cmeLeft = 'LEFT'
cmeEmoted = 'EMOTED'
cmePostedContacts = 'POSTEDCONTACTS'
cmeGapInChat = 'GAP_IN_CHAT'
cmeSetRole = 'SETROLE'
cmeKicked = 'KICKED'
cmeKickBanned = 'KICKBANNED'
cmeSetOptions = 'SETOPTIONS'
cmeSetPicture = 'SETPICTURE'
cmeSetGuidelines = 'SETGUIDELINES'
cmeJoinedAsApplicant = 'JOINEDASAPPLICANT'


# TChatMessageStatus
cmsUnknown = 'UNKNOWN'
cmsSending = 'SENDING'
cmsSent = 'SENT'
cmsReceived = 'RECEIVED'
cmsRead = 'READ'


# TUserSex
usexUnknown = 'UNKNOWN'
usexMale = 'MALE'
usexFemale = 'FEMALE'


# TBuddyStatus
budUnknown = -1
budNeverBeenFriend = 0
budDeletedFriend = 1
budPendingAuthorization = 2
budFriend = 3


# TOnlineStatus
olsUnknown = 'UNKNOWN'
olsOffline = 'OFFLINE'
olsOnline = 'ONLINE'
olsAway = 'AWAY'
olsNotAvailable = 'NA'
olsDoNotDisturb = 'DND'
olsInvisible = 'INVISIBLE'
olsSkypeOut = 'SkypeOut'
olsSkypeMe = 'SKYPEME'


# TChatLeaveReason
leaUnknown = ''
leaUserNotFound = 'USER_NOT_FOUND'
leaUserIncapable = 'USER_INCAPABLE'
leaAdderNotFriend = 'ADDER_MUST_BE_FRIEND'
leaAddedNotAuthorized = 'ADDED_MUST_BE_AUTHORIZED'
leaAddDeclined = 'ADD_DECLINED'
leaUnsubscribe = 'UNSUBSCRIBE'


# TChatStatus
chsUnknown = 'UNKNOWN'
chsLegacyDialog = 'LEGACY_DIALOG'
chsDialog = 'DIALOG'
chsMultiNeedAccept = 'MULTI_NEED_ACCEPT'
chsMultiSubscribed = 'MULTI_SUBSCRIBED'
chsUnsubscribed = 'UNSUBSCRIBED'


# TVoicemailType
vmtUnknown = 'UNKNOWN'
vmtIncoming = 'INCOMING'
vmtDefaultGreeting = 'DEFAULT_GREETING'
vmtCustomGreeting = 'CUSTOM_GREETING'
vmtOutgoing = 'OUTGOING'


# TVoicemailStatus
vmsUnknown = 'UNKNOWN'
vmsNotDownloaded = 'NOTDOWNLOADED'
vmsDownloading = 'DOWNLOADING'
vmsUnplayed = 'UNPLAYED'
vmsBuffering = 'BUFFERING'
vmsPlaying = 'PLAYING'
vmsPlayed = 'PLAYED'
vmsBlank = 'BLANK'
vmsRecording = 'RECORDING'
vmsRecorded = 'RECORDED'
vmsUploading = 'UPLOADING'
vmsUploaded = 'UPLOADED'
vmsDeleting = 'DELETING'
vmsFailed = 'FAILED'


# TVoicemailFailureReason
vmrUnknown = 'UNKNOWN'
vmrNoError = 'NOERROR'
vmrMiscError = 'MISC_ERROR'
vmrConnectError = 'CONNECT_ERROR'
vmrNoPrivilege = 'NO_VOICEMAIL_PRIVILEGE'
vmrNoVoicemail = 'NO_SUCH_VOICEMAIL'
vmrFileReadError = 'FILE_READ_ERROR'
vmrFileWriteError = 'FILE_WRITE_ERROR'
vmrRecordingError = 'RECORDING_ERROR'
vmrPlaybackError = 'PLAYBACK_ERROR'


# TGroupType
grpUnknown = 'UNKNOWN'
grpCustomGroup = 'CUSTOM_GROUP'
grpAllUsers = 'ALL_USERS'
grpAllFriends = 'ALL_FRIENDS'
grpSkypeFriends = 'SKYPE_FRIENDS'
grpSkypeOutFriends = 'SkypeOut_FRIENDS'
grpOnlineFriends = 'ONLINE_FRIENDS'
grpPendingAuthorizationFriends = 'UNKNOWN_OR_PENDINGAUTH_FRIENDS'
grpRecentlyContactedUsers = 'RECENTLY_CONTACTED_USERS'
grpUsersWaitingMyAuthorization = 'USERS_WAITING_MY_AUTHORIZATION'
grpUsersAuthorizedByMe = 'USERS_AUTHORIZED_BY_ME'
grpUsersBlockedByMe = 'USERS_BLOCKED_BY_ME'
grpUngroupedFriends = 'UNGROUPED_FRIENDS'
grpSharedGroup = 'SHARED_GROUP'
grpProposedSharedGroup = 'PROPOSED_SHARED_GROUP'


# TCallChannelType
cctUnknown = 'UNKNOWN'
cctDatagram = 'DATAGRAM'
cctReliable = 'RELIABLE'


# TApiSecurityContext
apiContextUnknown = 'UNKNOWN'
apiContextVoice = 'VOICE'
apiContextMessaging = 'MESSAGING'
apiContextAccount = 'ACCOUNT'
apiContextContacts = 'CONTACTS'


# TSmsMessageType
smsMessageTypeUnknown = 'UNKNOWN'
smsMessageTypeIncoming = 'INCOMING'
smsMessageTypeOutgoing = 'OUTGOING'
smsMessageTypeCCRequest = 'CONFIRMATION_CODE_REQUEST'
smsMessageTypeCCSubmit = 'CONFRIMATION_CODE_SUBMIT'


# TSmsMessageStatus
smsMessageStatusUnknown = 'UNKNOWN'
smsMessageStatusReceived = 'RECEIVED'
smsMessageStatusRead = 'READ'
smsMessageStatusComposing = 'COMPOSING'
smsMessageStatusSendingToServer = 'SENDING_TO_SERVER'
smsMessageStatusSentToServer = 'SENT_TO_SERVER'
smsMessageStatusDelivered = 'DELIVERED'
smsMessageStatusSomeTargetsFailed = 'SOME_TARGETS_FAILED'
smsMessageStatusFailed = 'FAILED'


# TSmsFailureReason
smsFailureReasonUnknown = 'UNKNOWN'
smsFailureReasonMiscError = 'MISC_ERROR'
smsFailureReasonServerConnectFailed = 'SERVER_CONNECT_FAILED'
smsFailureReasonNoSmsCapability = 'NO_SMS_CAPABILITY'
smsFailureReasonInsufficientFunds = 'INSUFFICIENT_FUNDS'
smsFailureReasonInvalidConfirmationCode = 'INVALID_CONFIRMATION_CODE'
smsFailureReasonUserBlocked = 'USER_BLOCKED'
smsFailureReasonIPBlocked = 'IP_BLOCKED'
smsFailureReasonNodeBlocked = 'NODE_BLOCKED'
smsFailureReasonNoSenderIdCapability = 'NO_SENDERID_CAPABILITY'


# TSmsTargetStatus
smsTargetStatusUnknown = 'UNKNOWN'
smsTargetStatusUndefined = 'TARGET_UNDEFINED'
smsTargetStatusAnalyzing = 'TARGET_ANALYZING'
smsTargetStatusAcceptable = 'TARGET_ACCEPTABLE'
smsTargetStatusNotRoutable = 'TARGET_NOT_ROUTABLE'
smsTargetStatusDeliveryPending = 'TARGET_DELIVERY_PENDING'
smsTargetStatusDeliverySuccessful = 'TARGET_DELIVERY_SUCCESSFUL'
smsTargetStatusDeliveryFailed = 'TARGET_DELIVERY_FAILED'


# TPluginContext
pluginContextUnknown = 'UNKNOWN'
pluginContextChat = 'CHAT'
pluginContextCall = 'CALL'
pluginContextContact = 'CONTACT'
pluginContextMyself = 'MYSELF'
pluginContextTools = 'TOOLS'


# TPluginContactType
pluginContactTypeUnknown = 'UNKNOWN'
pluginContactTypeAll = 'ALL'
pluginContactTypeSkype = 'SKYPE'
pluginContactTypeSkypeOut = 'SKYPEOUT'


# TFileTransferType
fileTransferTypeIncoming = 'INCOMING'
fileTransferTypeOutgoing = 'OUTGOING'


# TFileTransferStatus
fileTransferStatusNew = 'NEW'
fileTransferStatusConnecting = 'CONNECTING'
fileTransferStatusWaitingForAccept = 'WAITING_FOR_ACCEPT'
fileTransferStatusTransferring = 'TRANSFERRING'
fileTransferStatusTransferringOverRelay = 'TRANSFERRING_OVER_RELAY'
fileTransferStatusPaused = 'PAUSED'
fileTransferStatusRemotelyPaused = 'REMOTELY_PAUSED'
fileTransferStatusCancelled = 'CANCELLED'
fileTransferStatusCompleted = 'COMPLETED'
fileTransferStatusFailed = 'FAILED'


# TFileTransferFailureReason
fileTransferFailureReasonSenderNotAuthorized = 'SENDER_NOT_AUTHORIZED'
fileTransferFailureReasonRemotelyCancelled = 'REMOTELY_CANCELLED'
fileTransferFailureReasonFailedRead = 'FAILED_READ'
fileTransferFailureReasonFailedRemoteRead = 'FAILED_REMOTE_READ'
fileTransferFailureReasonFailedWrite = 'FAILED_WRITE'
fileTransferFailureReasonFailedRemoteWrite = 'FAILED_REMOTE_WRITE'
fileTransferFailureReasonRemoteDoesNotSupportFT = 'REMOTE_DOES_NOT_SUPPORT_FT'
fileTransferFailureReasonRemoteOfflineTooLong = 'REMOTE_OFFLINE_TOO_LONG'
