'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *


class TAttachmentStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN', -1),
               ('Success', 'SUCCESS', 0),
               ('PendingAuthorization', 'PENDING', 1),
               ('Refused', 'REFUSED', 2),
               ('NotAvailable', 'NOT_AVAILABLE', 3),
               ('Available', 'AVAILABLE', 0x8001)])


class TConnectionStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Offline', 'OFFLINE'),
               ('Connecting', 'CONNECTING'),
               ('Pausing', 'PAUSING'),
               ('Online', 'ONLINE')])


class TUserStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Offline', 'OFFLINE'),
               ('Online', 'ONLINE'),
               ('Away', 'AWAY'),
               ('NotAvailable', 'NA'),
               ('DoNotDisturb', 'DND'),
               ('Invisible', 'INVISIBLE'),
               ('LoggedOut', 'LOGGEDOUT'),
               ('SkypeMe', 'SKYPEME')])


class TCallFailureReason(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN', 0),
               ('MiscError', 'MISCERROR', 1),
               ('UserDoesNotExist', 'USER_DOES_NOT_EXIST', 2),
               ('UserIsOffline', 'USER_IS_OFFLINE', 3),
               ('NoProxyFound', 'NO_PROXY_FOUND', 4),
               ('SessionTerminated', 'SESSION_TERMINATED', 5),
               ('NoCommonCodec', 'NO_COMMON_CODEC', 6),
               ('SoundIOError', 'SOUNDIO_ERROR', 7),
               ('RemoteDeviceError', 'REMOTE_DEVICE_ERROR', 8),
               ('BlockedByRecipient', 'BLOCKED_BY_RECIPIENT', 9),
               ('RecipientNotFriend', 'RECIPIENT_NOT_FRIEND', 10),
               ('NotAuthorizedByRecipient', 'NOT_AUTHORIZED_BY_RECIPIENT', 11),
               ('SoundRecordingError', 'SOUND_RECORDING_ERROR', 12)])


class TCallStatus(Enum):
    _enum_ = ([('Unknown', 'NOT_AVAILABLE'),
               ('Unplaced', 'UNPLACED'),
               ('Routing', 'ROUTING'),
               ('EarlyMedia', 'EARLYMEDIA'),
               ('Failed', 'FAILED'),
               ('Ringing', 'RINGING'),
               ('InProgress', 'INPROGRESS'),
               ('OnHold', 'ONHOLD'),
               ('Finished', 'FINISHED'),
               ('Missed', 'MISSED'),
               ('Refused', 'REFUSED'),
               ('Busy', 'BUSY'),
               ('Cancelled', 'CANCELLED'),
               ('LocalHold', 'REDIAL_PENDING'),
               ('RemoteHold', 'WAITING_REDIAL_COMMAND'),
               ('VoicemailBufferingGreeting', 'VM_BUFFERING_GREETING'),
               ('VoicemailPlayingGreeting', 'VM_PLAYING_GREETING'),
               ('VoicemailRecording', 'VM_RECORDING'),
               ('VoicemailUploading', 'VM_UPLOADING'),
               ('VoicemailSent', 'VM_SENT'),
               ('VoicemailCancelled', 'VM_CANCELLED'),
               ('VoicemailFailed', 'VM_FAILED'),
               ('Transferring', 'TRANSFERRING'),
               ('Transferred', 'TRANSFERRED')])


class TCallType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('IncomingPSTN', 'INCOMING_PSTN'),
               ('OutgoingPSTN', 'OUTGOING_PSTN'),
               ('IncomingP2P', 'INCOMING_P2P'),
               ('OutgoingP2P', 'OUTGOING_P2P')])


class TCallHistory(Enum):
    _enum_ = ([('AllCalls', 'ALL'),
               ('MissedCalls', 'MISSED'),
               ('IncomingCalls', 'INCOMING'),
               ('OutgoingCalls', 'OUTGOING')])


class TCallVideoStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('None', 'VIDEO_NONE'),
               ('SendEnabled', 'VIDEO_SEND_ENABLED'),
               ('ReceiveEnabled', 'VIDEO_RECV_ENABLED'),
               ('BothEnabled', 'VIDEO_BOTH_ENABLED')])


class TCallVideoSendStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('NotAvailable', 'NOT_AVAILABLE'),
               ('Available', 'AVAILABLE'),
               ('Starting', 'STARTING'),
               ('Rejected', 'REJECTED'),
               ('Running', 'RUNNING'),
               ('Stopping', 'STOPPING'),
               ('Paused', 'PAUSED')])


class TCallIoDeviceType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Soundcard', 'SOUNDCARD'),
               ('Port', 'PORT'),
               ('File', 'FILE')])


