'''Main Skype interface.
'''
__docformat__ = 'restructuredtext en'


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
    '''The main class which you have to instantiate to get access to the Skype client
    running currently in the background.

    1. Usage.

       You should access this class using the alias at the package level:

       .. python::
       
           import Skype4Py

           skype = Skype4Py.Skype()

       Read the constructor (`Skype.__init__`) documentation for a list of accepted
       arguments.

    2. Events.

       This class provides events.

       The events names and their arguments lists can be found in the `SkypeEvents`
       class in this module.

       The use of events is explained in the `EventHandlingBase` class
       which is a superclass of this class.
    '''

    def __init__(self, Events=None, **Options):
        '''Initializes the object.
        
        :Parameters:
          Events
            An optional object with event handlers. See `Skype4Py.utils.EventHandlingBase`
            for more information on events.
          Options
            Additional options for the low-level API handler. See the `Skype4Py.api`
            subpackage for supported options. Available options may depend on the
            current platform.
        '''
        EventHandlingBase.__init__(self)
        if Events:
            self._SetEventHandlerObj(Events)

        self._API = SkypeAPI(Options)
        self._API.register_handler(self._Handler)
        
        Cached._CreateOwner(self)

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
                    o = User(self, object_id)
                    if prop_name == 'ONLINESTATUS':
                        self._CallEventHandler('OnlineStatus', o, str(value))
                    elif prop_name == 'MOOD_TEXT' or prop_name == 'RICH_MOOD_TEXT':
                        self._CallEventHandler('UserMood', o, value)
                    elif prop_name == 'RECEIVEDAUTHREQUEST':
                        self._CallEventHandler('UserAuthorizationRequestReceived', o)
                elif object_type == 'CALL':
                    o = Call(self, object_id)
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
                    o = Chat(self, object_id)
                    if prop_name == 'MEMBERS':
                        self._CallEventHandler('ChatMembersChanged', o, gen(User(self, x) for x in split(value)))
                    if prop_name in ('OPENED', 'CLOSED'):
                        self._CallEventHandler('ChatWindowState', o, (prop_name == 'OPENED'))
                elif object_type == 'CHATMEMBER':
                    o = ChatMember(self, object_id)
                    if prop_name == 'ROLE':
                        self._CallEventHandler('ChatMemberRoleChanged', o, str(value))
                elif object_type == 'CHATMESSAGE':
                    o = ChatMessage(self, object_id)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('MessageStatus', o, str(value))
                elif object_type == 'APPLICATION':
                    o = Application(self, object_id)
                    if prop_name == 'CONNECTING':
                        self._CallEventHandler('ApplicationConnecting', o, gen(User(self, x) for x in split(value)))
                    elif prop_name == 'STREAMS':
                        self._CallEventHandler('ApplicationStreams', o, gen(ApplicationStream(o, x) for x in split(value)))
                    elif prop_name == 'DATAGRAM':
                        handle, text = chop(value)
                        self._CallEventHandler('ApplicationDatagram', o, ApplicationStream(o, handle), text)
                    elif prop_name == 'SENDING':
                        self._CallEventHandler('ApplicationSending', o, gen(ApplicationStream(o, x.split('=')[0]) for x in split(value)))
                    elif prop_name == 'RECEIVED':
                        self._CallEventHandler('ApplicationReceiving', o, gen(ApplicationStream(o, x.split('=')[0]) for x in split(value)))
                elif object_type == 'GROUP':
                    o = Group(self, object_id)
                    if prop_name == 'VISIBLE':
                        self._CallEventHandler('GroupVisible', o, (value == 'TRUE'))
                    elif prop_name == 'EXPANDED':
                        self._CallEventHandler('GroupExpanded', o, (value == 'TRUE'))
                    elif prop_name == 'USERS':
                        self._CallEventHandler('GroupUsers', o, gen(User(self, x) for x in split(value, ', ')))
                elif object_type == 'SMS':
                    o = SmsMessage(self, object_id)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('SmsMessageStatusChanged', o, str(value))
                    elif prop_name == 'TARGET_STATUSES':
                        for t in split(value, ', '):
                            number, status = t.split('=')
                            self._CallEventHandler('SmsTargetStatusChanged', SmsTarget(o, number), str(status))
                elif object_type == 'FILETRANSFER':
                    o = FileTransfer(self, object_id)
                    if prop_name == 'STATUS':
                        self._CallEventHandler('FileTransferStatusChanged', o, str(value))
                elif object_type == 'VOICEMAIL':
                    o = Voicemail(self, object_id)
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
                    self._CallEventHandler('PluginEventClicked', PluginEvent(self, object_id))
            elif a == 'MENU_ITEM':
                object_id, prop_name, value = chop(b, 2)
                if prop_name == 'CLICKED':
                    i = value.rfind('CONTEXT ')
                    if i >= 0:
                        context = chop(value[i+8:])[0]
                        users = ()
                        context_id = u''
                        if context in (pluginContextContact, pluginContextCall, pluginContextChat):
                            users = gen(User(self, x) for x in split(value[:i-1], ', '))
                        if context in (pluginContextCall, pluginContextChat):
                            j = value.rfind('CONTEXT_ID ')
                            if j >= 0:
                                context_id = str(chop(value[j+11:])[0])
                                if context == pluginContextCall:
                                    context_id = int(context_id)
                        self._CallEventHandler('PluginMenuItemClicked', PluginMenuItem(self, object_id), users, str(context), context_id)
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
        command = Command(Cmd, ExpectedReply, True, self.Timeout)
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
            value = unicode(Set)
            self._DoCommand('SET %s %s' % (jarg, value), jarg)
            if Cache and self._Cache:
                self._CacheDict[h] = value

    def _Alter(self, ObjectType, ObjectId, AlterName, Args=None, Reply=None):
        cmd = 'ALTER %s %s %s' % (str(ObjectType), str(ObjectId), str(AlterName))
        if Reply is None:
            Reply = cmd
        if Args is not None:
            cmd = '%s %s' % (cmd, tounicode(Args))
        reply = self._DoCommand(cmd, Reply)
        arg = cmd.split()
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
        cmd = 'SEARCH %s' % ObjectType
        if Args is not None:
            cmd = '%s %s' % (cmd, Args)
        # It is safe to do str() as none of the searchable objects use non-ascii chars.
        return split(chop(str(self._DoCommand(cmd)))[-1], ', ')

    def ApiSecurityContextEnabled(self, Context):
        '''Queries if an API security context for Internet Explorer is enabled.

        :Parameters:
          Context : unicode
            API security context to check.

        :return: True if the API security for the given context is enabled, False otherwise.
        :rtype: bool

        :warning: This functionality isn't supported by Skype4Py.
        '''
        self._API.security_context_enabled(Context)

    def Application(self, Name):
        '''Queries an application object.

        :Parameters:
          Name : unicode
            Application name.
            
        :return: The application object.
        :rtype: `application.Application`
        '''
        return Application(Name, self)

    def _AsyncSearchUsersReplyHandler(self, Command):
        if Command in self._AsyncSearchUsersCommands:
            self._AsyncSearchUsersCommands.remove(Command)
            self._CallEventHandler('AsyncSearchUsersFinished', Command.Id,
                gen(User(self, x) for x in split(chop(Command.Reply)[-1], ', ')))
            if len(self._AsyncSearchUsersCommands) == 0:
                self.UnregisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
                del self._AsyncSearchUsersCommands

    def AsyncSearchUsers(self, Target):
        '''Asynchronously searches for Skype users.

        :Parameters:
          Target : unicode
            Search target (name or email address).

        :return: A search identifier. It will be passed along with the results to the
                 `SkypeEvents.AsyncSearchUsersFinished` event after the search is completed.
        :rtype: int
        '''
        if not hasattr(self, '_AsyncSearchUsersCommands'):
            self._AsyncSearchUsersCommands = []
            self.RegisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
        command = Command('SEARCH USERS %s' % tounicode(Target), 'USERS', False, self.Timeout)
        self._AsyncSearchUsersCommands.append(command)
        self.SendCommand(command)
        # return pCookie - search identifier
        return command.Id

    def Attach(self, Protocol=5, Wait=True):
        '''Establishes a connection to Skype.

        :Parameters:
          Protocol : int
            Minimal Skype protocol version.
          Wait : bool
            If set to False, blocks forever until the connection is established. Otherwise, timeouts
            after the `Timeout`.
        '''
        try:
            self._API.protocol = Protocol
            self._API.attach(self.Timeout, Wait)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def Call(self, Id=0):
        '''Queries a call object.

        :Parameters:
          Id : int
            Call identifier.

        :return: Call object.
        :rtype: `call.Call`
        '''
        o = Call(self, Id)
        o.Status # Test if such a call exists.
        return o

    def Calls(self, Target=''):
        '''Queries calls in call history.

        :Parameters:
          Target : str
            Call target.

        :return: Call objects.
        :rtype: tuple of `call.Call`
        '''
        return gen(Call(self, x) for x in self._Search('CALLS', Target))

    def _ChangeUserStatus_UserStatus(self, Status):
        if Status.upper() == self._ChangeUserStatus_Status:
            self._ChangeUserStatus_Event.set()

    def ChangeUserStatus(self, Status):
        '''Changes the online status for the current user.

        :Parameters:
          Status : `enums`.cus*
            New online status for the user.

        :note: This function waits until the online status changes. Alternatively, use the
               `CurrentUserStatus` property to perform an immediate change of status.
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

        :Parameters:
          Name : str
            Chat name.

        :return: A chat object.
        :rtype: `chat.Chat`
        '''
        o = Chat(self, Name)
        o.Status # Tests if such a chat really exists.
        return o

    def ClearCallHistory(self, Username='ALL', Type=chsAllCalls):
        '''Clears the call history.

        :Parameters:
          Username : str
            Skypename of the user. A special value of 'ALL' means that entries of all users should
            be removed.
          Type : `enums`.clt*
            Call type.
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

        :Parameters:
          Command : unicode
            Command string.
          Reply : unicode
            Expected reply. By default any reply is accepted (except errors which raise an
            `SkypeError` exception).
          Block : bool
            If set to True, `SendCommand` method waits for a response from Skype API before
            returning.
          Timeout : int
            Timeout in milliseconds. Used if Block=True.
          Id : int
            Command Id. The default (-1) means it will be assigned automatically as soon as the
            command is sent.

        :return: A command object.
        :rtype: `Command`

        :see: `SendCommand`
        '''
        from API import Command as COMMAND
        return COMMAND(Command, Reply, Block, Timeout, Id)

    def Conference(self, Id=0):
        '''Queries a call conference object.

        :Parameters:
          Id : int
            Conference Id.

        :return: A conference object.
        :rtype: `Conference`
        '''
        o = Conference(self, Id)
        if Id <= 0 or not o.Calls:
            raise SkypeError(0, 'Unknown conference')
        return o

    def CreateChatUsingBlob(self, Blob):
        '''Returns existing or joins a new chat using given blob.

        :Parameters:
          Blob : str
            A blob identifying the chat.

        :return: A chat object
        :rtype: `chat.Chat`
        '''
        return Chat(self, chop(self._DoCommand('CHAT CREATEUSINGBLOB %s' % Blob), 2)[1])

    def CreateChatWith(self, *Usernames):
        '''Creates a chat with one or more users.

        :Parameters:
          Usernames : str
            One or more Skypenames of the users.

        :return: A chat object
        :rtype: `Chat`

        :see: `Chat.AddMembers`
        '''
        return Chat(self, chop(self._DoCommand('CHAT CREATE %s' % ', '.join(Usernames)), 2)[1])

    def CreateGroup(self, GroupName):
        '''Creates a custom contact group.

        :Parameters:
          GroupName : unicode
            Group name.

        :return: A group object.
        :rtype: `Group`

        :see: `DeleteGroup`
        '''
        groups = self.CustomGroups
        self._DoCommand('CREATE GROUP %s' % tounicode(GroupName))
        for g in self.CustomGroups:
            if g not in groups and g.DisplayName == GroupName:
                return g
        raise SkypeError(0, 'Group creating failed')

    def CreateSms(self, MessageType, *TargetNumbers):
        '''Creates an SMS message.

        :Parameters:
          MessageType : `enums`.smsMessageType*
            Message type.
          TargetNumbers : str
            One or more target SMS numbers.

        :return: An sms message object.
        :rtype: `SmsMessage`
        '''
        return SmsMessage(self, chop(self._DoCommand('CREATE SMS %s %s' % (MessageType, ', '.join(TargetNumbers))), 2)[1])

    def DeleteGroup(self, GroupId):
        '''Deletes a custom contact group.

        Users in the contact group are moved to the All Contacts (hardwired) contact group.

        :Parameters:
          GroupId : int
            Group identifier. Get it from `Group.Id`.

        :see: `CreateGroup`
        '''
        self._DoCommand('DELETE GROUP %s' % GroupId)

    def EnableApiSecurityContext(self, Context):
        '''Enables an API security context for Internet Explorer scripts.

        :Parameters:
          Context : unicode
            combination of API security context values.

        :warning: This functionality isn't supported by Skype4Py.
        '''
        self._API.enable_security_context(Context)

    def FindChatUsingBlob(self, Blob):
        '''Returns existing chat using given blob.

        :Parameters:
          Blob : str
            A blob identifying the chat.

        :return: A chat object
        :rtype: `chat.Chat`
        '''
        return Chat(self, chop(self._DoCommand('CHAT FINDUSINGBLOB %s' % Blob), 2)[1])

    def Greeting(self, Username=''):
        '''Queries the greeting used as voicemail.

        :Parameters:
          Username : str
            Skypename of the user.

        :return: A voicemail object.
        :rtype: `Voicemail`
        '''
        for v in self.Voicemails:
            if Username and v.PartnerHandle != Username:
                continue
            if v.Type in (vmtDefaultGreeting, vmtCustomGreeting):
                return v

    def Message(self, Id=0):
        '''Queries a chat message object.

        :Parameters:
          Id : int
            Message Id.

        :return: A chat message object.
        :rtype: `ChatMessage`
        '''
        o = ChatMessage(self, Id)
        o.Status # Test if such an id is known.
        return o

    def Messages(self, Target=''):
        '''Queries chat messages which were sent/received by the user.

        :Parameters:
          Target : str
            Message sender.

        :return: Chat message objects.
        :rtype: tuple of `ChatMessage`
        '''
        return gen(ChatMessage(self, x) for x in self._Search('CHATMESSAGES', Target))

    def PlaceCall(self, *Targets):
        '''Places a call to a single user or creates a conference call.

        :Parameters:
          Targets : str
            One or more call targets. If multiple targets are specified, a conference call is
            created. The call target can be a Skypename, phone number, or speed dial code.

        :return: A call object.
        :rtype: `call.Call`
        '''
        calls = self.ActiveCalls
        reply = self._DoCommand('CALL %s' % ', '.join(Targets))
        # Skype for Windows returns the call status which gives us the call Id;
        if reply.startswith('CALL '):
            return Call(self, chop(reply, 2)[1])
        # On linux we get 'OK' as reply so we search for the new call on
        # list of active calls.
        for c in self.ActiveCalls:
            if c not in calls:
                return c
        raise SkypeError(0, 'Placing call failed')

    def Privilege(self, Name):
        '''Queries the Skype services (privileges) enabled for the Skype client.

        :Parameters:
          Name : str
            Privilege name, currently one of 'SKYPEOUT', 'SKYPEIN', 'VOICEMAIL'.

        :return: True if the privilege is available, False otherwise.
        :rtype: bool
        '''
        return (self._Property('PRIVILEGE', '', Name.upper()) == 'TRUE')

    def Profile(self, Property, Set=None):
        '''Queries/sets user profile properties.

        :Parameters:
          Property : str
            Property name, currently one of 'PSTN_BALANCE', 'PSTN_BALANCE_CURRENCY', 'FULLNAME',
            'BIRTHDAY', 'SEX', 'LANGUAGES', 'COUNTRY', 'PROVINCE', 'CITY', 'PHONE_HOME',
            'PHONE_OFFICE', 'PHONE_MOBILE', 'HOMEPAGE', 'ABOUT'.
          Set : unicode or None
            Value the property should be set to or None if the value should be queried.

        :return: Property value if Set=None, None otherwise.
        :rtype: unicode or None
        '''
        return self._Property('PROFILE', '', Property, Set)

    def Property(self, ObjectType, ObjectId, PropName, Set=None):
        '''Queries/sets the properties of an object.

        :Parameters:
          ObjectType : str
            Object type ('USER', 'CALL', 'CHAT', 'CHATMESSAGE', ...).
          ObjectId : str
            Object Id, depends on the object type.
          PropName : str
            Name of the property to access.
          Set : unicode or None
            Value the property should be set to or None if the value should be queried.

        :return: Property value if Set=None, None otherwise.
        :rtype: unicode or None
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

        :Parameters:
          Target : unicode
            Search target (name or email address).

        :return: Found users.
        :rtype: tuple of `user.User`
        '''
        return gen(User(self, x) for x in self._Search('USERS', tounicode(Target)))

    def SendCommand(self, Command):
        '''Sends an API command.

        :Parameters:
          Command : `Command`
            Command to send. Use `Command` method to create a command.
        '''
        try:
            self._API.send_command(Command)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def SendMessage(self, Username, Text):
        '''Sends a chat message.

        :Parameters:
          Username : str
            Skypename of the user.
          Text : unicode
            Body of the message.

        :return: A chat message object.
        :rtype: `ChatMessage`
        '''
        return self.CreateChatWith(Username).SendMessage(Text)

    def SendSms(self, *TargetNumbers, **Properties):
        '''Creates and sends an SMS message.

        :Parameters:
          TargetNumbers : str
            One or more target SMS numbers.
          Properties
            Message properties. Properties available are same as `SmsMessage` object properties.

        :return: An sms message object. The message is already sent at this point.
        :rtype: `SmsMessage`
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

        :Parameters:
          Username : str
            Skypename of the user.

        :return: A voicemail object.
        :rtype: `Voicemail`
        '''
        if self._API.protocol >= 6:
            self._DoCommand('CALLVOICEMAIL %s' % Username)
        else:
            self._DoCommand('VOICEMAIL %s' % Username)

    def User(self, Username=''):
        '''Queries a user object.

        :Parameters:
          Username : str
            Skypename of the user.

        :return: A user object.
        :rtype: `user.User`
        '''
        o = User(self, Username)
        o.OnlineStatus # Test if such a user exists.
        return o

    def Variable(self, Name, Set=None):
        '''Queries/sets Skype general parameters.

        :Parameters:
          Name : str
            Variable name.
          Set : unicode or None
            Value the variable should be set to or None if the value should be queried.

        :return: Variable value if Set=None, None otherwise.
        :rtype: unicode or None
        '''
        return self._Property(Name, '', '', Set)

    def Voicemail(self, Id):
        '''Queries the voicemail object.

        :Parameters:
          Id : int
            Voicemail Id.

        :return: A voicemail object.
        :rtype: `Voicemail`
        '''
        o = Voicemail(self, Id)
        o.Type # Test if such a voicemail exists.
        return o

    def _GetActiveCalls(self):
        return gen(Call(self, x) for x in self._Search('ACTIVECALLS'))

    ActiveCalls = property(_GetActiveCalls,
    doc='''Queries a list of active calls.

    :type: tuple of `call.Call`
    ''')

    def _GetActiveChats(self):
        return gen(Chat(self, x) for x in self._Search('ACTIVECHATS'))

    ActiveChats = property(_GetActiveChats,
    doc='''Queries a list of active chats.

    :type: tuple of `chat.Chat`
    ''')

    def _GetActiveFileTransfers(self):
        return gen(FileTransfer(self, x) for x in self._Search('ACTIVEFILETRANSFERS'))

    ActiveFileTransfers = property(_GetActiveFileTransfers,
    doc='''Queries currently active file transfers.

    :type: tuple of `FileTransfer`
    ''')

    def _GetApiDebugLevel(self):
        return self._API.debug_level

    def _SetApiDebugLevel(self, Value):
        self._API.set_debug_level(int(Value))

    ApiDebugLevel = property(_GetApiDebugLevel, _SetApiDebugLevel,
    doc='''Queries/sets the debug level of the underlying API. Currently there are
    only two levels, 0 which means no debug information and 1 which means that the
    commands sent to / received from the Skype client are printed to the sys.stderr.

    :type: int
    ''')

    def _GetApiWrapperVersion(self):
        from Skype4Py import __version__
        return __version__

    ApiWrapperVersion = property(_GetApiWrapperVersion,
    doc='''Returns Skype4Py version.

    :type: str
    ''')

    def _GetAttachmentStatus(self):
        return self._API.attachment_status

    AttachmentStatus = property(_GetAttachmentStatus,
    doc='''Queries the attachment status of the Skype client.

    :type: `enums`.apiAttach*
    ''')

    def _GetBookmarkedChats(self):
        return gen(Chat(self, x) for x in self._Search('BOOKMARKEDCHATS'))

    BookmarkedChats = property(_GetBookmarkedChats,
    doc='''Queries a list of bookmarked chats.

    :type: tuple of `chat.Chat`
    ''')

    def _GetCache(self):
        return self._Cache

    def _SetCache(self, Value):
        self._Cache = bool(Value)

    Cache = property(_GetCache, _SetCache,
    doc='''Queries/sets the status of internal cache. The internal API cache is used
    to cache Skype object properties and global parameters.

    :type: bool
    ''')

    def _GetChats(self):
        return gen(Chat(self, x) for x in self._Search('CHATS'))

    Chats = property(_GetChats,
    doc='''Queries a list of chats.

    :type: tuple of `chat.Chat`
    ''')

    def _GetClient(self):
        return self._Client

    Client = property(_GetClient,
    doc='''Queries the user interface control object.

    :type: `Client`
    ''')

    def _GetCommandId(self):
        return True

    def _SetCommandId(self, Value):
        pass

    CommandId = property(_GetCommandId, _SetCommandId,
    doc='''Queries/sets the status of automatic command identifiers.

    :type: bool

    :note: Currently it is always True.
    ''')

    def _GetConferences(self):
        for c in self.Calls():
            cid = c.ConferenceId
            if cid > 0 and cid not in [x.Id for x in confs]:
                yield Conference(self, cid)

    Conferences = property(lambda self: gen(self._GetConferences()),
    doc='''Queries a list of call conferences.

    :type: tuple of `Conference`
    ''')

    def _GetConnectionStatus(self):
        return self.Variable('CONNSTATUS')

    ConnectionStatus = property(_GetConnectionStatus,
    doc='''Queries the connection status of the Skype client.

    :type: `enums`.con*
    ''')

    def _GetConvert(self):
        return self._Convert

    Convert = property(_GetConvert,
    doc='''Queries the conversion object.

    :type: `Conversion`
    ''')

    def _GetCurrentUser(self):
        return User(self, self.CurrentUserHandle)

    CurrentUser = property(_GetCurrentUser,
    doc='''Queries the current user object.

    :type: `user.User`
    ''')

    def _GetCurrentUserHandle(self):
        return str(self.Variable('CURRENTUSERHANDLE'))

    CurrentUserHandle = property(_GetCurrentUserHandle,
    doc='''Queries the Skypename of the current user.

    :type: str
    ''')

    def _GetCurrentUserProfile(self):
        return self._Profile

    CurrentUserProfile = property(_GetCurrentUserProfile,
    doc='''Queries the user profile object.

    :type: `Profile`
    ''')

    def _GetCurrentUserStatus(self):
        return str(self.Variable('USERSTATUS'))

    def _SetCurrentUserStatus(self, Value):
        self.Variable('USERSTATUS', str(Value))

    CurrentUserStatus = property(_GetCurrentUserStatus, _SetCurrentUserStatus,
    doc='''Queries/sets the online status of the current user.

    :type: `enums`.ols*
    ''')

    def _GetCustomGroups(self):
        return gen(Group(self, x) for x in self._Search('GROUPS', 'CUSTOM'))

    CustomGroups = property(_GetCustomGroups,
    doc='''Queries the list of custom contact groups. Custom groups are contact groups defined by the user.

    :type: tuple of `Group`
    ''')

    def _GetFileTransfers(self):
        return gen(FileTransfer(self, x) for x in self._Search('FILETRANSFERS'))

    FileTransfers = property(_GetFileTransfers,
    doc='''Queries all file transfers.

    :type: tuple of `FileTransfer`
    ''')

    def _GetFocusedContacts(self):
        # we have to use _DoCommand() directly because for unknown reason the API returns
        # "CONTACTS FOCUSED" instead of "CONTACTS_FOCUSED" (note the space instead of "_")
        return gen(User(self, x) for x in split(chop(self._DoCommand('GET CONTACTS_FOCUSED', 'CONTACTS FOCUSED'), 2)[-1]))

    FocusedContacts = property(_GetFocusedContacts,
    doc='''Queries a list of contacts selected in the contacts list.

    :type: tuple of `user.User`
    ''')

    def _GetFriendlyName(self):
        return self._API.friendly_name

    def _SetFriendlyName(self, Value):
        self._API.set_friendly_name(tounicode(Value))

    FriendlyName = property(_GetFriendlyName, _SetFriendlyName,
    doc='''Queries/sets a "friendly" name for an application.

    :type: unicode
    ''')

    def _GetFriends(self):
        return gen(User(self, x) for x in self._Search('FRIENDS'))

    Friends = property(_GetFriends,
    doc='''Queries the users in a contact list.

    :type: tuple of `user.User`
    ''')

    def _GetGroups(self):
        return gen(Group(self, x) for x in self._Search('GROUPS', 'ALL'))

    Groups = property(_GetGroups,
    doc='''Queries the list of all contact groups.

    :type: tuple of `Group`
    ''')

    def _GetHardwiredGroups(self):
        return gen(Group(self, x) for x in self._Search('GROUPS', 'HARDWIRED'))

    HardwiredGroups = property(_GetHardwiredGroups,
    doc='''Queries the list of hardwired contact groups. Hardwired groups are "smart" contact groups,
    defined by Skype, that cannot be removed.

    :type: tuple of `Group`
    ''')

    def _GetMissedCalls(self):
        return gen(Call(self, x) for x in self._Search('MISSEDCALLS'))

    MissedCalls = property(_GetMissedCalls,
    doc='''Queries a list of missed calls.

    :type: tuple of `call.Call`
    ''')

    def _GetMissedChats(self):
        return gen(Chat(self, x) for x in self._Search('MISSEDCHATS'))

    MissedChats = property(_GetMissedChats,
    doc='''Queries a list of missed chats.

    :type: tuple of `chat.Chat`
    ''')

    def _GetMissedMessages(self):
        return gen(ChatMessage(self, x) for x in self._Search('MISSEDCHATMESSAGES'))

    MissedMessages = property(_GetMissedMessages,
    doc='''Queries a list of missed chat messages.

    :type: `ChatMessage`
    ''')

    def _GetMissedSmss(self):
        return gen(SmsMessage(self, x) for x in self._Search('MISSEDSMSS'))

    MissedSmss = property(_GetMissedSmss,
    doc='''Requests a list of all missed SMS messages.

    :type: tuple of `SmsMessage`
    ''')

    def _GetMissedVoicemails(self):
        return gen(Voicemail(self, x) for x in self._Search('MISSEDVOICEMAILS'))

    MissedVoicemails = property(_GetMissedVoicemails,
    doc='''Requests a list of missed voicemails.

    :type: `Voicemail`
    ''')

    def _GetMute(self):
        return self.Variable('MUTE') == 'ON'

    def _SetMute(self, Value):
        self.Variable('MUTE', cndexp(Value, 'ON', 'OFF'))

    Mute = property(_GetMute, _SetMute,
    doc='''Queries/sets the mute status of the Skype client.

    Type: bool
    Note: This value can be set only when there is an active call.

    :type: bool
    ''')

    def _GetPredictiveDialerCountry(self):
        return str(self.Variable('PREDICTIVE_DIALER_COUNTRY'))

    PredictiveDialerCountry = property(_GetPredictiveDialerCountry,
    doc='''Returns predictive dialler country as an ISO code.

    :type: unicode
    ''')

    def _GetProtocol(self):
        return self._API.protocol

    def _SetProtocol(self, Value):
        self._DoCommand('PROTOCOL %s' % Value)
        self._API.protocol = int(Value)

    Protocol = property(_GetProtocol, _SetProtocol,
    doc='''Queries/sets the protocol version used by the Skype client.

    :type: int
    ''')

    def _GetRecentChats(self):
        return gen(Chat(self, x) for x in self._Search('RECENTCHATS'))

    RecentChats = property(_GetRecentChats,
    doc='''Queries a list of recent chats.

    :type: tuple of `chat.Chat`
    ''')

    def _GetSettings(self):
        return self._Settings

    Settings = property(_GetSettings,
    doc='''Queries the settings for Skype general parameters.

    :type: `Settings`
    ''')

    def _GetSilentMode(self):
        return self._Property('SILENT_MODE', '', '', Cache=False) == 'ON'

    def _SetSilentMode(self, Value):
        self._Property('SILENT_MODE', '', '', cndexp(Value, 'ON', 'OFF'), Cache=False)

    SilentMode = property(_GetSilentMode, _SetSilentMode,
    doc='''Returns/sets Skype silent mode status.

    :type: bool
    ''')

    def _GetSmss(self):
        return gen(SmsMessage(self, x) for x in self._Search('SMSS'))

    Smss = property(_GetSmss,
    doc='''Requests a list of all SMS messages.

    :type: tuple of `SmsMessage`
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
    to the Skype API and to attachment requests (see `Attach`). If a response is not received
    during the timeout period, an `SkypeAPIError` exception is raised.
    
    The units depend on the type. For float it is the number of seconds, for int or long
    it is the number of milliseconds. Floats are commonly used in Python modules to express
    timeouts (see time.sleep() for a basic example). Milliseconds are supported for backward
    compatibility. Skype4Py support for real float timeouts was introduced in version 1.0.31.1.

    The default value is 30000 milliseconds (int).

    :type: float, int or long
    ''')

    def _GetUsersWaitingAuthorization(self):
        return gen(User(self, x) for x in self._Search('USERSWAITINGMYAUTHORIZATION'))

    UsersWaitingAuthorization = property(_GetUsersWaitingAuthorization,
    doc='''Queries the list of users waiting for authorization.

    :type: tuple of `user.User`
    ''')

    def _GetVersion(self):
        return str(self.Variable('SKYPEVERSION'))

    Version = property(_GetVersion,
    doc='''Queries the application version of the Skype client.

    :type: str
    ''')

    def _GetVoicemails(self):
        return gen(Voicemail(self, x) for x in self._Search('VOICEMAILS'))

    Voicemails = property(_GetVoicemails,
    doc='''Queries a list of voicemails.

    :type: `Voicemail`
    ''')


