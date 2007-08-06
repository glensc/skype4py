'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from API import *
from errors import ISkypeError
from enums import *
from utils import *
from conversion import *
from client import *
from user import *
from call import *
from profile import *
from settings import *
from chat import *
from application import *
from voicemail import *
from sms import *
from filetransfer import *
import time


# Skype4Py version
_version_ = '0.4.0.3'


# early version, enable leak debugging
import gc
gc.set_debug(gc.DEBUG_LEAK)


ISkypeEventHandling = EventHandling([
    'Command',
    'Reply',
    'Error_',
    'AttachmentStatus',
    'ConnectionStatus',
    'UserStatus',
    'OnlineStatus',
    'CallStatus',
    'CallHistory',
    'Mute',
    'MessageStatus',
    'MessageHistory',
    'AutoAway',
    'CallDtmfReceived',
    'VoicemailStatus',
    'ApplicationConnecting',
    'ApplicationStreams',
    'ApplicationDatagram',
    'ApplicationSending',
    'ApplicationReceiving',
    'ContactsFocused',
    'GroupVisible',
    'GroupExpanded',
    'GroupUsers',
    'GroupDeleted',
    'UserMood',
    'SmsMessageStatusChanged',
    'SmsTargetStatusChanged',
    'CallInputStatusChanged',
    'AsyncSearchUsersFinished',
    'CallSeenStatusChanged',
    'PluginEventClicked',
    'PluginMenuItemClicked',
    'WallpaperChanged',
    'FileTransferStatusChanged'])