class TChatMessageType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('CreatedChatWith', 'CREATEDCHATWITH'),
               ('SawMembers', 'SAWMEMBERS'),
               ('AddedMembers', 'ADDEDMEMBERS'),
               ('SetTopic', 'SETTOPIC'),
               ('Said', 'SAID'),
               ('Left', 'LEFT'),
               ('Emoted', 'EMOTED'),
               ('PostedContacts', 'POSTEDCONTACTS'),
               ('GapInChat', 'GAP_IN_CHAT'),
               ('SetRole', 'SETROLE'),
               ('Kicked', 'KICKED'),
               ('KickBanned', 'KICKBANNED'),
               ('SetOptions', 'SETOPTIONS'),
               ('SetPicture', 'SETPICTURE'),
               ('SetGuidelines', 'SETGUIDELINES'),
               ('JoinedAsApplicant', 'JOINEDASAPPLICANT')])


class TChatMessageStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Sending', 'SENDING'),
               ('Sent', 'SENT'),
               ('Received', 'RECEIVED'),
               ('Read', 'READ')])


class TUserSex(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Male', 'MALE'),
               ('Female', 'FEMALE')])


class TBuddyStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('NeverBeenFriend', 'NEVER_BEEN_FRIEND', 0),
               ('DeletedFriend', 'DELETED_FRIEND', 1),
               ('PendingAuthorization', 'PENDING', 2),
               ('Friend', 'FRIEND', 3)])


class TOnlineStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Offline', 'OFFLINE'),
               ('Online', 'ONLINE'),
               ('Away', 'AWAY'),
               ('NotAvailable', 'NA'),
               ('DoNotDisturb', 'DND'),
               ('Invisible', 'INVISIBLE'),
               ('SkypeOut', 'SkypeOut'),
               ('SkypeMe', 'SKYPEME')])


class TChatLeaveReason(Enum):
    _enum_ = ([('Unknown', ''),
               ('UserNotFound', 'USER_NOT_FOUND'),
               ('UserIncapable', 'USER_INCAPABLE'),
               ('AdderNotFriend', 'ADDER_MUST_BE_FRIEND'),
               ('AddedNotAuthorized', 'ADDED_MUST_BE_AUTHORIZED'),
               ('AddDeclined', 'ADD_DECLINED'),
               ('Unsubscribe', 'UNSUBSCRIBE')])


class TChatStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('LegacyDialog', 'LEGACY_DIALOG'),
               ('Dialog', 'DIALOG'),
               ('MultiNeedAccept', 'MULTI_NEED_ACCEPT'),
               ('MultiSubscribed', 'MULTI_SUBSCRIBED'),
               ('Unsubscribed', 'UNSUBSCRIBED')])


class TVoicemailType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Incoming', 'INCOMING'),
               ('DefaultGreeting', 'DEFAULT_GREETING'),
               ('CustomGreeting', 'CUSTOM_GREETING'),
               ('Outgoing', 'OUTGOING')])


class TVoicemailStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('NotDownloaded', 'NOTDOWNLOADED'),
               ('Downloading', 'DOWNLOADING'),
               ('Unplayed', 'UNPLAYED'),
               ('Buffering', 'BUFFERING'),
               ('Playing', 'PLAYING'),
               ('Played', 'PLAYED'),
               ('Blank', 'BLANK'),
               ('Recording', 'RECORDING'),
               ('Recorded', 'RECORDED'),
               ('Uploading', 'UPLOADING'),
               ('Uploaded', 'UPLOADED'),
               ('Deleting', 'DELETING'),
               ('Failed', 'FAILED')])


class TVoicemailFailureReason(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('NoError', 'NOERROR'),
               ('MiscError', 'MISC_ERROR'),
               ('ConnectError', 'CONNECT_ERROR'),
               ('NoPrivilege', 'NO_VOICEMAIL_PRIVILEGE'),
               ('NoVoicemail', 'NO_SUCH_VOICEMAIL'),
               ('FileReadError', 'FILE_READ_ERROR'),
               ('FileWriteError', 'FILE_WRITE_ERROR'),
               ('RecordingError', 'RECORDING_ERROR'),
               ('PlaybackError', 'PLAYBACK_ERROR')])


class TGroupType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('CustomGroup', 'CUSTOM_GROUP'),
               ('AllUsers', 'ALL_USERS'),
               ('AllFriends', 'ALL_FRIENDS'),
               ('SkypeFriends', 'SKYPE_FRIENDS'),
               ('SkypeOutFriends', 'SkypeOut_FRIENDS'),
               ('OnlineFriends', 'ONLINE_FRIENDS'),
               ('PendingAuthorizationFriends', 'UNKNOWN_OR_PENDINGAUTH_FRIENDS'),
               ('RecentlyContactedUsers', 'RECENTLY_CONTACTED_USERS'),
               ('UsersWaitingMyAuthorization', 'USERS_WAITING_MY_AUTHORIZATION'),
               ('UsersAuthorizedByMe', 'USERS_AUTHORIZED_BY_ME'),
               ('UsersBlockedByMe', 'USERS_BLOCKED_BY_ME'),
               ('UngroupedFriends', 'UNGROUPED_FRIENDS'),
               ('SharedGroup', 'SHARED_GROUP'),
               ('ProposedSharedGroup', 'PROPOSED_SHARED_GROUP')])