class SkypeEvents(object):
    '''Events defined in `Skype`.

    See `EventHandlingBase` for more information on events.
    '''

    def ApplicationConnecting(self, App, Users):
        '''This event is triggered when list of users connecting to an application changes.

        :Parameters:
          App : `Application`
            Application object.
          Users : tuple of `User`
            Connecting users.
        '''

    def ApplicationDatagram(self, App, Stream, Text):
        '''This event is caused by the arrival of an application datagram.

        :Parameters:
          App : `Application`
            Application object.
          Stream : `ApplicationStream`
            Application stream that received the datagram.
          Text : unicode
            The datagram text.
        '''

    def ApplicationReceiving(self, App, Streams):
        '''This event is triggered when list of application receiving streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : tuple of `ApplicationStream`
            Application receiving streams.
        '''

    def ApplicationSending(self, App, Streams):
        '''This event is triggered when list of application sending streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : tuple of `ApplicationStream`
            Application sending streams.
        '''

    def ApplicationStreams(self, App, Streams):
        '''This event is triggered when list of application streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : tuple of `ApplicationStream`
            Application streams.
        '''

    def AsyncSearchUsersFinished(self, Cookie, Users):
        '''This event occurs when an asynchronous search is completed.

        :Parameters:
          Cookie : int
            Search identifier as returned by `Skype.AsyncSearchUsers`.
          Users : tuple of `User`
            Found users.

        :see: `Skype.AsyncSearchUsers`
        '''

    def AttachmentStatus(self, Status):
        '''This event is caused by a change in the status of an attachment to the Skype API.

        :Parameters:
          Status : `enums`.apiAttach*
            New attachment status.
        '''

    def AutoAway(self, Automatic):
        '''This event is caused by a change of auto away status.

        :Parameters:
          Automatic : bool
            New auto away status.
        '''

    def CallDtmfReceived(self, Call, Code):
        '''This event is caused by a call DTMF event.

        :Parameters:
          Call : `Call`
            Call object.
          Code : str
            Received DTMF code.
        '''

    def CallHistory(self):
        '''This event is caused by a change in call history.
        '''

    def CallInputStatusChanged(self, Call, Active):
        '''This event is caused by a change in the Call voice input status change.

        :Parameters:
          Call : `Call`
            Call object.
          Active : bool
            New voice input status (active when True).
        '''

    def CallSeenStatusChanged(self, Call, Seen):
        '''This event occurs when the seen status of a call changes.

        :Parameters:
          Call : `Call`
            Call object.
          Seen : bool
            True if call was seen.

        :see: `Call.Seen`
        '''

    def CallStatus(self, Call, Status):
        '''This event is caused by a change in call status.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cls*
            New status of the call.
        '''

    def CallTransferStatusChanged(self, Call, Status):
        '''This event occurs when a call transfer status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cls*
            New status of the call transfer.
        '''

    def CallVideoReceiveStatusChanged(self, Call, Status):
        '''This event occurs when a call video receive status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.vss*
            New video receive status of the call.
        '''

    def CallVideoSendStatusChanged(self, Call, Status):
        '''This event occurs when a call video send status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.vss*
            New video send status of the call.
        '''

    def CallVideoStatusChanged(self, Call, Status):
        '''This event occurs when a call video status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cvs*
            New video status of the call.
        '''

    def ChatMemberRoleChanged(self, Member, Role):
        '''This event occurs when a chat member role changes.

        :Parameters:
          Member : `ChatMember`
            Chat member object.
          Role : `enums`.chatMemberRole*
            New member role.
        '''

    def ChatMembersChanged(self, Chat, Members):
        '''This event occurs when a list of chat members change.

        :Parameters:
          Chat : `Chat`
            Chat object.
          Members : tuple of `User`
            Chat members.
        '''

    def ChatWindowState(self, Chat, State):
        '''This event occurs when chat window is opened or closed.

        :Parameters:
          Chat : `Chat`
            Chat object.
          State : bool
            True if the window was opened or False if closed.
        '''

    def ClientWindowState(self, State):
        '''This event occurs when the state of the client window changes.

        :Parameters:
          State : `enums`.wnd*
            New window state.
        '''

    def Command(self, command):
        '''This event is triggered when a command is sent to the Skype API.

        :Parameters:
          command : `Command`
            Command object.
        '''

    def ConnectionStatus(self, Status):
        '''This event is caused by a connection status change.

        :Parameters:
          Status : `enums`.con*
            New connection status.
        '''

    def ContactsFocused(self, Username):
        '''This event is caused by a change in contacts focus.

        :Parameters:
          Username : str
            Name of the user that was focused or empty string if focus was lost.
        '''

    def Error(self, command, Number, Description):
        '''This event is triggered when an error occurs during execution of an API command.

        :Parameters:
          command : `Command`
            Command object that caused the error.
          Number : int
            Error number returned by the Skype API.
          Description : unicode
            Description of the error.
        '''

    def FileTransferStatusChanged(self, Transfer, Status):
        '''This event occurs when a file transfer status changes.

        :Parameters:
          Transfer : `FileTransfer`
            File transfer object.
          Status : `enums`.fileTransferStatus*
            New status of the file transfer.
        '''

    def GroupDeleted(self, GroupId):
        '''This event is caused by a user deleting a custom contact group.

        :Parameters:
          GroupId : int
            Id of the deleted group.
        '''

    def GroupExpanded(self, Group, Expanded):
        '''This event is caused by a user expanding or collapsing a group in the contacts tab.

        :Parameters:
          Group : `Group`
            Group object.
          Expanded : bool
            Tells if the group is expanded (True) or collapsed (False).
        '''

    def GroupUsers(self, Group, Users):
        '''This event is caused by a change in a contact group members.

        :Parameters:
          Group : `Group`
            Group object.
          Users : tuple of `User`
            Group members.
        '''

    def GroupVisible(self, Group, Visible):
        '''This event is caused by a user hiding/showing a group in the contacts tab.

        :Parameters:
          Group : `Group`
            Group object.
          Visible : bool
            Tells if the group is visible or not.
        '''

    def MessageHistory(self, Username):
        '''This event is caused by a change in message history.

        :Parameters:
          Username : str
            Name of the user whose message history changed.
        '''

    def MessageStatus(self, Message, Status):
        '''This event is caused by a change in chat message status.

        :Parameters:
          Message : `ChatMessage`
            Chat message object.
          Status : `enums`.cms*
            New status of the chat message.
        '''

    def Mute(self, Mute):
        '''This event is caused by a change in mute status.

        :Parameters:
          Mute : bool
            New mute status.
        '''

    def Notify(self, Notification):
        '''This event is triggered whenever Skype client sends a notification.

        :Parameters:
          Notification : unicode
            Notification string.

        :note: Use this event only if there is no dedicated one.
        '''

    def OnlineStatus(self, User, Status):
        '''This event is caused by a change in the online status of a user.

        :Parameters:
          User : `User`
            User object.
          Status : `enums`.ols*
            New online status of the user.
        '''

    def PluginEventClicked(self, Event):
        '''This event occurs when a user clicks on a plug-in event.

        :Parameters:
          Event : `PluginEvent`
            Plugin event object.
        '''

    def PluginMenuItemClicked(self, MenuItem, Users, PluginContext, ContextId):
        '''This event occurs when a user clicks on a plug-in menu item.

        :Parameters:
          MenuItem : `PluginMenuItem`
            Menu item object.
          Users : tuple of `User`
            Users this item refers to.
          PluginContext : unicode
            Plug-in context.
          ContextId : str or int
            Context Id. Chat name for chat context or Call ID for call context.

        :see: `PluginMenuItem`
        '''

    def Reply(self, command):
        '''This event is triggered when the API replies to a command object.

        :Parameters:
          command : `Command`
            Command object.
        '''

    def SilentModeStatusChanged(self, Silent):
        '''This event occurs when a silent mode is switched off.

        :Parameters:
          Silent : bool
            Skype client silent status.
        '''

    def SmsMessageStatusChanged(self, Message, Status):
        '''This event is caused by a change in the SMS message status.

        :Parameters:
          Message : `SmsMessage`
            SMS message object.
          Status : `enums`.smsMessageStatus*
            New status of the SMS message.
        '''

    def SmsTargetStatusChanged(self, Target, Status):
        '''This event is caused by a change in the SMS target status.

        :Parameters:
          Target : `SmsTarget`
            SMS target object.
          Status : `enums`.smsTargetStatus*
            New status of the SMS target.
        '''

    def UserAuthorizationRequestReceived(self, User):
        '''This event occurs when user sends you an authorization request.

        :Parameters:
          User : `User`
            User object.
        '''

    def UserMood(self, User, MoodText):
        '''This event is caused by a change in the mood text of the user.

        :Parameters:
          User : `User`
            User object.
          MoodText : unicode
            New mood text.
        '''

    def UserStatus(self, Status):
        '''This event is caused by a user status change.

        :Parameters:
          Status : `enums`.cus*
            New user status.
        '''

    def VoicemailStatus(self, Mail, Status):
        '''This event is caused by a change in voicemail status.

        :Parameters:
          Mail : `Voicemail`
            Voicemail object.
          Status : `enums`.vms*
            New status of the voicemail.
        '''

    def WallpaperChanged(self, Path):
        '''This event occurs when client wallpaper changes.

        :Parameters:
          Path : str
            Path to new wallpaper bitmap.
        '''


Skype._AddEvents(SkypeEvents)
