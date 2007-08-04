
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
import time


# Skype4Py version
_version_ = '0.4.0.0'


class ISkypeEvents(object):
    def Command(self, Command):
        print '<CmdSend> ' + Command.Command

    def Reply(self, Command):
        print '<CmdRece> ' + Command.Reply

    def Error_(self, pCommand, Number, Description):
        pass

    def AttachmentStatus(self, Status):
        pass

    def ConnectionStatus(self, Status):
        pass

    def UserStatus(self, Status):
        pass

    def OnlineStatus(self, pUser, Status):
        pass

    def CallStatus(self, pCall, Status):
        pass

    def CallHistory(self):
        pass

    def Mute(self, Mute):
        pass

    def MessageStatus(self, pMessage, Status):
        pass

    def MessageHistory(self, Username):
        pass

    def AutoAway(self, Automatic):
        pass

    def CallDtmfReceived(self, pCall, Code):
        pass

    def VoicemailStatus(self, pMail, Status):
        pass

    def ApplicationConnecting(self, pApp, pUsers):
        pass

    def ApplicationStreams(self, pApp, pStreams):
        pass

    def ApplicationDatagram(self, pApp, pStream, Text):
        pass

    def ApplicationSending(self, pApp, pStreams):
        pass

    def ApplicationReceiving(self, pApp, pStreams):
        pass

    def ContactsFocused(self, Username):
        pass

    def GroupVisible(self, pGroup, Visible):
        pass

    def GroupExpanded(self, pGroup, Expanded):
        pass

    def GroupUsers(self, pGroup, pUsers):
        pass

    def GroupDeleted(self, GroupId):
        pass

    def UserMood(self, pUser, MoodText):
        pass

    def SmsMessageStatusChanged(self, pMessage, Status):
        pass

    def SmsTargetStatusChanged(self, pTarget, Status):
        pass

    def CallInputStatusChanged(self, pCall, Status):
        pass

    def AsyncSearchUsersFinished(self, Cookie, pUsers):
        pass

    def CallSeenStatusChanged(self, pCall, Status):
        pass

    def PluginEventClicked(self, pEvent):
        pass

    def PluginMenuItemClicked(self, pMenuItem, pUsers, PluginContext, ContextId):
        pass

    def WallpaperChanged(self, Path):
        pass

    def FileTransferStatusChanged(self, pTransfer, Status):
        pass


ISkypeEventHandling = EventHandling(dir(ISkypeEvents))


