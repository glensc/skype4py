'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from API import *
from errors import *
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
import threading


ISkypeEventHandling = EventHandling([
    'Notify', # custom
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
    'FileTransferStatusChanged',
    'CallTransferStatusChanged',
    'ChatMembersChanged',
    'ChatMemberRoleChanged'])


class ISkype(ISkypeEventHandling):
    def __init__(self, Events=None, **Options):
        ISkypeEventHandling.__init__(self)
        if Events:
            self._SetEventHandlerObj(Events)

        self._API = ISkypeAPI(self._Handler, **Options)

        self._Cache = True
        self.ResetCache()

        self._Timeout = 30000

        self._Convert = IConversion(self)
        self._Client = IClient(self)
        self._Settings = ISettings(self)
        self._Profile = IProfile(self)

    def __del__(self):
        self._API.Close()

    def _Handler(self, mode, arg):
        # low-level API callback
        if mode == 'rece_api':
            self._CallEventHandler('Notify', arg)
            a, b = chop(arg)
            ObjectType = None
            # if..elif handling cache and most event handlers
            if a in ('CALL', 'USER', 'GROUP', 'CHAT', 'CHATMESSAGE', 'CHATMEMBER', 'VOICEMAIL', 'APPLICATION', 'SMS', 'FILETRANSFER'):
                ObjectType, ObjectId, PropName, Value = [a] + chop(b, 2)
                self._CacheDict[str(ObjectType), str(ObjectId), str(PropName)] = Value
                if ObjectType == 'USER':
                    o = IUser(ObjectId, self)
                    if PropName == 'ONLINESTATUS':
                        self._CallEventHandler('OnlineStatus', o, Value)
                    elif PropName == 'MOOD_TEXT' or PropName == 'RICH_MOOD_TEXT':
                        self._CallEventHandler('UserMood', o, Value)
                elif ObjectType == 'CALL':
                    o = ICall(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('CallStatus', o, Value)
                    elif PropName == 'SEEN':
                        self._CallEventHandler('CallSeenStatusChanged', o, Value == 'TRUE')
                    elif PropName == 'VAA_INPUT_STATUS':
                        self._CallEventHandler('CallInputStatusChanged', o, Value == 'TRUE')
                    elif PropName == 'TRANSFER_STATUS':
                        self._CallEventHandler('CallTransferStatusChanged', o, Value)
                elif ObjectType == 'CHAT':
                    o = IChat(ObjectId, self)
                    if PropName == 'MEMBERS':
                        self._CallEventHandler('ChatMembersChanged', o, tuple(IUser(x, self) for x in esplit(Value)))
                elif ObjectType == 'CHATMEMBER':
                    o = IChatMember(ObjectId, self)
                    if PropName == 'ROLE':
                        self._CallEventHandler('ChatMemberRoleChanged', o, Value)
                elif ObjectType == 'CHATMESSAGE':
                    o = IChatMessage(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('MessageStatus', o, Value)
                elif ObjectType == 'APPLICATION':
                    o = IApplication(ObjectId, self)
                    if PropName == 'CONNECTING':
                        self._CallEventHandler('ApplicationConnecting', o, tuple(IUser(x, self) for x in esplit(Value)))
                    elif PropName == 'STREAMS':
                        self._CallEventHandler('ApplicationStreams', o, tuple(IApplicationStream(x, o) for x in esplit(Value)))
                    elif PropName == 'DATAGRAM':
                        handle, text = chop(Value)
                        self._CallEventHandler('ApplicationDatagram', o, IApplicationStream(handle, o), text)
                    elif PropName == 'SENDING':
                        self._CallEventHandler('ApplicationSending', o, tuple(IApplicationStream(x.split('=')[0], o) for x in esplit(Value)))
                    elif PropName == 'RECEIVED':
                        self._CallEventHandler('ApplicationReceiving', o, tuple(IApplicationStream(x.split('=')[0], o) for x in esplit(Value)))
                elif ObjectType == 'GROUP':
                    o = IGroup(ObjectId, self)
                    if PropName == 'VISIBLE':
                        self._CallEventHandler('GroupVisible', o, Value == 'TRUE')
                    elif PropName == 'EXPANDED':
                        self._CallEventHandler('GroupExpanded', o, Value == 'TRUE')
                    elif PropName == 'USERS':
                        self._CallEventHandler('GroupUsers', o, tuple(IUser(x, self) for x in esplit(Value, ', ')))
                elif ObjectType == 'SMS':
                    o = ISmsMessage(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('SmsMessageStatusChanged', o, Value)
                    elif PropName == 'TARGET_STATUSES':
                        for t in esplit(Value, ', '):
                            number, status = t.split('=')
                            self._CallEventHandler('SmsTargetStatusChanged', ISmsTarget((number, o)), status)
                elif ObjectType == 'FILETRANSFER':
                    o = IFileTransfer(ObjectId, self)
                    if PropName == 'STATUS':
                        self._CallEventHandler('FileTransferStatusChanged', o, Value)
            elif a in ('PROFILE', 'PRIVILEGE'):
                ObjectType, ObjectId, PropName, Value = [a, ''] + chop(b)
                self._CacheDict[str(ObjectType), str(ObjectId), str(PropName)] = Value
            elif a in ('CURRENTUSERHANDLE', 'USERSTATUS', 'CONNSTATUS', 'PREDICTIVE_DIALER_COUNTRY', 'SILENT_MODE', 'AUDIO_IN', 'AUDIO_OUT', 'RINGER', 'MUTE'):
                ObjectType, ObjectId, PropName, Value = [a, '', '', b]
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
                    i = Value.rfind('CONTEXT ')
                    if i >= 0:
                        context = chop(Value[i+8:])[0]
                        users = ()
                        context_id = u''
                        if context in (pluginContextContact, pluginContextCall, pluginContextChat):
                            users = tuple(IUser(x, self) for x in esplit(Value[:i-1], ', '))
                        if context in (pluginContextCall, pluginContextChat):
                            j = Value.rfind('CONTEXT_ID ')
                            if j >= 0:
                                context_id = chop(Value[j+11:])[0]
                        self._CallEventHandler('PluginMenuItemClicked', IPluginMenuItem(ObjectId, self), users, context, context_id)
            elif a == 'WALLPAPER':
                self._CallEventHandler('WallpaperChanged', b)
        elif mode == 'rece':
            self._CallEventHandler('Reply', arg)
        elif mode == 'send':
            self._CallEventHandler('Command', arg)
        elif mode == 'attach':
            self._CallEventHandler('AttachmentStatus', arg)
            if arg == apiAttachRefused:
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

    def _Property(self, ObjectType, ObjectId, PropName, Set=None, Cache=True):
        h = (str(ObjectType), str(ObjectId), str(PropName))
        arg = ('%s %s %s' % h).split()
        while '' in arg:
            arg.remove('')
        if Set == None: # Get
            if Cache and self._Cache and h in self._CacheDict:
                return self._CacheDict[h]
            Value = self._DoCommand('GET %s' % ' '.join(arg))
            while arg:
                try:
                    a, b = chop(Value)
                except ValueError:
                    break
                if a.lower() != arg[0].lower():
                    break
                del arg[0]
                Value = b
            return Value
        else: # Set
            self._DoCommand('SET %s %s' % (' '.join(arg), unicode(Set)))

    def _Alter(self, ObjectType, ObjectId, AlterName, Args=None, Reply=None):
        com = 'ALTER %s %s %s' % (str(ObjectType), str(ObjectId), str(AlterName))
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
            if a.lower() != arg[0].lower():
                break
            del arg[0]
            reply = b
        return reply

    def _Search(self, ObjectType, Args=None):
        com = 'SEARCH %s' % ObjectType
        if Args != None:
            com = '%s %s' % (com, Args)
        return esplit(chop(self._DoCommand(com))[-1], ', ')

    def Attach(self, Protocol=5, Wait=True):
        '''Connects to Skype API.'''
        try:
            self._API.Protocol = Protocol
            self._API.Attach(self.Timeout, Wait)
        except ISkypeAPIError:
            self.ResetCache()
            raise

    def SendCommand(self, Command):
        '''Sends Skype API command.'''
        try:
            self._API.SendCommand(Command)
        except ISkypeAPIError:
            self.ResetCache()
            raise

    def Command(self, Command, Reply=u'', Block=False, Timeout=30000, Id=-1):
        '''Returns a new command object.'''
        return ICommand(Id, Command, Reply, Block, Timeout)

    def SearchForUsers(self, Target):
        '''Returns collection of users found as the result of search operation.'''
        return tuple(IUser(x, self) for x in self._Search('USERS', Target))

    def AsyncSearchUsers(self, Target):
        '''Search for Skype users.'''
        def reply_handler(command):
            if command.Command.startswith('SEARCH USERS'):
                self._CallEventHandler('AsyncSearchUsersFinished', command.Id, tuple(IUser(x, self) for x in esplit(chop(command.Reply)[-1], ', ')))
                self.UnregisterEventHandler('Reply', reply_handler)
        command = ICommand(-1, 'SEARCH USERS %s' % Target, 'USERS', False, self.Timeout)
        self.RegisterEventHandler('Reply', reply_handler)
        self.SendCommand(command)
        # return pCookie - search identifier
        return command.Id

    def PlaceCall(self, *Targets):
        '''Calls specified target(s) and returns a new call object.'''
        calls = self.ActiveCalls
        reply = self._DoCommand('CALL %s' % ', '.join(Targets))
        # Skype for Windows returns the call status which gives us the call Id;
        if reply.startswith('CALL '):
            return ICall(chop(reply, 2)[1], self)
        # On linux we get 'OK' as reply so we search for the new call on
        # list of active calls.
        for c in self.ActiveCalls:
            if c not in calls:
                return c
        raise ISkypeError(0, 'Placing call failed')

    def SendMessage(self, Username, Text):
        '''Sends IM message to specified user and returns a new message object.'''
        return self.CreateChatWith(Username).SendMessage(Text)

    def ChangeUserStatus(self, Val):
        '''Changes current user online status.'''
        event = threading.Event()
        def userstatus_handler(status):
            if status.upper() == Val.upper():
                event.set()
        self.RegisterEventHandler('UserStatus', userstatus_handler)
        self.CurrentUserStatus = Val
        event.wait()
        self.UnregisterEventHandler('UserStatus', userstatus_handler)

    def CreateChatWith(self, *Usernames):
        '''Creates a new chat with a one or more users.'''
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % ', '.join(Usernames)), 2)[1], self)

    def CreateChatMultiple(self, Members):
        '''Creates a new chat with multiple members specified as a list of IUser objects.'''
        return IChat(chop(self._DoCommand('CHAT CREATE %s' % ', '.join([x.Handle for x in Members])), 2)[1], self)

    def SendVoicemail(self, Username):
        '''Sends voicemail to specified user.'''
        if self._API.Protocol >= 6:
            self._DoCommand('CALLVOICEMAIL %s' % Username)
        else:
            self._DoCommand('VOICEMAIL %s' % Username)

    def ClearChatHistory(self):
        '''Clears chat history.'''
        self._DoCommand('CLEAR CHATHISTORY')

    def ClearVoicemailHistory(self):
        '''Clears voicemail history.'''
        self._DoCommand('CLEAR VOICEMAILHISTORY')

    def ClearCallHistory(self, Username='ALL', Type=chsAllCalls):
        '''Clears call history.'''
        self._DoCommand('CLEAR CALLHISTORY %s %s' % (str(Type), Username))

    def _SetCache(self, Cache):
        self._Cache = Cache

    def ResetCache(self):
        '''Empties command cache.'''
        self._CacheDict = {}

    def CreateGroup(self, GroupName):
        '''Creates a new custom group.'''
        groups = self.CustomGroups
        self._DoCommand('CREATE GROUP %s' % GroupName)
        for g in self.CustomGroups:
            if g not in groups and g.DisplayName == GroupName:
                return g
        raise ISkypeError(0, 'Group creating failed')

    def DeleteGroup(self, GroupId):
        '''Deletes a custom group.'''
        self._DoCommand('DELETE GROUP %s' % GroupId)

    def CreateSms(self, MessageType, *TargetNumbers):
        '''Returns new SMS object.'''
        return ISmsMessage(chop(self._DoCommand('CREATE SMS %s %s' % (MessageType, ', '.join(TargetNumbers))), 2)[1], self)

    def SendSms(self, MessageText, *TargetNumbers, **Options):
        '''Sends a SMS messages.'''
        sms = ISmsMessage(chop(self._DoCommand('CREATE SMS OUTGOING %s' % ', '.join(TargetNumbers)), 2)[1], self)
        sms.Body = MessageText
        sms.__dict__.update(Options)
        sms.Send()
        return sms

    def Property(self, ObjectType, ObjectId, PropName, Set=None):
        '''Returns/sets USER, CALL, CHAT, CHATMESSAGE or VOICEMAIL object property value.'''
        return self._Property(ObjectType, ObjectId, PropName, Set)

    def Variable(self, Name, Set=None):
        '''Returns/sets general variable value.'''
        return self._Property(Name, '', '', Set)

    def Privilege(self, Name):
        '''Returns current user privilege.'''
        return self._Property('PRIVILEGE', '', Name.upper()) == 'TRUE'

    def Calls(self, Target=''):
        return tuple(ICall(x, self) for x in self._Search('CALLS', Target))

    def Messages(self, Target=''):
        return tuple(IChatMessage(x, self) for x in self._Search('CHATMESSAGES', Target))

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
        if Id <= 0 or not o.Calls:
            raise ISkypeError(0, 'Unknown conference')
        return o

    def Profile(self, Property, Set=None):
        '''Returns user profile property value.'''
        return self._Property('PROFILE', '', Property, Set)

    def Application(self, Name):
        '''Returns new application object.'''
        return IApplication(Name, self)

    def Greeting(self, Username=''):
        for v in self.Voicemails:
            if Username and v.PartnerHandle != Username:
                continue
            if v.Type in (vmtDefaultGreeting, vmtCustomGreeting):
                return v

    def Voicemail(self, Id):
        '''Returns voicemail object.'''
        o = IVoicemail(Id, self)
        o.Type
        return o

    def ApiSecurityContextEnabled(self, Context):
        '''Checks for enabled API security contexts.'''
        self._API.ApiSecurityContextEnabled(Context)

    def EnableApiSecurityContext(self, Context):
        '''Enables API security contexts.'''
        self._API.EnableApiSecurityContext(Context)

    def _GetApiWrapperVersion(self):
        from Skype4Py import __version__
        return unicode(__version__)

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
            if cid > 0 and cid not in [x.Id for x in confs]:
                confs.append(IConference(cid, self))
        return tuple(confs)

    def CreateChatUsingBlob(self, Blob):
        return IChat(chop(self._DoCommand('CHAT CREATEUSINGBLOB %s' % Blob), 2)[1], self)

    def FindChatUsingBlob(self, Blob):
        return IChat(chop(self._DoCommand('CHAT FINDUSINGBLOB %s' % Blob), 2)[1], self)

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
    Friends = property(lambda self: tuple(IUser(x, self) for x in self._Search('FRIENDS')))

    Client = property(lambda self: self._Client)
    AttachmentStatus = property(lambda self: self._API.AttachmentStatus)

    CurrentUserProfile = property(lambda self: self._Profile)

    Groups = property(lambda self: tuple(IGroup(x, self) for x in self._Search('GROUPS', 'ALL')))
    CustomGroups = property(lambda self: tuple(IGroup(x, self) for x in self._Search('GROUPS', 'CUSTOM')))
    HardwiredGroups = property(lambda self: tuple(IGroup(x, self) for x in self._Search('GROUPS', 'HARDWIRED')))

    ActiveCalls = property(lambda self: tuple(ICall(x, self) for x in self._Search('ACTIVECALLS')))
    MissedCalls = property(lambda self: tuple(ICall(x, self) for x in self._Search('MISSEDCALLS')))

    FriendlyName = property(fset=_SetFriendlyName)
    ApiWrapperVersion = property(_GetApiWrapperVersion)
    SilentMode = property(lambda self: self.Variable('SILENT_MODE') == 'ON',
                          lambda self, value: self.SendCommand(ICommand(-1, 'SET SILENT_MODE %s' % 'ON' if value else 'OFF')))
    Settings = property(lambda self: self._Settings)

    UsersWaitingAuthorization = property(lambda self: tuple(IUser(x, self) for x in self._Search('USERSWAITINGMYAUTHORIZATION')))
    Cache = property(lambda self: self._Cache, _SetCache)
    CommandId = property(lambda self: True)

    Chats = property(lambda self: tuple(IChat(x, self) for x in self._Search('CHATS')))
    ActiveChats = property(lambda self: tuple(IChat(x, self) for x in self._Search('ACTIVECHATS')))
    MissedChats = property(lambda self: tuple(IChat(x, self) for x in self._Search('MISSEDCHATS')))
    RecentChats = property(lambda self: tuple(IChat(x, self) for x in self._Search('RECENTCHATS')))
    BookmarkedChats = property(lambda self: tuple(IChat(x, self) for x in self._Search('BOOKMARKEDCHATS')))
    MissedMessages = property(lambda self: tuple(IChatMessage(x, self) for x in self._Search('MISSEDCHATMESSAGES')))

    Voicemails = property(lambda self: tuple(IVoicemail(x, self) for x in self._Search('VOICEMAILS')))
    MissedVoicemails = property(lambda self: tuple(IVoicemail(x, self) for x in self._Search('MISSEDVOICEMAILS')))

    Conferences = property(_GetConferences)
    Smss = property(lambda self: tuple(ISmsMessage(x, self) for x in self._Search('SMSS')))
    MissedSmss = property(lambda self: tuple(ISmsMessage(x, self) for x in self._Search('MISSEDSMSS')))
    FileTransfers = property(lambda self: tuple(IFileTransfer(x, self) for x in self._Search('FILETRANSFERS')))
    ActiveFileTransfers = property(lambda self: tuple(IFileTransfer(x, self) for x in self._Search('ACTIVEFILETRANSFERS')))

    FocusedContacts = property(lambda self: tuple(IUser(x, self) for x in esplit(chop(self.Variable('CONTACTS_FOCUSED'), 2)[-1])))
