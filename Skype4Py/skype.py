'''Main Skype interface.
'''

import threading

from api import *
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


class Skype(EventHandlingBase):
    '''The main class which you have to instatinate to get access to Skype client.

      1. Usage.

         You should access this class using the alias at the package level::

             import Skype4Py

             skype = Skype4Py.Skype()

         For possible constructor arguments, read the L{Skype.__init__} description.

      2. Events.

         This class provides events.

         The events names and their arguments lists can be found in L{SkypeEvents} class.

         The usage of events is described in L{EventHandlingBase} class which is a superclass of
         this class. Follow the link for more information.

    @newfield option: Option, Options

    @ivar OnNotify: Event handler for L{SkypeEvents.Notify} event. See L{EventHandlingBase} for more information on events.
    @type OnNotify: callable

    @ivar OnCommand: Event handler for L{SkypeEvents.Command} event. See L{EventHandlingBase} for more information on events.
    @type OnCommand: callable

    @ivar OnReply: Event handler for L{SkypeEvents.Reply} event. See L{EventHandlingBase} for more information on events.
    @type OnReply: callable

    @ivar OnError: Event handler for L{SkypeEvents.Error} event. See L{EventHandlingBase} for more information on events.
    @type OnError: callable

    @ivar OnAttachmentStatus: Event handler for L{SkypeEvents.AttachmentStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnAttachmentStatus: callable

    @ivar OnConnectionStatus: Event handler for L{SkypeEvents.ConnectionStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnConnectionStatus: callable

    @ivar OnUserStatus: Event handler for L{SkypeEvents.UserStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnUserStatus: callable

    @ivar OnOnlineStatus: Event handler for L{SkypeEvents.OnlineStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnOnlineStatus: callable

    @ivar OnCallStatus: Event handler for L{SkypeEvents.CallStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnCallStatus: callable

    @ivar OnCallHistory: Event handler for L{SkypeEvents.CallHistory} event. See L{EventHandlingBase} for more information on events.
    @type OnCallHistory: callable

    @ivar OnMute: Event handler for L{SkypeEvents.Mute} event. See L{EventHandlingBase} for more information on events.
    @type OnMute: callable

    @ivar OnMessageStatus: Event handler for L{SkypeEvents.MessageStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnMessageStatus: callable

    @ivar OnMessageHistory: Event handler for L{SkypeEvents.MessageHistory} event. See L{EventHandlingBase} for more information on events.
    @type OnMessageHistory: callable

    @ivar OnAutoAway: Event handler for L{SkypeEvents.AutoAway} event. See L{EventHandlingBase} for more information on events.
    @type OnAutoAway: callable

    @ivar OnCallDtmfReceived: Event handler for L{SkypeEvents.CallDtmfReceived} event. See L{EventHandlingBase} for more information on events.
    @type OnCallDtmfReceived: callable

    @ivar OnVoicemailStatus: Event handler for L{SkypeEvents.VoicemailStatus} event. See L{EventHandlingBase} for more information on events.
    @type OnVoicemailStatus: callable

    @ivar OnApplicationConnecting: Event handler for L{SkypeEvents.ApplicationConnecting} event. See L{EventHandlingBase} for more information on events.
    @type OnApplicationConnecting: callable

    @ivar OnApplicationStreams: Event handler for L{SkypeEvents.ApplicationStreams} event. See L{EventHandlingBase} for more information on events.
    @type OnApplicationStreams: callable

    @ivar OnApplicationDatagram: Event handler for L{SkypeEvents.ApplicationDatagram} event. See L{EventHandlingBase} for more information on events.
    @type OnApplicationDatagram: callable

    @ivar OnApplicationSending: Event handler for L{SkypeEvents.ApplicationSending} event. See L{EventHandlingBase} for more information on events.
    @type OnApplicationSending: callable

    @ivar OnApplicationReceiving: Event handler for L{SkypeEvents.ApplicationReceiving} event. See L{EventHandlingBase} for more information on events.
    @type OnApplicationReceiving: callable

    @ivar OnContactsFocused: Event handler for L{SkypeEvents.ContactsFocused} event. See L{EventHandlingBase} for more information on events.
    @type OnContactsFocused: callable

    @ivar OnGroupVisible: Event handler for L{SkypeEvents.GroupVisible} event. See L{EventHandlingBase} for more information on events.
    @type OnGroupVisible: callable

    @ivar OnGroupExpanded: Event handler for L{SkypeEvents.GroupExpanded} event. See L{EventHandlingBase} for more information on events.
    @type OnGroupExpanded: callable

    @ivar OnGroupUsers: Event handler for L{SkypeEvents.GroupUsers} event. See L{EventHandlingBase} for more information on events.
    @type OnGroupUsers: callable

    @ivar OnGroupDeleted: Event handler for L{SkypeEvents.GroupDeleted} event. See L{EventHandlingBase} for more information on events.
    @type OnGroupDeleted: callable

    @ivar OnUserMood: Event handler for L{SkypeEvents.UserMood} event. See L{EventHandlingBase} for more information on events.
    @type OnUserMood: callable

    @ivar OnSmsMessageStatusChanged: Event handler for L{SkypeEvents.SmsMessageStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnSmsMessageStatusChanged: callable

    @ivar OnSmsTargetStatusChanged: Event handler for L{SkypeEvents.SmsTargetStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnSmsTargetStatusChanged: callable

    @ivar OnCallInputStatusChanged: Event handler for L{SkypeEvents.CallInputStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallInputStatusChanged: callable

    @ivar OnAsyncSearchUsersFinished: Event handler for L{SkypeEvents.AsyncSearchUsersFinished} event. See L{EventHandlingBase} for more information on events.
    @type OnAsyncSearchUsersFinished: callable

    @ivar OnCallSeenStatusChanged: Event handler for L{SkypeEvents.CallSeenStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallSeenStatusChanged: callable

    @ivar OnPluginEventClicked: Event handler for L{SkypeEvents.PluginEventClicked} event. See L{EventHandlingBase} for more information on events.
    @type OnPluginEventClicked: callable

    @ivar OnPluginMenuItemClicked: Event handler for L{SkypeEvents.PluginMenuItemClicked} event. See L{EventHandlingBase} for more information on events.
    @type OnPluginMenuItemClicked: callable

    @ivar OnWallpaperChanged: Event handler for L{SkypeEvents.WallpaperChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnWallpaperChanged: callable

    @ivar OnFileTransferStatusChanged: Event handler for L{SkypeEvents.FileTransferStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnFileTransferStatusChanged: callable

    @ivar OnCallTransferStatusChanged: Event handler for L{SkypeEvents.CallTransferStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallTransferStatusChanged: callable

    @ivar OnChatMembersChanged: Event handler for L{SkypeEvents.ChatMembersChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnChatMembersChanged: callable

    @ivar OnChatMemberRoleChanged: Event handler for L{SkypeEvents.ChatMemberRoleChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnChatMemberRoleChanged: callable

    @ivar OnCallVideoReceiveStatusChanged: Event handler for L{SkypeEvents.CallVideoReceiveStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallVideoReceiveStatusChanged: callable

    @ivar OnCallVideoSendStatusChanged: Event handler for L{SkypeEvents.CallVideoSendStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallVideoSendStatusChanged: callable

    @ivar OnCallVideoStatusChanged: Event handler for L{SkypeEvents.CallVideoStatusChanged} event. See L{EventHandlingBase} for more information on events.
    @type OnCallVideoStatusChanged: callable

    @ivar OnChatWindowState: Event handler for L{SkypeEvents.ChatWindowState} event. See L{EventHandlingBase} for more information on events.
    @type OnChatWindowState: callable

    @ivar OnClientWindowState: Event handler for L{SkypeEvents.ClientWindowState} event. See L{EventHandlingBase} for more information on events.
    @type OnClientWindowState: callable
    '''

    def __init__(self, Events=None, **Options):
        '''Initializes the object.

        @param Events: An optional object with event handlers. See L{EventHandlingBase} for more information on events.
        @type Events: object
        @param Options: Addtional options for the low-level API handler. For supported options, go to L{Skype4Py.api}
        subpackage and select your platform.
        @type Options: kwargs
        '''
        EventHandlingBase.__init__(self)
        if Events:
            self._SetEventHandlerObj(Events)

        self._API = SkypeAPI(Options)
        self._API.register_handler(self._Handler)

        self._Cache = True
        self.ResetCache()

        self._Timeout = 30000

        self._Convert = Conversion(self)
        self._Client = Client(self)
        self._Settings = Settings(self)
        self._Profile = Profile(self)

    def __del__(self):
        '''Frees all resources.
        '''
        if hasattr(self, '_API'):
            self._API.close()

    def _Handler(self, Mode, Arg):
        # low-level API callback
        if Mode == 'rece_api':
            self._CallEventHandler('Notify', Arg)
            a, b = chop(Arg)
            object_type = None
            # if..elif handling cache and most event handlers
            if a in ('CALL', 'USER', 'GROUP', 'CHAT', 'CHATMESSAGE', 'CHATMEMBER', 'VOICEMAIL', 'APPLICATION', 'SMS', 'FILETRANSFER'):
                object_type, object_id, prop_name, value = [a] + chop(b, 2)
                self._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
                if object_type == 'USER':
                    o = User(object_id, self)
                    if prop_name == 'ONLINESTATUS':
                        self._CallEventHandler('OnlineStatus', o, str(value))
                    elif prop_name == 'MOOD_TEXT' or prop_name == 'RICH_MOOD_TEXT':
                        self._CallEventHandler('UserMood', o, value)
                    elif prop_name == 'RECEIVEDAUTHREQUEST':
                        self._CallEventHandler('UserAuthorizationRequestReceived', o)
                elif object_type == 'CALL':
                    o = Call(object_id, self)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('CallStatus', o, str(value))
                    elif prop_name == 'SEEN':
                        self._CallEventHandler('CallSeenStatusChanged', o, (value == 'TRUE'))
                    elif prop_name == 'VAA_INPUT_STATUS':
                        self._CallEventHandler('CallInputStatusChanged', o, (value == 'TRUE'))
                    elif prop_name == 'TRANSFER_STATUS':
                        self._CallEventHandler('CallTransferStatusChanged', o, str(value))
                    elif prop_name == 'DTMF':
                        self._CallEventHandler('CallDtmfReceived', o, str(value))
                    elif prop_name == 'VIDEO_STATUS':
                        self._CallEventHandler('CallVideoStatusChanged', o, str(value))
                    elif prop_name == 'VIDEO_SEND_STATUS':
                        self._CallEventHandler('CallVideoSendStatusChanged', o, str(value))
                    elif prop_name == 'VIDEO_RECEIVE_STATUS':
                        self._CallEventHandler('CallVideoReceiveStatusChanged', o, str(value))
                elif object_type == 'CHAT':
                    o = Chat(object_id, self)
                    if prop_name == 'MEMBERS':
                        self._CallEventHandler('ChatMembersChanged', o, gen(User(x, self) for x in split(value)))
                    if prop_name in ('OPENED', 'CLOSED'):
                        self._CallEventHandler('ChatWindowState', o, (prop_name == 'OPENED'))
                elif object_type == 'CHATMEMBER':
                    o = ChatMember(object_id, self)
                    if prop_name == 'ROLE':
                        self._CallEventHandler('ChatMemberRoleChanged', o, str(value))
                elif object_type == 'CHATMESSAGE':
                    o = ChatMessage(object_id, self)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('MessageStatus', o, str(value))
                elif object_type == 'APPLICATION':
                    o = Application(object_id, self)
                    if prop_name == 'CONNECTING':
                        self._CallEventHandler('ApplicationConnecting', o, gen(User(x, self) for x in split(value)))
                    elif prop_name == 'STREAMS':
                        self._CallEventHandler('ApplicationStreams', o, gen(ApplicationStream(x, o) for x in split(value)))
                    elif prop_name == 'DATAGRAM':
                        handle, text = chop(value)
                        self._CallEventHandler('ApplicationDatagram', o, ApplicationStream(handle, o), text)
                    elif prop_name == 'SENDING':
                        self._CallEventHandler('ApplicationSending', o, gen(ApplicationStream(x.split('=')[0], o) for x in split(value)))
                    elif prop_name == 'RECEIVED':
                        self._CallEventHandler('ApplicationReceiving', o, gen(ApplicationStream(x.split('=')[0], o) for x in split(value)))
                elif object_type == 'GROUP':
                    o = Group(object_id, self)
                    if prop_name == 'VISIBLE':
                        self._CallEventHandler('GroupVisible', o, (value == 'TRUE'))
                    elif prop_name == 'EXPANDED':
                        self._CallEventHandler('GroupExpanded', o, (value == 'TRUE'))
                    elif prop_name == 'USERS':
                        self._CallEventHandler('GroupUsers', o, gen(User(x, self) for x in split(value, ', ')))
                elif object_type == 'SMS':
                    o = SmsMessage(object_id, self)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('SmsMessageStatusChanged', o, str(value))
                    elif prop_name == 'TARGET_STATUSES':
                        for t in split(value, ', '):
                            number, status = t.split('=')
                            self._CallEventHandler('SmsTargetStatusChanged', SmsTarget((number, o)), str(status))
                elif object_type == 'FILETRANSFER':
                    o = FileTransfer(object_id, self)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('FileTransferStatusChanged', o, str(value))
                elif object_type == 'VOICEMAIL':
                    o = Voicemail(object_id, self)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('VoicemailStatus', o, str(value))
            elif a in ('PROFILE', 'PRIVILEGE'):
                object_type, object_id, prop_name, value = [a, ''] + chop(b)
                self._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
            elif a in ('CURRENTUSERHANDLE', 'USERSTATUS', 'CONNSTATUS', 'PREDICTIVE_DIALER_COUNTRY', 'SILENT_MODE', 'AUDIO_IN', 'AUDIO_OUT', 'RINGER', 'MUTE', 'AUTOAWAY', 'WINDOWSTATE'):
                object_type, object_id, prop_name, value = [a, '', '', b]
                self._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
                if object_type == 'MUTE':
                    self._CallEventHandler('Mute', value == 'TRUE')
                elif object_type == 'CONNSTATUS':
                    self._CallEventHandler('ConnectionStatus', str(value))
                elif object_type == 'USERSTATUS':
                    self._CallEventHandler('UserStatus', str(value))
                elif object_type == 'AUTOAWAY':
                    self._CallEventHandler('AutoAway', (value == 'ON'))
                elif object_type == 'WINDOWSTATE':
                    self._CallEventHandler('ClientWindowState', str(value))
                elif object_type == 'SILENT_MODE':
                    self._CallEventHandler('SilentModeStatusChanged', (value == 'ON'))
            elif a == 'CALLHISTORYCHANGED':
                self._CallEventHandler('CallHistory')
            elif a == 'IMHISTORYCHANGED':
                self._CallEventHandler('MessageHistory', '') # XXX: Arg is Skypename, which one?
            elif a == 'CONTACTS':
                prop_name, value = chop(b)
                if prop_name == 'FOCUSED':
                    self._CallEventHandler('ContactsFocused', str(value))
            elif a == 'DELETED':
                prop_name, value = chop(b)
                if prop_name == 'GROUP':
                    self._CallEventHandler('GroupDeleted', int(value))
            elif a == 'EVENT':
                object_id, prop_name, value = chop(b, 2)
                if prop_name == 'CLICKED':
                    self._CallEventHandler('PluginEventClicked', PluginEvent(object_id, self))
            elif a == 'MENU_ITEM':
                object_id, prop_name, value = chop(b, 2)
                if prop_name == 'CLICKED':
                    i = value.rfind('CONTEXT ')
                    if i >= 0:
                        context = chop(value[i+8:])[0]
                        users = ()
                        context_id = u''
                        if context in (pluginContextContact, pluginContextCall, pluginContextChat):
                            users = gen(User(x, self) for x in split(value[:i-1], ', '))
                        if context in (pluginContextCall, pluginContextChat):
                            j = value.rfind('CONTEXT_ID ')
                            if j >= 0:
                                context_id = str(chop(value[j+11:])[0])
                                if context == pluginContextCall:
                                    context_id = int(context_id)
                        self._CallEventHandler('PluginMenuItemClicked', PluginMenuItem(object_id, self), users, str(context), context_id)
            elif a == 'WALLPAPER':
                self._CallEventHandler('WallpaperChanged', unicode2path(b))
        elif Mode == 'rece':
            self._CallEventHandler('Reply', Arg)
        elif Mode == 'send':
            self._CallEventHandler('Command', Arg)
        elif Mode == 'attach':
            self._CallEventHandler('AttachmentStatus', str(Arg))
            if Arg == apiAttachRefused:
                raise SkypeAPIError('Skype connection refused')

    def _DoCommand(self, Cmd, ExpectedReply=''):
        command = Command(-1, Cmd, ExpectedReply, True, self.Timeout)
        self.SendCommand(command)
        a, b = chop(command.Reply)
        if a == 'ERROR':
            errnum, errstr = chop(b)
            self._CallEventHandler('Error', command, int(errnum), errstr)
            raise SkypeError(int(errnum), errstr)
        if not command.Reply.startswith(command.Expected):
            raise SkypeError(0, 'Unexpected reply from Skype, got [%s], expected [%s]' % \
                (command.Reply, command.Expected))
        return command.Reply

    def _Property(self, ObjectType, ObjectId, PropName, Set=None, Cache=True):
        h = (str(ObjectType), str(ObjectId), str(PropName))
        arg = ('%s %s %s' % h).split()
        while '' in arg:
            arg.remove('')
        jarg = ' '.join(arg)
        if Set is None: # Get
            if Cache and self._Cache and h in self._CacheDict:
                return self._CacheDict[h]
            value = self._DoCommand('GET %s' % jarg, jarg)
            while arg:
                try:
                    a, b = chop(value)
                except ValueError:
                    break
                if a.lower() != arg[0].lower():
                    break
                del arg[0]
                value = b
            if Cache and self._Cache:
                self._CacheDict[h] = value
            return value
        else: # Set
            value = tounicode(Set)
            self._DoCommand('SET %s %s' % (jarg, value), jarg)
            if Cache and self._Cache:
                self._CacheDict[h] = value

    def _Alter(self, ObjectType, ObjectId, AlterName, Args=None, Reply=None):
        com = 'ALTER %s %s %s' % (str(ObjectType), str(ObjectId), str(AlterName))
        if Reply is None:
            Reply = com
        if Args is not None:
            com = '%s %s' % (com, tounicode(Args))
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
        if Args is not None:
            com = '%s %s' % (com, Args)
        return tuple(split(chop(self._DoCommand(com))[-1], ', '))

    def ApiSecurityContextEnabled(self, Context):
        '''Queries if an API security context for Internet Explorer is enabled.

        @param Context: API security context to check.
        @type Context: unicode
        @return: True if the API security for the given context is enabled, False elsewhere.
        @rtype: bool

        @warning: This functionality isn't supported by Skype4Py.
        '''
        self._API.security_context_enabled(Context)

    def Application(self, Name):
        '''Queries an application object.

        @param Name: Application name.
        @type Name: unicode
        @return: The application object.
        @rtype: L{Application}
        '''
        return Application(Name, self)

    def _AsyncSearchUsersReplyHandler(self, Command):
        if Command in self._AsyncSearchUsersCommands:
            self._AsyncSearchUsersCommands.remove(Command)
            self._CallEventHandler('AsyncSearchUsersFinished', Command.Id,
                gen(User(x, self) for x in split(chop(Command.Reply)[-1], ', ')))
            if len(self._AsyncSearchUsersCommands) == 0:
                self.UnregisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
                del self._AsyncSearchUsersCommands

    def AsyncSearchUsers(self, Target):
        '''Asynchronously searches for Skype users.

        @param Target: Search target (name or email address).
        @type Target: unicode
        @return: A search identifier. It will be passed along with the results to the
        L{SkypeEvents.AsyncSearchUsersFinished} event after the search is completed.
        @rtype: int
        '''
        if not hasattr(self, '_AsyncSearchUsersCommands'):
            self._AsyncSearchUsersCommands = []
            self.RegisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
        command = Command(-1, 'SEARCH USERS %s' % tounicode(Target), 'USERS', False, self.Timeout)
        self._AsyncSearchUsersCommands.append(command)
        self.SendCommand(command)
        # return pCookie - search identifier
        return command.Id

    def Attach(self, Protocol=5, Wait=True):
        '''Establishes a connection to Skype.

        @param Protocol: Minimal Skype protocol version.
        @type Protocol: int
        @param Wait: If set to False, blocks forever until the connection is established.
        Otherwise, timeouts after the L{Timeout}.
        @type Wait: bool
        '''
        try:
            self._API.protocol = Protocol
            self._API.attach(self.Timeout, Wait)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def Call(self, Id=0):
        '''Queries a call object.

        @param Id: Call identifier.
        @type Id: int
        @return: Call object.
        @rtype: L{Call}
        '''
        o = Call(Id, self)
        o.Status # Test if such a call exists.
        return o

    def Calls(self, Target=''):
        '''Queries calls in call history.

        @param Target: Call target.
        @type Target: str
        @return: Call objects.
        @rtype: tuple of L{Call}
        '''
        return gen(Call(x, self) for x in self._Search('CALLS', Target))

    def _ChangeUserStatus_UserStatus(self, Status):
        if Status.upper() == self._ChangeUserStatus_Status:
            self._ChangeUserStatus_Event.set()

    def ChangeUserStatus(self, Status):
        '''Changes the online status for the current user.

        @param Status: New online status for the user.
        @type Status: L{User status<enums.cusUnknown>}

        @note: This function waits until the online status changes. Alternatively, use
        the L{CurrentUserStatus} property to perform an immediate change of status.
        '''
        if self.CurrentUserStatus.upper() == Status.upper():
            return
        self._ChangeUserStatus_Event = threading.Event()
        self._ChangeUserStatus_Status = Status.upper()
        self.RegisterEventHandler('UserStatus', self._ChangeUserStatus_UserStatus)
        self.CurrentUserStatus = Status
        self._ChangeUserStatus_Event.wait()
        self.UnregisterEventHandler('UserStatus', self._ChangeUserStatus_UserStatus)
        del self._ChangeUserStatus_Event, self._ChangeUserStatus_Status

    def Chat(self, Name=''):
        '''Queries a chat object.

        @param Name: Chat name.
        @type Name: str
        @return: A chat object.
        @rtype: L{Chat}
        '''
        o = Chat(Name, self)
        o.Status # Tests if such a chat really exists.
        return o

    def ClearCallHistory(self, Username='ALL', Type=chsAllCalls):
        '''Clears the call history.

        @param Username: Skypename of the user. A special value of 'ALL' means that entries of all users should
        be removed.
        @type Username: str
        @param Type: Call type.
        @type Type: L{Call type<enums.cltUnknown>}
        '''
        self._DoCommand('CLEAR CALLHISTORY %s %s' % (str(Type), Username))

    def ClearChatHistory(self):
        '''Clears the chat history.
        '''
        self._DoCommand('CLEAR CHATHISTORY')

    def ClearVoicemailHistory(self):
        '''Clears the voicemail history.
        '''
        self._DoCommand('CLEAR VOICEMAILHISTORY')

    def Command(self, Command, Reply=u'', Block=False, Timeout=30000, Id=-1):
        '''Creates an API command object.

        @param Command: Command string.
        @type Command: unicode
        @param Reply: Expected reply. By default any reply is accepted (except errors
        which raise an L{SkypeError} exception).
        @type Reply: unicode
        @param Block: If set to True, L{SendCommand} method waits for a response from Skype API before returning.
        @type Block: bool
        @param Timeout: Timeout in milliseconds. Used if Block=True.
        @type Timeout: int
        @param Id: Command Id. The default (-1) means it will be assigned automatically as soon as the command is sent.
        @type Id: int
        @return: A command object.
        @rtype: L{Command}
        @see: L{SendCommand}
        '''
        from API import Command as COMMAND
        return COMMAND(Id, Command, Reply, Block, Timeout)

    def Conference(self, Id=0):
        '''Queries a call conference object.

        @param Id: Conference Id.
        @type Id: int
        @return: A conference object.
        @rtype: L{Conference}
        '''
        o = Conference(Id, self)
        if Id <= 0 or not o.Calls:
            raise ISkypeError(0, 'Unknown conference')
        return o

    def CreateChatUsingBlob(self, Blob):
        '''Returns existing or joins a new chat using given blob.

        @param Blob: A blob indentifying the chat.
        @type Blob: str
        @return: A chat object
        @rtype: L{Chat}
        '''
        return Chat(chop(self._DoCommand('CHAT CREATEUSINGBLOB %s' % Blob), 2)[1], self)

    def CreateChatWith(self, *Usernames):
        '''Creates a chat with one or more users.

        @param Usernames: One or more strings with the Skypenames of the users.
        @type Usernames: str
        @return: A chat object
        @rtype: L{Chat}
        @see: L{Chat.AddMembers}
        '''
        return Chat(chop(self._DoCommand('CHAT CREATE %s' % ', '.join(Usernames)), 2)[1], self)

    def CreateGroup(self, GroupName):
        '''Creates a custom contact group.

        @param GroupName: Group name.
        @type GroupName: unicode
        @return: A group object.
        @rtype: L{Group}
        @see: L{DeleteGroup}
        '''
        groups = self.CustomGroups
        self._DoCommand('CREATE GROUP %s' % tounicode(GroupName))
        for g in self.CustomGroups:
            if g not in groups and g.DisplayName == GroupName:
                return g
        raise SkypeError(0, 'Group creating failed')

    def CreateSms(self, MessageType, *TargetNumbers):
        '''Creates an SMS message.

        @param MessageType: Message type.
        @type MessageType: L{SMS message type<enums.smsMessageTypeUnknown>}
        @param TargetNumbers: One or more target SMS numbers.
        @type TargetNumbers: str
        @return: An sms message object.
        @rtype: L{SmsMessage}
        '''
        return SmsMessage(chop(self._DoCommand('CREATE SMS %s %s' % (MessageType, ', '.join(TargetNumbers))), 2)[1], self)

    def DeleteGroup(self, GroupId):
        '''Deletes a custom contact group.

        Users in the contact group are moved to the All Contacts (hardwired) contact group.

        @param GroupId: Group identifier. Get it from L{Group.Id}.
        @type GroupId: int
        @see: L{CreateGroup}
        '''
        self._DoCommand('DELETE GROUP %s' % GroupId)

    def EnableApiSecurityContext(self, Context):
        '''Enables an API security context for Internet Explorer scripts.

        @param Context: combination of API security context values.
        @type Context: unicode
        @warning: This functionality isn't supported by Skype4Py.
        '''
        self._API.enable_security_context(Context)

    def FindChatUsingBlob(self, Blob):
        '''Returns existing chat using given blob.

        @param Blob: A blob identifying the chat.
        @type Blob: str
        @return: A chat object
        @rtype: L{Chat}
        '''
        return Chat(chop(self._DoCommand('CHAT FINDUSINGBLOB %s' % Blob), 2)[1], self)

    def Greeting(self, Username=''):
        '''Queries the greeting used as voicemail.

        @param Username: Skypename of the user.
        @type Username: str
        @return: A voicemail object.
        @rtype: L{Voicemail}
        '''
        for v in self.Voicemails:
            if Username and v.PartnerHandle != Username:
                continue
            if v.Type in (vmtDefaultGreeting, vmtCustomGreeting):
                return v

    def Message(self, Id=0):
        '''Queries a chat message object.

        @param Id: Message Id.
        @type Id: int
        @return: A chat message object.
        @rtype: L{ChatMessage}
        '''
        o = ChatMessage(Id, self)
        o.Status # Test if such an id is known.
        return o

    def Messages(self, Target=''):
        '''Queries chat messages which were sent/received by the user.

        @param Target: Message sender.
        @type Target: str
        @return: Chat message objects.
        @rtype: tuple of L{ChatMessage}
        '''
        return gen(ChatMessage(x, self) for x in self._Search('CHATMESSAGES', Target))

    def PlaceCall(self, *Targets):
        '''Places a call to a single user or creates a conference call.

        @param Targets: One or more call targets. If multiple targets are specified, a conference
        call is created. The call target can be a Skypename, phone number, or speed dial code.
        @type Targets: str
        @return: A call object.
        @rtype: L{Call}
        '''
        calls = self.ActiveCalls
        reply = self._DoCommand('CALL %s' % ', '.join(Targets))
        # Skype for Windows returns the call status which gives us the call Id;
        if reply.startswith('CALL '):
            return Call(chop(reply, 2)[1], self)
        # On linux we get 'OK' as reply so we search for the new call on
        # list of active calls.
        for c in self.ActiveCalls:
            if c not in calls:
                return c
        raise SkypeError(0, 'Placing call failed')

    def Privilege(self, Name):
        '''Queries the Skype services (privileges) enabled for the Skype client.

        @param Name: Privilege name, currently one of 'SKYPEOUT', 'SKYPEIN', 'VOICEMAIL'.
        @type Name: str
        @return: True if the privilege is available, False otherwise.
        @rtype: bool
        '''
        return (self._Property('PRIVILEGE', '', Name.upper()) == 'TRUE')

    def Profile(self, Property, Set=None):
        '''Queries/sets user profile properties.

        @param Property: Property name, currently one of 'PSTN_BALANCE', 'PSTN_BALANCE_CURRENCY',
        'FULLNAME', 'BIRTHDAY', 'SEX', 'LANGUAGES', 'COUNTRY', 'PROVINCE', 'CITY', 'PHONE_HOME',
        'PHONE_OFFICE', 'PHONE_MOBILE', 'HOMEPAGE', 'ABOUT'.
        @type Property: str
        @param Set: Value the property should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Property value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        return self._Property('PROFILE', '', Property, Set)

    def Property(self, ObjectType, ObjectId, PropName, Set=None):
        '''Queries/sets the properties of an object.

        @param ObjectType: Object type ('USER', 'CALL', 'CHAT', 'CHATMESSAGE', ...).
        @type ObjectType: str
        @param ObjectId: Object Id, depends on the object type.
        @type ObjectId: str
        @param PropName: Name of the property to access.
        @type PropName: str
        @param Set: Value the property should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Property value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        return self._Property(ObjectType, ObjectId, PropName, Set)

    def ResetCache(self):
        '''Deletes all command cache entries.

        This method clears the Skype4Py's internal command cache which means that all objects will forget
        their property values and querying them will trigger a code to get them from Skype client (and
        cache them again).
        '''
        self._CacheDict = {}

    def SearchForUsers(self, Target):
        '''Searches for users.

        @param Target: Search target (name or email address).
        @type Target: unicode
        @return: Found users.
        @rtype: tuple of L{User}
        '''
        return gen(User(x, self) for x in self._Search('USERS', tounicode(Target)))

    def SendCommand(self, Command):
        '''Sends an API command.

        @param Command: Command to send. Use L{Command} method to create a command.
        @type Command: L{Command}
        '''
        try:
            self._API.send_command(Command)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def SendMessage(self, Username, Text):
        '''Sends a chat message.

        @param Username: Skypename of the user.
        @type Username: str
        @param Text: Body of the message.
        @type Text: unicode
        @return: A chat message object.
        @rtype: L{ChatMessage}
        '''
        return self.CreateChatWith(Username).SendMessage(Text)

    def SendSms(self, *TargetNumbers, **Properties):
        '''Creates and sends an SMS message.

        @param TargetNumbers: One or more target SMS numbers.
        @type TargetNumbers: str
        @param Properties: Message properties. Properties available are same as L{SmsMessage} object properties.
        @type Properties: kwargs
        @return: An sms message object. The message is already sent at this point.
        @rtype: L{SmsMessage}
        '''
        sms = self.CreateSms(smsMessageTypeOutgoing, *TargetNumbers)
        for prop, value in Properties.items():
            if hasattr(sms, prop):
                setattr(sms, prop, value)
            else:
                raise TypeError('Unknown property: %s' % prop)
        sms.Send()
        return sms

    def SendVoicemail(self, Username):
        '''Sends a voicemail to a specified user.

        @param Username: Skypename of the user.
        @type Username: str
        @return: A voicemail object.
        @rtype: L{Voicemail}
        '''
        if self._API.protocol >= 6:
            self._DoCommand('CALLVOICEMAIL %s' % Username)
        else:
            self._DoCommand('VOICEMAIL %s' % Username)

    def User(self, Username=''):
        '''Queries a user object.

        @param Username: Skypename of the user.
        @type Username: str
        @return: A user object.
        @rtype: L{User}
        '''
        o = User(Username, self)
        o.OnlineStatus # Test if such a user exists.
        return o

    def Variable(self, Name, Set=None):
        '''Queries/sets Skype general parameters.

        @param Name: Variable name.
        @type Name: str
        @param Set: Value the variable should be set to or None if the value should be queried.
        @type Set: unicode or None
        @return: Variable value if Set=None, None otherwise.
        @rtype: unicode or None
        '''
        return self._Property(Name, '', '', Set)

    def Voicemail(self, Id):
        '''Queries the voicemail object.

        @param Id: Voicemail Id.
        @type Id: int
        @return: A voicemail object.
        @rtype: L{Voicemail}
        '''
        o = Voicemail(Id, self)
        o.Type # Test if such a voicemail exists.
        return o

    def _GetActiveCalls(self):
        return gen(Call(x, self) for x in self._Search('ACTIVECALLS'))

    ActiveCalls = property(_GetActiveCalls,
    doc='''Queries a list of active calls.

    @type: tuple of L{Call}
    ''')

    def _GetActiveChats(self):
        return gen(Chat(x, self) for x in self._Search('ACTIVECHATS'))

    ActiveChats = property(_GetActiveChats,
    doc='''Queries a list of active chats.

    @type: tuple of L{Chat}
    ''')

    def _GetActiveFileTransfers(self):
        return gen(FileTransfer(x, self) for x in self._Search('ACTIVEFILETRANSFERS'))

    ActiveFileTransfers = property(_GetActiveFileTransfers,
    doc='''Queries currently active file transfers.

    @type: tuple of L{FileTransfer}
    ''')

    def _GetApiDebugLevel(self):
        return self._API.debug_level

    def _SetApiDebugLevel(self, Value):
        self._API.set_debug_level(int(Value))

    ApiDebugLevel = property(_GetApiDebugLevel, _SetApiDebugLevel,
    doc='''Queries/sets the debug level of the underlying API. Currently there are
    only two levels, 0 which means no debug information and 1 which means that the
    commands sent to / received from the Skype client are printed to the sys.stderr.
    
    @type: int
    ''')

    def _GetApiWrapperVersion(self):
        from Skype4Py import __version__
        return __version__

    ApiWrapperVersion = property(_GetApiWrapperVersion,
    doc='''Returns Skype4Py version.

    @type: str
    ''')

    def _GetAttachmentStatus(self):
        return self._API.attachment_status

    AttachmentStatus = property(_GetAttachmentStatus,
    doc='''Queries the attachment status of the Skype client.

    @type: L{Attachment status<enums.apiAttachUnknown>}
    ''')

    def _GetBookmarkedChats(self):
        return gen(Chat(x, self) for x in self._Search('BOOKMARKEDCHATS'))

    BookmarkedChats = property(_GetBookmarkedChats,
    doc='''Queries a list of bookmarked chats.

    @type: tuple of L{Chat}
    ''')

    def _GetCache(self):
        return self._Cache

    def _SetCache(self, Value):
        self._Cache = bool(Value)

    Cache = property(_GetCache, _SetCache,
    doc='''Queries/sets the status of internal cache. The internal API cache is used
    to cache Skype object properties and global parameters.

    @type: bool
    ''')

    def _GetChats(self):
        return gen(Chat(x, self) for x in self._Search('CHATS'))

    Chats = property(_GetChats,
    doc='''Queries a list of chats.

    @type: tuple of L{Chat}
    ''')

    def _GetClient(self):
        return self._Client

    Client = property(_GetClient,
    doc='''Queries the user interface control object.

    @type: L{Client}
    ''')

    def _GetCommandId(self):
        return True

    def _SetCommandId(self, Value):
        pass

    CommandId = property(_GetCommandId, _SetCommandId,
    doc='''Queries/sets the status of automatic command identifiers.

    Type: bool
    Note: Currently it is always True.

    @type: bool
    ''')

    def _GetConferences(self):
        for c in self.Calls():
            cid = c.ConferenceId
            if cid > 0 and cid not in [x.Id for x in confs]:
                yield Conference(cid, self)

    Conferences = property(lambda self: gen(self._GetConferences()),
    doc='''Queries a list of call conferences.

    @type: tuple of L{Conference}
    ''')

    def _GetConnectionStatus(self):
        return self.Variable('CONNSTATUS')

    ConnectionStatus = property(_GetConnectionStatus,
    doc='''Queries the connection status of the Skype client.

    @type: L{Connection status<enums.conUnknown>}
    ''')

    def _GetConvert(self):
        return self._Convert

    Convert = property(_GetConvert,
    doc='''Queries the conversion object.

    @type: L{Conversion}
    ''')

    def _GetCurrentUser(self):
        return User(self.CurrentUserHandle, self)

    CurrentUser = property(_GetCurrentUser,
    doc='''Queries the current user object.

    @type: L{User}
    ''')

    def _GetCurrentUserHandle(self):
        return str(self.Variable('CURRENTUSERHANDLE'))

    CurrentUserHandle = property(_GetCurrentUserHandle,
    doc='''Queries the Skypename of the current user.

    @type: str
    ''')

    def _GetCurrentUserProfile(self):
        return self._Profile

    CurrentUserProfile = property(_GetCurrentUserProfile,
    doc='''Queries the user profile object.

    @type: L{Profile}
    ''')

    def _GetCurrentUserStatus(self):
        return str(self.Variable('USERSTATUS'))

    def _SetCurrentUserStatus(self, Value):
        self.Variable('USERSTATUS', str(Value))

    CurrentUserStatus = property(_GetCurrentUserStatus, _SetCurrentUserStatus,
    doc='''Queries/sets the online status of the current user.

    @type: L{Online status<enums.olsUnknown>}
    ''')

    def _GetCustomGroups(self):
        return gen(Group(x, self) for x in self._Search('GROUPS', 'CUSTOM'))

    CustomGroups = property(_GetCustomGroups,
    doc='''Queries the list of custom contact groups. Custom groups are contact groups defined by the user.

    @type: tuple of L{Group}
    ''')

    def _GetFileTransfers(self):
        return gen(FileTransfer(x, self) for x in self._Search('FILETRANSFERS'))

    FileTransfers = property(_GetFileTransfers,
    doc='''Queries all file transfers.

    @type: tuple of L{FileTransfer}
    ''')

    def _GetFocusedContacts(self):
        # we have to use _DoCommand() directly because for unknown reason the API returns
        # "CONTACTS FOCUSED" instead of "CONTACTS_FOCUSED" (note the space instead of "_")
        return gen(User(x, self) for x in split(chop(self._DoCommand('GET CONTACTS_FOCUSED', 'CONTACTS FOCUSED'), 2)[-1]))

    FocusedContacts = property(_GetFocusedContacts,
    doc='''Queries a list of contacts selected in the contacts list.

    @type: tuple of L{User}
    ''')

    def _GetFriendlyName(self):
        return self._API.friendly_name

    def _SetFriendlyName(self, Value):
        self._API.set_friendly_name(tounicode(Value))

    FriendlyName = property(_GetFriendlyName, _SetFriendlyName,
    doc='''Queries/sets a "friendly" name for an application.

    @type: unicode
    ''')

    def _GetFriends(self):
        return gen(User(x, self) for x in self._Search('FRIENDS'))

    Friends = property(_GetFriends,
    doc='''Queries the users in a contact list.

    @type: tuple of L{User}
    ''')

    def _GetGroups(self):
        return gen(Group(x, self) for x in self._Search('GROUPS', 'ALL'))

    Groups = property(_GetGroups,
    doc='''Queries the list of all contact groups.

    @type: tuple of L{Group}
    ''')

    def _GetHardwiredGroups(self):
        return gen(Group(x, self) for x in self._Search('GROUPS', 'HARDWIRED'))

    HardwiredGroups = property(_GetHardwiredGroups,
    doc='''Queries the list of hardwired contact groups. Hardwired groups are "smart" contact groups,
    defined by Skype, that cannot be removed.

    @type: tuple of L{Group}
    ''')

    def _GetMissedCalls(self):
        return gen(Call(x, self) for x in self._Search('MISSEDCALLS'))

    MissedCalls = property(_GetMissedCalls,
    doc='''Queries a list of missed calls.

    @type: tuple of L{Call}
    ''')

    def _GetMissedChats(self):
        return gen(Chat(x, self) for x in self._Search('MISSEDCHATS'))

    MissedChats = property(_GetMissedChats,
    doc='''Queries a list of missed chats.

    @type: tuple of L{Chat}
    ''')

    def _GetMissedMessages(self):
        return gen(ChatMessage(x, self) for x in self._Search('MISSEDCHATMESSAGES'))

    MissedMessages = property(_GetMissedMessages,
    doc='''Queries a list of missed chat messages.

    @type: L{ChatMessage}
    ''')

    def _GetMissedSmss(self):
        return gen(SmsMessage(x, self) for x in self._Search('MISSEDSMSS'))

    MissedSmss = property(_GetMissedSmss,
    doc='''Requests a list of all missed SMS messages.

    @type: tuple of L{SmsMessage}
    ''')

    def _GetMissedVoicemails(self):
        return gen(Voicemail(x, self) for x in self._Search('MISSEDVOICEMAILS'))

    MissedVoicemails = property(_GetMissedVoicemails,
    doc='''Requests a list of missed voicemails.

    @type: L{Voicemail}
    ''')

    def _GetMute(self):
        return self.Variable('MUTE') == 'ON'

    def _SetMute(self, Value):
        self.Variable('MUTE', cndexp(Value, 'ON', 'OFF'))

    Mute = property(_GetMute, _SetMute,
    doc='''Queries/sets the mute status of the Skype client.

    Type: bool
    Note: This value can be set only when there is an active call.

    @type: bool
    ''')

    def _GetPredictiveDialerCountry(self):
        return str(self.Variable('PREDICTIVE_DIALER_COUNTRY'))

    PredictiveDialerCountry = property(_GetPredictiveDialerCountry,
    doc='''Returns predictive dialer coutry as an ISO code.

    @type: unicode
    ''')

    def _GetProtocol(self):
        return self._API.protocol

    def _SetProtocol(self, Value):
        self._DoCommand('PROTOCOL %s' % Value)
        self._API.protocol = int(Value)

    Protocol = property(_GetProtocol, _SetProtocol,
    doc='''Queries/sets the protocol version used by the Skype client.

    @type: int
    ''')

    def _GetRecentChats(self):
        return gen(Chat(x, self) for x in self._Search('RECENTCHATS'))

    RecentChats = property(_GetRecentChats,
    doc='''Queries a list of recent chats.

    @type: tuple of L{Chat}
    ''')

    def _GetSettings(self):
        return self._Settings

    Settings = property(_GetSettings,
    doc='''Queries the settings for Skype general parameters.

    @type: L{Settings}
    ''')

    def _GetSilentMode(self):
        return self._Property('SILENT_MODE', '', '', Cache=False) == 'ON'

    def _SetSilentMode(self, Value):
        self._Property('SILENT_MODE', '', '', cndexp(Value, 'ON', 'OFF'), Cache=False)

    SilentMode = property(_GetSilentMode, _SetSilentMode,
    doc='''Returns/sets Skype silent mode status.

    @type: bool
    ''')

    def _GetSmss(self):
        return gen(SmsMessage(x, self) for x in self._Search('SMSS'))

    Smss = property(_GetSmss,
    doc='''Requests a list of all SMS messages.

    @type: tuple of L{SmsMessage}
    ''')

    def _GetTimeout(self):
        return self._Timeout

    def _SetTimeout(self, Value):
        if not isinstance(Value, (int, long, float)):
            raise TypeError('%s: wrong type, expected float (seconds), int or long (milliseconds)' %
                repr(type(Value)))
        self._Timeout = Value

    Timeout = property(_GetTimeout, _SetTimeout,
    doc='''Queries/sets the wait timeout value. This timeout value applies to every command sent
    to the Skype API and to attachment requests (see L{Attach}). If a response is not received
    during the timeout period, an L{SkypeAPIError} exception is raised.
    
    The units depend on the type. For float it is the number of seconds, for int or long
    it is the number of milliseconds. Floats are commonly used in Python modules to express
    timeouts (see time.sleep() for a basic example). Milliseconds are supported for backward
    compatibility. Skype4Py support for real float timeouts was introduced in version 1.0.31.1.

    The default value is 30000 milliseconds (int).

    @type: float, int or long
    ''')

    def _GetUsersWaitingAuthorization(self):
        return gen(User(x, self) for x in self._Search('USERSWAITINGMYAUTHORIZATION'))

    UsersWaitingAuthorization = property(_GetUsersWaitingAuthorization,
    doc='''Queries the list of users waiting for authorization.

    @type: tuple of L{User}
    ''')

    def _GetVersion(self):
        return str(self.Variable('SKYPEVERSION'))

    Version = property(_GetVersion,
    doc='''Queries the application version of the Skype client.

    @type: str
    ''')

    def _GetVoicemails(self):
        return gen(Voicemail(x, self) for x in self._Search('VOICEMAILS'))

    Voicemails = property(_GetVoicemails,
    doc='''Queries a list of voicemails.

    @type: L{Voicemail}
    ''')