class TCallChannelType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Datagram', 'DATAGRAM'),
               ('Reliable', 'RELIABLE')])


class TApiSecurityContext(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Voice', 'VOICE'),
               ('Messaging', 'MESSAGING'),
               ('Account', 'ACCOUNT'),
               ('Contacts', 'CONTACTS')])


class TSmsMessageType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Incoming', 'INCOMING'),
               ('Outgoing', 'OUTGOING'),
               ('CCRequest', 'CONFIRMATION_CODE_REQUEST'),
               ('CCSubmit', 'CONFRIMATION_CODE_SUBMIT')])


class TSmsMessageStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Received', 'RECEIVED'),
               ('Read', 'READ'),
               ('Composing', 'COMPOSING'),
               ('SendingToServer', 'SENDING_TO_SERVER'),
               ('SentToServer', 'SENT_TO_SERVER'),
               ('Delivered', 'DELIVERED'),
               ('SomeTargetsFailed', 'SOME_TARGETS_FAILED'),
               ('Failed', 'FAILED')])


class TSmsFailureReason(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('MiscError', 'MISC_ERROR'),
               ('ServerConnectFailed', 'SERVER_CONNECT_FAILED'),
               ('NoSmsCapability', 'NO_SMS_CAPABILITY'),
               ('InsufficientFunds', 'INSUFFICIENT_FUNDS'),
               ('InvalidConfirmationCode', 'INVALID_CONFIRMATION_CODE'),
               ('UserBlocked', 'USER_BLOCKED'),
               ('IPBlocked', 'IP_BLOCKED'),
               ('NodeBlocked', 'NODE_BLOCKED'),
               ('NoSenderIdCapability', 'NO_SENDERID_CAPABILITY')])


class TSmsTargetStatus(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Undefined', 'TARGET_UNDEFINED'),
               ('Analyzing', 'TARGET_ANALYZING'),
               ('Acceptable', 'TARGET_ACCEPTABLE'),
               ('NotRoutable', 'TARGET_NOT_ROUTABLE'),
               ('DeliveryPending', 'TARGET_DELIVERY_PENDING'),
               ('DeliverySuccessful', 'TARGET_DELIVERY_SUCCESSFUL'),
               ('DeliveryFailed', 'TARGET_DELIVERY_FAILED')])


class TPluginContext(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('Chat', 'CHAT'),
               ('Call', 'CALL'),
               ('Contact', 'CONTACT'),
               ('Myself', 'MYSELF'),
               ('Tools', 'TOOLS')])


class TPluginContactType(Enum):
    _enum_ = ([('Unknown', 'UNKNOWN'),
               ('All', 'ALL'),
               ('Skype', 'SKYPE'),
               ('SkypeOut', 'SKYPEOUT')])


class TFileTransferType(Enum):
    _enum_ = ([('Incoming', 'INCOMING', 0),
               ('Outgoing', 'OUTGOING', 1)])


class TFileTransferStatus(Enum):
    _enum_ = ([('New', 'NEW'),
               ('Connecting', 'CONNECTING'),
               ('WaitingForAccept', 'WAITING_FOR_ACCEPT'),
               ('Transferring', 'TRANSFERRING'),
               ('TransferringOverRelay', 'TRANSFERRING_OVER_RELAY'),
               ('Paused', 'PAUSED'),
               ('RemotelyPaused', 'REMOTELY_PAUSED'),
               ('Cancelled', 'CANCELLED'),
               ('Completed', 'COMPLETED'),
               ('Failed', 'FAILED')])


class TFileTransferFailureReason(Enum):
    _enum_ = ([('SenderNotAuthorized', 'SENDER_NOT_AUTHORIZED'),
               ('RemotelyCancelled', 'REMOTELY_CANCELLED'),
               ('FailedRead', 'FAILED_READ'),
               ('FailedRemoteRead', 'FAILED_REMOTE_READ'),
               ('FailedWrite', 'FAILED_WRITE'),
               ('FailedRemoteWrite', 'FAILED_REMOTE_WRITE'),
               ('RemoteDoesNotSupportFT', 'REMOTE_DOES_NOT_SUPPORT_FT'),
               ('RemoteOfflineTooLong', 'REMOTE_OFFLINE_TOO_LONG')])