class ISkype(ISkypeEventHandling):
    def __init__(self, Events=ISkypeEvents):
        ISkypeEventHandling.__init__(self)
        self._RegisterEventsClass(Events)

        self._API = ISkypeAPI(self._Handler)
        self._Cache = True
        self.ResetCache()

        self._Timeout = 30000
        self._AttachmentStatus = TAttachmentStatus.apiAttachUnknown

        self._Convert = IConversion(self)
        self._Client = IClient(self)
        self._Settings = ISettings(self)
        self._Profile = IProfile(self)

    def __del__(self):
        self.Close()

    def _Handler(self, mode, arg):
        if mode == 'rece_api':
            print '<ApiRece> ' + arg.encode('latin-1', 'replace')
            a, b = chop(arg)
            ObjectType = None
            if a == 'ERROR':
                errnum, errstr = chop(b)
                self._CallEventHandler('Error_', None, int(errnum), errstr)
                raise ISkypeError(int(errnum), errstr)
            elif a in ['CALL', 'USER', 'GROUP', 'CHAT', 'CHATMESSAGE', 'CHATMEMBER', 'VOICEMAIL', 'APPLICATION', 'SMS', 'FILETRANSFER']:
                ObjectType, ObjectId, PropName, Value = [a] + chop(b, 2)
                if self._Cache:
                    self._CacheDict[str(ObjectType), unicode(ObjectId), str(PropName)] = Value
                if ObjectType == 'USER':
                    usr = IUser(ObjectId, self)
                    if PropName == 'ONLINESTATUS':
                        self._CallEventHandler('OnlineStatus', usr, TOnlineStatus(Value))
                    elif PropName == 'MOOD_TEXT':
                        self._CallEventHandler('UserMood', usr, Value)
                if ObjectType == 'CALL':
                    call = ICall(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('CallStatus', call, TCallStatus(Value))
                    elif PropName == 'SEEN':
                        self._CallEventHandler('CallSeenStatusChanged', call, Value == 'TRUE')
                if ObjectType == 'CHATMESSAGE' and PropName == 'STATUS':
                    self._CallEventHandler('MessageStatus', IChatMessage(ObjectId, self), TChatMessageStatus(Value))
                if ObjectType == 'APPLICATION':
                    app = IApplication(ObjectId, self)
                    if PropName == 'CONNECTING':
                        self._CallEventHandler('ApplicationConnecting', app, map(lambda x: IUser(x, self), esplit(Value)))
                    elif PropName == 'STREAMS':
                        self._CallEventHandler('ApplicationStreams', app, map(lambda x: IApplicationStream(x, app), esplit(Value)))
                    elif PropName == 'DATAGRAM':
                        handle, text = chop(Value)
                        self._CallEventHandler('ApplicationDatagram', app, IApplicationStream(handle, app), text)
                    elif PropName == 'SENDING':
                        self._CallEventHandler('ApplicationSending', app, map(lambda x: IApplicationStream(x.split('=')[0], app), esplit(Value)))
                    elif PropName == 'RECEIVED':
                        self._CallEventHandler('ApplicationReceiving', app, map(lambda x: IApplicationStream(x.split('=')[0], app), esplit(Value)))
                elif ObjectType == 'GROUP':
                    group = IGroup(ObjectId, self)
                    if PropName == 'VISIBLE':
                        self._CallEventHandler('GroupVisible', group, Value == 'TRUE')
                    elif PropName == 'EXPANDED':
                        self._CallEventHandler('GroupExpanded', group, Value == 'TRUE')
                    elif PropName == 'USERS':
                        self._CallEventHandler('GroupUsers', group, map(lambda x: IUser(x, self), esplit(Value, ', ')))
            elif a in ['PROFILE', 'PRIVILEGE']:
                ObjectType, ObjectId, PropName, Value = [a, ''] + chop(b)
                if self._Cache:
                    self._CacheDict[str(ObjectType), unicode(ObjectId), str(PropName)] = Value
            elif a in ['CURRENTUSERHANDLE', 'USERSTATUS', 'CONNSTATUS', 'PREDICTIVE_DIALER_COUNTRY', 'SILENT_MODE', 'AUDIO_IN', 'AUDIO_OUT', 'RINGER', 'MUTE']:
                ObjectType, ObjectId, PropName, Value = [a, '', '', b]
                if self._Cache:
                    self._CacheDict[str(ObjectType), unicode(ObjectId), str(PropName)] = Value
                if ObjectType == 'MUTE':
                    self._CallEventHandler('Mute', Value == 'TRUE')
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
            elif a == 'CONNSTATUS':
                self._CallEventHandler('ConnectionStatus', TConnectionStatus(b))
            elif a == 'USERSTATUS':
                self._CallEventHandler('UserStatus', TUserStatus(b))
            elif a == 'WALLPAPER':
                self._CallEventHandler('WallpaperChanged', b)
        elif mode == 'rece':
            self._CallEventHandler('Reply', arg)
            if hasattr(arg, '_reply_handler'):
                getattr(arg, '_reply_handler')(arg)
        elif mode == 'send':
            self._CallEventHandler('Command', arg)
        elif mode == 'attach':
            self._AttachmentStatus = TAttachmentStatus(arg)
            self._CallEventHandler('AttachmentStatus', self._AttachmentStatus)
            if self._AttachmentStatus == 'REFUSED':
                raise ISkypeAPIError('Skype connection refused')

    def _DoCommand(self, com, reply=''):
        command = ICommand(-1, com, reply, True, self.Timeout)
        self.SendCommand(command)
        a, b = chop(command.Reply)
        if a == 'ERROR':
            self._CallEventHandler('Error_', command, *chop(b))
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
        command._reply_handler = self._AsyncSearchUsersEnd
        self.SendCommand(command)
        return command.Id

    def _AsyncSearchUsersEnd(self, Command):
        self._CallEventHandler('AsyncSearchUsersFinished', Command.Id, map(lambda x: IUser(x, self), esplit(chop(Command.Reply)[-1], ', ')))

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
        self._API.SendCommand(Command)
        if self._AttachmentStatus != 'SUCCESS':
            raise ISkypeError(0, 'Not attached to Skype')

    def ChangeUserStatus(self, newVal):
        self.CurrentUserStatus = newVal
        while str(newVal) not in [str(self.CurrentUser.OnlineStatus), 'UNKNOWN']:
            time.sleep(0.01)

    def CreateChatWith(self, Username):
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % Username), 2)[1], self)

    def CreateChatMultiple(self, pMembers):
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % ', '.join(map(lambda x: x.Handle, pMembers))), 2)[1], self)

    def SendVoicemail(self, Username):
        # [out, retval] IVoicemail **pVoicemail
        pass

    def ClearChatHistory(self):
        self._DoCommand('CLEAR CHARHISTORY')

    def ClearVoicemailHistory(self):
        self._DoCommand('CLEAR VOICEMAILHISTORY')

    def ClearCallHistory(self, Username='ALL', type_=TCallHistory.chsAllCalls):
        self._DoCommand('CLEAR CALLHISTORY %s %s' % (str(type_), Username))

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
        # [out, retval] ISmsMessage **pMessage
        pass

    def SendSms(self, TargetNumbers, MessageText, ReplyToNumber=''):
        # [out, retval] ISmsMessage **pMessage
        pass

    def _Property(self, ObjectType, ObjectId, PropName, Value=None, Cache=True):
        h = (str(ObjectType).upper(), unicode(ObjectId), str(PropName).upper())
        arg = ('%s %s %s' % h).split()
        while '' in arg:
            arg.remove('')
        if Value == None: # Get
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
            Value = unicode(Value)
            self._DoCommand('SET %s %s' % (' '.join(arg), Value))
            if Cache and self._Cache:
                self._CacheDict[h] = Value

    def Property(self, ObjectType, ObjectId, PropName, Value=None):
        return self._Property(ObjectType, ObjectId, PropName, Value)

    def Variable(self, Name, Value=None):
        return self._Property(Name, '', '', Value)

    def Privilege(self, Name):
        return self._Property('PRIVILEGE', '', Name) == 'TRUE'

    def Calls(self, Target=''):
        return map(lambda x: ICall(x, self), self._Search('CALLS', Target))

    def Messages(self, Target=''):
        return map(lambda x: IChatMessage(x, self), self._Search('CHATMESSAGES', Target))

    def User(self, Username=''):
        return IUser(Username, self)

    def Message(self, Id=0):
        return IChatMessage(Id, self)

    def Call(self, Id=0):
        return ICall(Id, self)

    def Chat(self, Name=''):
        return IChat(name, self)

    def Conference(self, Id=0):
        return IConference(Id, self)

    def Profile(self, Property, Value=None):
        return self._Property('PROFILE', '', Property, Value)

    def Application(self, Name):
        return IApplication(Name, self)

    def Greeting(self, Username=''):
        # TODO
        pass

    def Command(self, Id, command, Reply='', Block=False, Timeout=30000):
        return ICommand(Id, command, Reply, Block, Timeout)

    def Voicemail(self, Id):
        return IVoicemail(Id, self)

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

    def ResetIdleTimer(self):
        self._DoCommand('RESETIDLETIMER')

    Timeout = property(lambda self: self._Timeout, _SetTimeout)
    Protocol = property(lambda self: self._API.Protocol, _SetProtocol)
    CurrentUserHandle = property(lambda self: self.Variable('CURRENTUSERHANDLE'))
    CurrentUserStatus = property(lambda self: TUserStatus(self.Variable('USERSTATUS')),
                                 lambda self, value: self.Variable('USERSTATUS', str(value)))
    ConnectionStatus = property(lambda self: TConnectionStatus(self.Variable('CONNSTATUS')))
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
    ApiWrapperVersion = property(lambda self: unicode(_version_))
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

    '''
    IConferenceCollection Conferences
    IVoicemailCollection Voicemails
    IVoicemailCollection MissedVoicemails
    ISmsMessageCollection Smss
    ISmsMessageCollection MissedSmss
    IFileTransferCollection FileTransfers
    IFileTransferCollection ActiveFileTransfers
    '''