class SkypeEvents(object):
    '''Events defined in L{Skype}.

    See L{EventHandlingBase} for more information on events.
    '''

    def ApplicationConnecting(self, App, Users):
        '''This event is triggered when list of users connecting to an application changes.

        @param App: Application object.
        @type App: L{Application}
        @param Users: Connecting users.
        @type Users: tuple of L{User}
        '''

    def ApplicationDatagram(self, App, Stream, Text):
        '''This event is caused by the arrival of an application datagram.

        @param App: Application object.
        @type App: L{Application}
        @param Stream: Application stream that received the datagram.
        @type Stream: L{ApplicationStream}
        @param Text: The datagram text.
        @type Text: unicode
        '''

    def ApplicationReceiving(self, App, Streams):
        '''This event is triggered when list of application receiving streams changes.

        @param App: Application object.
        @type App: L{Application}
        @param Streams: Application receiving streams.
        @type Streams: tuple of L{ApplicationStream}
        '''

    def ApplicationSending(self, App, Streams):
        '''This event is triggered when list of application sending streams changes.

        @param App: Application object.
        @type App: L{Application}
        @param Streams: Application sending streams.
        @type Streams: tuple of L{ApplicationStream}
        '''

    def ApplicationStreams(self, App, Streams):
        '''This event is triggered when list of application streams changes.

        @param App: Application object.
        @type App: L{Application}
        @param Streams: Application streams.
        @type Streams: tuple of L{ApplicationStream}
        '''

    def AsyncSearchUsersFinished(self, Cookie, Users):
        '''This event occurs when an asynchronous search is completed.

        @param Cookie: Search identifier as returned by L{Skype.AsyncSearchUsers}.
        @type Cookie: int
        @param Users: Found users.
        @type Users: tuple of L{User}
        @see: L{Skype.AsyncSearchUsers}
        '''

    def AttachmentStatus(self, Status):
        '''This event is caused by a change in the status of an attachment to the Skype API.

        @param Status: New attachment status.
        @type Status: L{Attachment status<enums.apiAttachUnknown>}
        '''

    def AutoAway(self, Automatic):
        '''This event is caused by a change of auto away status.

        @param Automatic: New auto away status.
        @type Automatic: bool
        '''

    def CallDtmfReceived(self, Call, Code):
        '''This event is caused by a call DTMF event.

        @param Call: Call object.
        @type Call: L{Call}
        @param Code: Received DTMF code.
        @type Code: str
        '''

    def CallHistory(self):
        '''This event is caused by a change in call history.
        '''

    def CallInputStatusChanged(self, Call, Active):
        '''This event is caused by a change in the Call voice input status change.

        @param Call: Call object.
        @type Call: L{Call}
        @param Active: New voice input status (active when True).
        @type Active: bool
        '''

    def CallSeenStatusChanged(self, Call, Seen):
        '''This event occurs when the seen status of a call changes.

        @param Call: Call object.
        @type Call: L{Call}
        @param Seen: True if call was seen.
        @type Seen: bool
        @see: L{Call.Seen}
        '''

    def CallStatus(self, Call, Status):
        '''This event is caused by a change in call status.

        @param Call: Call object.
        @type Call: L{Call}
        @param Status: New status of the call.
        @type Status: L{Call status<enums.clsUnknown>}
        '''

    def CallTransferStatusChanged(self, Call, Status):
        '''This event occurs when a call transfer status changes.

        @param Call: Call object.
        @type Call: L{Call}
        @param Status: New status of the call transfer.
        @type Status: L{Call status<enums.clsUnknown>}
        '''

    def CallVideoReceiveStatusChanged(self, Call, Status):
        '''This event occurs when a call video receive status changes.

        @param Call: Call object.
        @type Call: L{Call}
        @param Status: New video receive status of the call.
        @type Status: L{Call video send status<enums.vssUnknown>}
        '''

    def CallVideoSendStatusChanged(self, Call, Status):
        '''This event occurs when a call video send status changes.

        @param Call: Call object.
        @type Call: L{Call}
        @param Status: New video send status of the call.
        @type Status: L{Call video send status<enums.vssUnknown>}
        '''

    def CallVideoStatusChanged(self, Call, Status):
        '''This event occurs when a call video status changes.

        @param Call: Call object.
        @type Call: L{Call}
        @param Status: New video status of the call.
        @type Status: L{Call video status<enums.cvsUnknown>}
        '''

    def ChatMemberRoleChanged(self, Member, Role):
        '''This event occurs when a chat member role changes.

        @param Member: Chat member object.
        @type Member: L{ChatMember}
        @param Role: New member role.
        @type Role: L{Chat member role<enums.chatMemberRoleUnknown>}
        '''

    def ChatMembersChanged(self, Chat, Members):
        '''This event occurs when a list of chat members change.

        @param Chat: Chat object.
        @type Chat: L{Chat}
        @param Members: Chat members.
        @type Members: tuple of L{User}
        '''

    def ChatWindowState(self, Chat, State):
        '''This event occurs when chat window is opened or closed.

        @param Chat: Chat object.
        @type Chat: L{Chat}
        @param State: True if the window was opened or False if closed.
        @type State: bool
        '''

    def ClientWindowState(self, State):
        '''This event occurs when the state of the client window changes.

        @param State: New window state.
        @type State: L{Window state<enums.wndUnknown>}
        '''

    def Command(self, command):
        '''This event is triggered when a command is sent to the Skype API.

        @param command: Command object.
        @type command: L{Command}
        '''

    def ConnectionStatus(self, Status):
        '''This event is caused by a connection status change.

        @param Status: New connection status.
        @type Status: L{Connection status<enums.conUnknown>}
        '''

    def ContactsFocused(self, Username):
        '''This event is caused by a change in contacts focus.

        @param Username: Name of the user that was focused or empty string if focus was lost.
        @type Username: str
        '''

    def Error(self, command, Number, Description):
        '''This event is triggered when an error occurs during execution of an API command.

        @param command: Command object that caused the error.
        @type command: L{Command}
        @param Number: Error number returned by the Skype API.
        @type Number: int
        @param Description: Description of the error.
        @type Description: unicode
        '''

    def FileTransferStatusChanged(self, Transfer, Status):
        '''This event occurs when a file transfer status changes.

        @param Transfer: File transfer object.
        @type Transfer: L{FileTransfer}
        @param Status: New status of the file transfer.
        @type Status: L{File transfer status<enums.fileTransferStatusNew>}
        '''

    def GroupDeleted(self, GroupId):
        '''This event is caused by a user deleting a custom contact group.

        @param GroupId: Id of the deleted group.
        @type GroupId: int
        '''

    def GroupExpanded(self, Group, Expanded):
        '''This event is caused by a user expanding or collapsing a group in the contacts tab.

        @param Group: Group object.
        @type Group: L{Group}
        @param Expanded: Tells if the group is expanded (True) or collapsed (False).
        @type Expanded: bool
        '''

    def GroupUsers(self, Group, Users):
        '''This event is caused by a change in a contact group members.

        @param Group: Group object.
        @type Group: L{Group}
        @param Users: Group members.
        @type Users: tuple of L{User}
        '''

    def GroupVisible(self, Group, Visible):
        '''This event is caused by a user hiding/showing a group in the contacts tab.

        @param Group: Group object.
        @type Group: L{Group}
        @param Visible: Tells if the group is visible or not.
        @type Visible: bool
        '''

    def MessageHistory(self, Username):
        '''This event is caused by a change in message history.

        @param Username: Name of the user whose message history changed.
        @type Username: str
        '''

    def MessageStatus(self, Message, Status):
        '''This event is caused by a change in chat message status.

        @param Message: Chat message object.
        @type Message: L{ChatMessage}
        @param Status: New status of the chat message.
        @type Status: L{Chat message status<enums.cmsUnknown>}
        '''

    def Mute(self, Mute):
        '''This event is caused by a change in mute status.

        @param Mute: New mute status.
        @type Mute: bool
        '''

    def Notify(self, Notification):
        '''This event is triggered whenever Skype client sends a notification.

        @param Notification: Notification string.
        @type Notification: unicode
        @note: Use this event only if there is no dedicated one.
        '''

    def OnlineStatus(self, User, Status):
        '''This event is caused by a change in the online status of a user.

        @param User: User object.
        @type User: L{User}
        @param Status: New online status of the user.
        @type Status: L{Online status<enums.olsUnknown>}
        '''

    def PluginEventClicked(self, Event):
        '''This event occurs when a user clicks on a plug-in event.

        @param Event: Plugin event object.
        @type Event: L{PluginEvent}
        '''

    def PluginMenuItemClicked(self, MenuItem, Users, PluginContext, ContextId):
        '''This event occurs when a user clicks on a plug-in menu item.

        @param MenuItem: Menu item object.
        @type MenuItem: L{PluginMenuItem}
        @param Users: Users this item refers to.
        @type Users: tuple of L{User}
        @param PluginContext: Plug-in context.
        @type PluginContext: unicode
        @param ContextId: Context Id. Chat name for chat context or Call ID for call context.
        @type ContextId: str or int
        @see: L{PluginMenuItem}
        '''

    def Reply(self, command):
        '''This event is triggered when the API replies to a command object.

        @param command: Command object.
        @type command: L{Command}
        '''

    def SilentModeStatusChanged(self, Silent):
        '''This event occurs when a silent mode is switched off.
        
        @param Silent: Skype client silent status.
        @type Silent: bool
        '''

    def SmsMessageStatusChanged(self, Message, Status):
        '''This event is caused by a change in the SMS message status.

        @param Message: SMS message object.
        @type Message: L{SmsMessage}
        @param Status: New status of the SMS message.
        @type Status: L{SMS message status<enums.smsMessageStatusUnknown>}
        '''

    def SmsTargetStatusChanged(self, Target, Status):
        '''This event is caused by a change in the SMS target status.

        @param Target: SMS target object.
        @type Target: L{SmsTarget}
        @param Status: New status of the SMS target.
        @type Status: L{SMS target status<enums.smsTargetStatusUnknown>}
        '''

    def UserAuthorizationRequestReceived(self, User):
        '''This event occurs when user sends you an authorization request.

        @param User: User object.
        @type User: L{User}
        '''

    def UserMood(self, User, MoodText):
        '''This event is caused by a change in the mood text of the user.

        @param User: User object.
        @type User: L{User}
        @param MoodText: New mood text.
        @type MoodText: unicode
        '''

    def UserStatus(self, Status):
        '''This event is caused by a user status change.

        @param Status: New user status.
        @type Status: L{User status<enums.cusUnknown>}
        '''

    def VoicemailStatus(self, Mail, Status):
        '''This event is caused by a change in voicemail status.

        @param Mail: Voicemail object.
        @type Mail: L{Voicemail}
        @param Status: New status of the voicemail.
        @type Status: L{Voicemail status<enums.vmsUnknown>}
        '''

    def WallpaperChanged(self, Path):
        '''This event occurs when client wallpaper changes.

        @param Path: Path to new wallpaper bitmap.
        @type Path: str
        '''


Skype._AddEvents(SkypeEvents)