class ISkype(ISkypeEventHandling):
    def __init__(self, Events=None):
        ISkypeEventHandling.__init__(self)

        if Events:
            self._RegisterEvents('default', Events)

        self._API = ISkypeAPI(self._Handler)
        self._Cache = True
        self.ResetCache()

        self._Timeout = 30000
        self._AttachmentStatus = apiAttachUnknown

        self._Convert = IConversion(self)
        self._Client = IClient(self)
        self._Settings = ISettings(self)
        self._Profile = IProfile(self)

    def __del__(self):
        self.Close()

    def _Handler(self, mode, arg):
        # low-level API callback
        if mode == 'rece_api':
            a, b = chop(arg)
            ObjectType = None
            # if..elif handling cache and most event handlers
            if a in ['CALL', 'USER', 'GROUP', 'CHAT', 'CHATMESSAGE', 'CHATMEMBER', 'VOICEMAIL', 'APPLICATION', 'SMS', 'FILETRANSFER']:
                ObjectType, ObjectId, PropName, Value = [a] + chop(b, 2)
                if self._Cache:
                    self._CacheDict[str(ObjectType), str(ObjectId), str(PropName)] = Value
                if ObjectType == 'USER':
                    o = IUser(ObjectId, self)
                    if PropName == 'ONLINESTATUS':
                        self._CallEventHandler('OnlineStatus', o, Value)
                    elif PropName == 'MOOD_TEXT' or PropName == 'RICH_MOOD_TEXT':
                        self._CallEventHandler('UserMood', o, Value)
                if ObjectType == 'CALL':
                    o = ICall(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('CallStatus', o, Value)
                    elif PropName == 'SEEN':
                        self._CallEventHandler('CallSeenStatusChanged', o, Value == 'TRUE')
                    elif PropName == 'INPUT':
                        self._CallEventHandler('CallInputStatusChanged', o, Value.startswith('SOUNDCARD='))
                if ObjectType == 'CHATMESSAGE':
                    o = IChatMessage(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('MessageStatus', o, Value)
                if ObjectType == 'APPLICATION':
                    o = IApplication(ObjectId, self)
                    if PropName == 'CONNECTING':
                        self._CallEventHandler('ApplicationConnecting', o, map(lambda x: IUser(x, self), esplit(Value)))
                    elif PropName == 'STREAMS':
                        self._CallEventHandler('ApplicationStreams', o, map(lambda x: IApplicationStream(x, app), esplit(Value)))
                    elif PropName == 'DATAGRAM':
                        handle, text = chop(Value)
                        self._CallEventHandler('ApplicationDatagram', o, IApplicationStream(handle, app), text)
                    elif PropName == 'SENDING':
                        self._CallEventHandler('ApplicationSending', o, map(lambda x: IApplicationStream(x.split('=')[0], app), esplit(Value)))
                    elif PropName == 'RECEIVED':
                        self._CallEventHandler('ApplicationReceiving', o, map(lambda x: IApplicationStream(x.split('=')[0], app), esplit(Value)))
                elif ObjectType == 'GROUP':
                    o = IGroup(ObjectId, self)
                    if PropName == 'VISIBLE':
                        self._CallEventHandler('GroupVisible', o, Value == 'TRUE')
                    elif PropName == 'EXPANDED':
                        self._CallEventHandler('GroupExpanded', o, Value == 'TRUE')
                    elif PropName == 'USERS':
                        self._CallEventHandler('GroupUsers', o, map(lambda x: IUser(x, self), esplit(Value, ', ')))
                elif ObjectType == 'SMS':
                    o = ISmsMessage(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('SmsMessageStatusChanged', o, Value)
                    elif PropName == 'TARGET_STATUSES':
                        for t in esplit(Value, ', '):
                            number, status = t.split('=')
                            self._CallEventHandler('SmsTargetStatusChanged', ISmsTarget(number, o), status)
                elif ObjectType == 'FILETRANSFER':
                    o = IFileTransfer(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('FileTransferStatusChanged', o, Value)
            elif a in ['PROFILE', 'PRIVILEGE']:
                ObjectType, ObjectId, PropName, Value = [a, ''] + chop(b)
                if self._Cache:
                    self._CacheDict[str(ObjectType), str(ObjectId), str(PropName)] = Value
            elif a in ['CURRENTUSERHANDLE', 'USERSTATUS', 'CONNSTATUS', 'PREDICTIVE_DIALER_COUNTRY', 'SILENT_MODE', 'AUDIO_IN', 'AUDIO_OUT', 'RINGER', 'MUTE']:
                ObjectType, ObjectId, PropName, Value = [a, '', '', b]
                if self._Cache:
                    self._CacheDict[str(ObjectType), str(ObjectId), str(PropName)] = Value
                if ObjectType == 'MUTE':
                    self._CallEventHandler('Mute', Value == 'TRUE')
                elif ObjectType == 'CONNSTATUS':
                    self._CallEventHandler('ConnectionStatus', Value)
                elif ObjectType == 'USERSTATUS':
                    self._CallEventHandler('UserStatus', Value)
            elif a == 'CALLHISTORYCHANGED':
                self._CallEventHandler('CallHistory')
            elif a == 'IMHISTORYCHANGED':
                self._CallEventHandler('MessageHistory', u'')
            elif a == 'CONTACTS':
                PropName, Value = chop(b)
                if PropName == 'FOCUSED':
                    self._CallEventHandler('ContactsFocused', Value)
            elif a == 'DELETED':
                PropName, Value = chop(b)
                if PropName == 'GROUP':
                    self._CallEventHandler('GroupDeleted', int(Value))
            elif a == 'EVENT':
                ObjectId, PropName, Value = chop(b, 2)
                if PropName == 'CLICKED':
                    self._CallEventHandler('PluginEventClicked', IPluginEvent(ObjectId, self))
            elif a == 'MENU_ITEM':
                ObjectId, PropName, Value = chop(b, 2)
                if PropName == 'CLICKED':
                    self._CallEventHandler('PluginMenuItemClicked', IPluginMenuItem(ObjectId, self))
            elif a == 'WALLPAPER':
                self._CallEventHandler('WallpaperChanged', b)
        elif mode == 'rece':
            self._CallEventHandler('Reply', arg)
        elif mode == 'send':
            self._CallEventHandler('Command', arg)
        elif mode == 'attach':
            if arg != self._AttachmentStatus:
                self._AttachmentStatus = arg
                self._CallEventHandler('AttachmentStatus', self._AttachmentStatus)
                if self._AttachmentStatus == 'REFUSED':
                    raise ISkypeAPIError('Skype connection refused')

    def _DoCommand(self, com, reply=''):
        command = ICommand(-1, com, reply, True, self.Timeout)
        self.SendCommand(command)
        a, b = chop(command.Reply)
        if a == 'ERROR':
            errnum, errstr = chop(b)
            self._CallEventHandler('Error_', command, int(errnum), errstr)
            raise ISkypeError(int(errnum), errstr)
        if not command.Reply.startswith(command.Expected):
            raise ISkypeError(0, 'Unexpected reply from Skype')
        return command.Reply

    def _Alter(self, ObjectType, ObjectId, AlterName, Args=None, Reply=None):
        com = 'ALTER %s %s %s' % (str(ObjectType).upper(), unicode(ObjectId), str(AlterName).upper())
        if Reply == None:
            Reply = com
        if Args != None:
            com = '%s %s' % (com, Args)
        reply = self._DoCommand(com, Reply)
        arg = com.split()
        while arg:
            try:
                a, b = chop(reply)
            except ValueError:
                break
            if a != arg[0]:
                break
            del arg[0]
            reply = b
        return reply

    def _Search(self, ObjectType, Args=None):
        com = 'SEARCH %s' % ObjectType
        if Args != None:
            com = '%s %s' % (com, Args)
        return esplit(chop(self._DoCommand(com))[-1], ', ')

    def Close(self):
        self._API.Close()

    def SearchForUsers(self, Target):
        return map(lambda x: IUser(x, self), self._Search('USERS', Target))

    def AsyncSearchUsers(self, Target):
        command = ICommand(-1, 'SEARCH USERS %s' % Target, 'USERS', False, self.Timeout)
        self._RegisterEventHandler('Reply', 'AsyncSearchUsers', self._AsyncSearchUsersEnd)
        self.SendCommand(command)
        return command.Id

    def _AsyncSearchUsersEnd(self, command):
        if command.Command.startswith('SEARCH USERS'):
            self._CallEventHandler('AsyncSearchUsersFinished', command.Id, map(lambda x: IUser(x, self), esplit(chop(command.Reply)[-1], ', ')))
            self._UnregisterEventHandler('Reply', 'AsyncSearchUsers')

    def Attach(self, Protocol=5, Wait=True):
        self._API.Protocol = Protocol
        self._API.Attach(self.Timeout)

    def PlaceCall(self, Target, Target2='', Target3='', Target4=''):
        com = 'CALL %s' % Target
        if Target2:
            com = '%s, %s' % (com, Target2)
        if Target3:
            com = '%s, %s' % (com, Target3)
        if Target4:
            com = '%s, %s' % (com, Target4)
        return ICall(chop(self._DoCommand(com), 2)[1], self)

    def SendMessage(self, Username, Text):
        return self.CreateChatWith(Username).SendMessage(Text)

    def SendCommand(self, Command):
        if not self._API.SendCommand(Command):
            raise ISkypeError(0, 'Skype does not respond')

    def ChangeUserStatus(self, newVal):
        self.CurrentUserStatus = newVal
        while self.CurrentUser.OnlineStatus != newVal:
            time.sleep(0.01)

    def CreateChatWith(self, Username):
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % Username), 2)[1], self)

    def CreateChatMultiple(self, pMembers):
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % ', '.join(map(lambda x: x.Handle, pMembers))), 2)[1], self)

    def SendVoicemail(self, Username):
        # TODO
        raise ISkypeError(0, 'Not implemented')

    def ClearChatHistory(self):
        self._DoCommand('CLEAR CHARHISTORY')

    def ClearVoicemailHistory(self):
        self._DoCommand('CLEAR VOICEMAILHISTORY')

    def ClearCallHistory(self, Username='ALL', Type=chsAllCalls):
        self._DoCommand('CLEAR CALLHISTORY %s %s' % (str(Type), Username))

    def _SetCache(self, Cache):
        self._Cache = Cache
        if not Cache:
            self.ResetCache()

    def ResetCache(self):
        self._CacheDict = {}

    def CreateGroup(self, GroupName):
        groups1 = self._Search('GROUPS', 'CUSTOM')
        self._DoCommand('CREATE GROUP %s' % GroupName)
        groups2 = self._Search('GROUPS', 'CUSTOM')
        for g in groups2:
            if g not in groups1:
                break
        else:
            raise SkypeError(0, 'Group creating failed')
        return IGroup(g, self)

    def DeleteGroup(self, GroupId):
        self._DoCommand('DELETE GROUP %s' % GroupId)

    def CreateSms(self, MessageType, TargetNumbers):
        return ISmsMessage(chop(self._DoCommand('CREATE SMS %s %s' % (TSmsMessageType(MessageType), TargetNumbers)), 2)[1], self)

    def SendSms(self, TargetNumbers, MessageText, ReplyToNumber=''):
        sms = ISmsMessage(chop(self._DoCommand('CREATE SMS OUTGOING %s' % TargetNumbers), 2)[1], self)
        sms.Body = MessageText
        sms.ReplyToNumber = ReplyToNumber
        sms.Send()
        return sms

    def _Property(self, ObjectType, ObjectId, PropName, Set=None, Cache=True):
        h = (str(ObjectType).upper(), str(ObjectId), str(PropName).upper())
        arg = ('%s %s %s' % h).split()
        while '' in arg:
            arg.remove('')
        if Set == None: # Get
            if Cache and h in self._CacheDict:
                return self._CacheDict[h]
            Value = self._DoCommand('GET %s' % ' '.join(arg))
            while arg:
                try:
                    a, b = chop(Value)
                except ValueError:
                    break
                if a != arg[0]:
                    break
                del arg[0]
                Value = b
            if Cache and self._Cache:
                self._CacheDict[h] = Value
            return Value
        else: # Set
            Value = unicode(Set)
            self._DoCommand('SET %s %s' % (' '.join(arg), Value))
            if Cache and self._Cache:
                self._CacheDict[h] = Value

    def Property(self, ObjectType, ObjectId, PropName, Set=None):
        return self._Property(ObjectType, ObjectId, PropName, Set)

    def Variable(self, Name, Set=None):
        return self._Property(Name, '', '', Set)

    def Privilege(self, Name):
        return self._Property('PRIVILEGE', '', Name) == 'TRUE'

    def Calls(self, Target=''):
        return map(lambda x: ICall(x, self), self._Search('CALLS', Target))

    def Messages(self, Target=''):
        return map(lambda x: IChatMessage(x, self), self._Search('CHATMESSAGES', Target))

    def User(self, Username=''):
        o = IUser(Username, self)
        o.OnlineStatus
        return o

    def Message(self, Id=0):
        o = IChatMessage(Id, self)
        o.Status
        return o

    def Call(self, Id=0):
        o = ICall(Id, self)
        o.Status
        return o

    def Chat(self, Name=''):
        o = IChat(Name, self)
        o.Status
        return o

    def Conference(self, Id=0):
        o = IConference(Id, self)
        if Id <= 0 or o.Calls == []:
            raise ISkypeError(0, 'Unknown conference')
        return o

    def Profile(self, Property, Set=None):
        return self._Property('PROFILE', '', Property, Set)

    def Application(self, Name):
        return IApplication(Name, self)

    def Greeting(self, Username=''):
        for v in self.Voicemails:
            if Username and v.PartnerHandle != Username:
                continue
            if v.Type in [vmtDefaultGreeting, vmtCustomGreeting]:
                return v

    def Command(self, Id, command, Reply='', Block=False, Timeout=30000):
        return ICommand(Id, command, Reply, Block, Timeout)

    def Voicemail(self, Id):
        o = IVoicemail(Id, self)
        o.Type
        return o

    def ApiSecurityContextEnabled(self, Context):
        raise SkypeError(0, 'Not supported')

    def EnableApiSecurityContext(self, Context):
        raise SkypeError(0, 'Not supported')

    def _SetTimeout(self, Timeout):
        self._Timeout = Timeout

    def _SetProtocol(self, Protocol):
        self._API.Protocol = Protocol

    def _SetFriendlyName(self, FriendlyName):
        self._API.SetFriendlyName(FriendlyName)

    def _GetConferences(self):
        confs = []
        for c in self.Calls():
            cid = c.ConferenceId
            if cid > 0 and cid not in map(lambda x: x.Id, confs):
                confs.append(IConference(cid, self))
        return confs

    # Custom, ISettings.AutoAway should be based on this?
    def ResetIdleTimer(self):
        self._DoCommand('RESETIDLETIMER')

    Timeout = property(lambda self: self._Timeout, _SetTimeout)
    Protocol = property(lambda self: self._API.Protocol, _SetProtocol)
    CurrentUserHandle = property(lambda self: self.Variable('CURRENTUSERHANDLE'))
    CurrentUserStatus = property(lambda self: self.Variable('USERSTATUS'),
                                 lambda self, value: self.Variable('USERSTATUS', str(value)))
    ConnectionStatus = property(lambda self: self.Variable('CONNSTATUS'))
    Mute = property(lambda self: self.Variable('MUTE') == 'ON',
                    lambda self, value: self.Variable('MUTE', 'ON' if value else 'OFF'))

    Version = property(lambda self: self.Variable('SKYPEVERSION'))
    CurrentUser = property(lambda self: IUser(self.CurrentUserHandle, self))
    Convert = property(lambda self: self._Convert)
    Friends = property(lambda self: map(lambda x: IUser(x, self), self._Search('FRIENDS')))

    Client = property(lambda self: self._Client)
    AttachmentStatus = property(lambda self: self._AttachmentStatus)

    CurrentUserProfile = property(lambda self: self._Profile)

    Groups = property(lambda self: map(lambda x: IGroup(x, self), self._Search('GROUPS', 'ALL')))
    CustomGroups = property(lambda self: map(lambda x: IGroup(x, self), self._Search('GROUPS', 'CUSTOM')))
    HardwiredGroups = property(lambda self: map(lambda x: IGroup(x, self), self._Search('GROUPS', 'HARDWIRED')))

    ActiveCalls = property(lambda self: map(lambda x: ICall(x, self), self._Search('ACTIVECALLS')))
    MissedCalls = property(lambda self: map(lambda x: ICall(x, self), self._Search('MISSEDCALLS')))

    FriendlyName = property(fset=_SetFriendlyName)
    ApiWrapperVersion = property(lambda self: GetVersion())
    SilentMode = property(lambda self: self.Variable('SILENT_MODE') == 'ON',
                          lambda self, value: self.SendCommand(ICommand(-1, 'SET SILENT_MODE %s' % 'ON' if value else 'OFF')))
    Settings = property(lambda self: self._Settings)

    UsersWaitingAuthorization = property(lambda self: map(lambda x: IUser(x, self), self._Search('USERSWAITINGMYAUTHORIZATION')))
    Cache = property(lambda self: self._Cache, _SetCache)
    CommandId = property(lambda self: True)

    Chats = property(lambda self: map(lambda x: IChat(x, self), self._Search('CHATS')))
    ActiveChats = property(lambda self: map(lambda x: IChat(x, self), self._Search('ACTIVECHATS')))
    MissedChats = property(lambda self: map(lambda x: IChat(x, self), self._Search('MISSEDCHATS')))
    RecentChats = property(lambda self: map(lambda x: IChat(x, self), self._Search('RECENTCHATS')))
    BookmarkedChats = property(lambda self: map(lambda x: IChat(x, self), self._Search('BOOKMARKEDCHATS')))
    MissedMessages = property(lambda self: map(lambda x: IChatMessage(x, self), self._Search('MISSEDCHATMESSAGES')))

    Voicemails = property(lambda self: map(lambda x: IVoicemail(x, self), self._Search('VOICEMAILS')))
    MissedVoicemails = property(lambda self: map(lambda x: IVoicemail(x, self), self._Search('MISSEDVOICEMAILS')))

    Conferences = property(_GetConferences)
    Smss = property(lambda self: map(lambda x: ISmsMessage(x, self), self._Search('SMSS')))
    MissedSmss = property(lambda self: map(lambda x: ISmsMessage(x, self), self._Search('MISSEDSMSS')))
    FileTransfers = property(lambda self: map(lambda x: IFileTransfer(x, self), self._Search('FILETRANSFERS')))
    ActiveFileTransfers = property(lambda self: map(lambda x: IFileTransfer(x, self), self._Search('ACTIVEFILETRANSFERS')))

    # Custom
    FocusedContact = property(lambda self: chop(self.Variable('CONTACTS_FOCUSED'), 2)[-1])


def GetVersion():
    return unicode(_version_)
