'''Chats.
'''

from utils import *
from user import *
from enums import *
from errors import *


class IChat(Cached):
    '''Represents a Skype chat.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CHAT', self._Name, AlterName, Args, 'ALTER CHAT %s' % AlterName)

    def _Init(self, Name, Skype):
        self._Skype = Skype
        self._Name = Name

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHAT', self._Name, PropName, Value, Cache)

    def AcceptAdd(self):
        '''AcceptAdd.
        '''
        self._Alter('ACCEPTADD')

    def AddMembers(self, pMembers):
        '''Adds new members to the chat.

        @param pMembers: pMembers
        @type pMembers: ?
        '''
        self._Alter('ADDMEMBERS', ', '.join([x.Handle for x in pMembers]))

    def Bookmark(self):
        '''Bookmarks the chat.
        '''
        self._Alter('BOOKMARK')

    def ClearRecentMessages(self):
        '''ClearRecentMessages.
        '''
        self._Alter('CLEARRECENTMESSAGES')

    def Disband(self):
        '''Disband.
        '''
        self._Alter('DISBAND')

    def EnterPassword(self, Password):
        '''EnterPassword.

        @param Password: Password
        @type Password: ?
        '''
        self._Alter('ENTERPASSWORD', Password)

    def Join(self):
        '''Join.
        '''
        self._Alter('JOIN')

    def Kick(self, Handle):
        '''Kick.

        @param Handle: Handle
        @type Handle: unicode
        '''
        self._Alter('KICK', Handle)

    def KickBan(self, Handle):
        '''KickBan.

        @param Handle: Handle
        @type Handle: unicode
        '''
        self._Alter('KICKBAN', Handle)

    def Leave(self):
        '''Leaves the chat.
        '''
        self._Alter('LEAVE')

    def OpenWindow(self):
        '''Opens chat window.
        '''
        self._Skype._DoCommand('OPEN CHAT %s' % self._Name)

    def SendMessage(self, MessageText):
        '''Sends chat message.

        @param MessageText: MessageText
        @type MessageText: unicode
        @return: ?
        @rtype: ?
        '''
        msgs1 = self.RecentMessages
        self._Skype._DoCommand('CHATMESSAGE %s %s' % (self._Name, MessageText))
        msgs2 = self.RecentMessages
        for m in msgs2:
            if m not in msgs1:
                return m

    def SetPassword(self, Password, Hint=''):
        '''SetPassword.

        @param Password: Password
        @type Password: ?
        @param Hint: Hint
        @type Hint: ?
        '''
        self._Alter('SETPASSWORD', '%s %s' % (Password, Hint))

    def Unbookmark(self):
        '''Bookmarks the chat.
        '''
        self._Alter('UNBOOKMARK')

    def _GetActiveMembers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('ACTIVEMEMBERS', Cache=False)))

    ActiveMembers = property(_GetActiveMembers,
    doc='''ActiveMembers.

    @type: ?
    ''')

    def _GetActivityDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.ActivityTimestamp)

    ActivityDatetime = property(_GetActivityDatetime,
    doc='''ActivityDatetime.

    @type: datetime.datetime
    ''')

    def _GetActivityTimestamp(self):
        return float(self._Property('ACTIVITY_TIMESTAMP'))

    ActivityTimestamp = property(_GetActivityTimestamp,
    doc='''ActivityTimestamp.

    @type: float
    ''')

    def _GetAdder(self):
        return IUser(self._Property('ADDER'), self._Skype)

    Adder = property(_GetAdder,
    doc='''Adder.

    @type: ?
    ''')

    def _SetAlertString(self, value):
        self._Alter('SETALERTSTRING', quote('=%s' % value))

    AlertString = property(fset=_SetAlertString,
    doc='''AlertString.

    @type: ?
    ''')

    def _GetApplicants(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('APPLICANTS')))

    Applicants = property(_GetApplicants,
    doc='''Applicants.

    @type: ?
    ''')

    def _GetBlob(self):
        return self._Property('BLOB')

    Blob = property(_GetBlob,
    doc='''Blob.

    @type: ?
    ''')

    def _GetBookmarked(self):
        return self._Property('BOOKMARKED') == 'TRUE'

    Bookmarked = property(_GetBookmarked,
    doc='''Bookmarked.

    @type: ?
    ''')

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc='''Datetime.

    @type: datetime.datetime
    ''')

    def _GetDescription(self):
        return self._Property('DESCRIPTION')

    def _SetDescription(self, value):
        self._Property('DESCRIPTION', value)

    Description = property(_GetDescription, _SetDescription,
    doc='''Description.

    @type: ?
    ''')

    def _GetDialogPartner(self):
        return self._Property('DIALOG_PARTNER')

    DialogPartner = property(_GetDialogPartner,
    doc='''DialogPartner.

    @type: ?
    ''')

    def _GetFriendlyName(self):
        return self._Property('FRIENDLYNAME')

    FriendlyName = property(_GetFriendlyName,
    doc='''FriendlyName.

    @type: unicode
    ''')

    def _GetGuideLines(self):
        return self._Property('GUIDELINES')

    def _SetGuideLines(self, value):
        self._Alter('SETGUIDELINES', value)

    GuideLines = property(_GetGuideLines, _SetGuideLines,
    doc='''GuideLines.

    @type: ?
    ''')

    def _GetMemberObjects(self):
        return tuple(IChatMember(x, self._Skype) for x in esplit(self._Property('MEMBEROBJECTS'), ', '))

    MemberObjects = property(_GetMemberObjects,
    doc='''MemberObjects.

    @type: ?
    ''')

    def _GetMembers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('MEMBERS')))

    Members = property(_GetMembers,
    doc='''Members.

    @type: ?
    ''')

    def _GetMessages(self):
        return tuple(IChatMessage(x ,self._Skype) for x in esplit(self._Property('CHATMESSAGES', Cache=False), ', '))

    Messages = property(_GetMessages,
    doc='''Messages.

    @type: ?
    ''')

    def _GetMyRole(self):
        return self._Property('MYROLE')

    MyRole = property(_GetMyRole,
    doc='''MyRole.

    @type: ?
    ''')

    def _GetMyStatus(self):
        return self._Property('MYSTATUS')

    MyStatus = property(_GetMyStatus,
    doc='''MyStatus.

    @type: ?
    ''')

    def _GetName(self):
        return self._Name

    Name = property(_GetName,
    doc='''Name.

    @type: unicode
    ''')

    def _GetOptions(self):
        return int(self._Property('OPTIONS'))

    def _SetOptions(self, value):
        self._Alter('SETOPTIONS', value)

    Options = property(_GetOptions, _SetOptions,
    doc='''Options.

    @type: ?
    ''')

    def _GetPasswordHint(self):
        return self._Property('PASSWORDHINT')

    PasswordHint = property(_GetPasswordHint,
    doc='''PasswordHint.

    @type: ?
    ''')

    def _GetPosters(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('POSTERS')))

    Posters = property(_GetPosters,
    doc='''Posters.

    @type: ?
    ''')

    def _GetRecentMessages(self):
        return tuple(IChatMessage(x, self._Skype) for x in esplit(self._Property('RECENTCHATMESSAGES', Cache=False), ', '))

    RecentMessages = property(_GetRecentMessages,
    doc='''RecentMessages.

    @type: ?
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
    ''')

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc='''Timestamp.

    @type: float
    ''')

    def _GetTopic(self):
        try:
            topicxml = self._Property('TOPICXML')
            if topicxml:
                return topicxml
        except ISkypeError:
            pass
        return self._Property('TOPIC')

    def _SetTopic(self, value):
        try:
            self._Alter('SETTOPICXML', value)
        except ISkypeError:
            self._Alter('SETTOPIC', value)

    Topic = property(_GetTopic, _SetTopic,
    doc='''Topic.

    @type: ?
    ''')

    def _GetTopicXML(self):
        return self._Property('TOPICXML')

    def _SetTopicXML(self, value):
        self._Property('TOPICXML', value)

    TopicXML = property(_GetTopicXML, _SetTopicXML,
    doc='''TopicXML.

    @type: ?
    ''')

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType,
    doc='''Type.

    @type: ?
    ''')


class IChatMessage(Cached):
    '''Represents a single chat message.
    '''

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMESSAGE', self._Id, PropName, Value, Cache)

    def SetAsSeen(self):
        '''SetAsSeen.
        '''
        self._Property('SEEN', '')

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, value):
        self._Property('BODY', value)

    Body = property(_GetBody, _SetBody,
    doc='''Body.

    @type: ?
    ''')

    def _GetChat(self):
        return IChat(self.ChatName, self._Skype)

    Chat = property(_GetChat,
    doc='''Chat.

    @type: L{IChat}
    ''')

    def _GetChatName(self):
        return self._Property('CHATNAME')

    ChatName = property(_GetChatName,
    doc='''ChatName.

    @type: unicode
    ''')

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc='''Datetime.

    @type: datetime.datetime
    ''')

    def _GetFromDisplayName(self):
        return self._Property('FROM_DISPNAME')

    FromDisplayName = property(_GetFromDisplayName,
    doc='''FromDisplayName.

    @type: unicode
    ''')

    def _GetFromHandle(self):
        return self._Property('FROM_HANDLE')

    FromHandle = property(_GetFromHandle,
    doc='''FromHandle.

    @type: unicode
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: ?
    ''')

    def _GetLeaveReason(self):
        return self._Property('LEAVEREASON')

    LeaveReason = property(_GetLeaveReason,
    doc='''LeaveReason.

    @type: ?
    ''')

    def _SetSeen(self, value):
        from warnings import warn
        warn('IChat.Seen = x: Use IChat.SetAsSeen instead.', DeprecationWarning, stacklevel=2)
        if value:
            self.SetAsSeen()
        else:
            raise ISkypeError(0, 'Seen can only be set to True')

    Seen = property(fset=_SetSeen,
    doc='''Seen.

    @type: ?
    ''')

    def _GetSender(self):
        return IUser(self.FromHandle, self._Skype)

    Sender = property(_GetSender,
    doc='''Sender.

    @type: ?
    ''')

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus,
    doc='''Status.

    @type: ?
    ''')

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc='''Timestamp.

    @type: float
    ''')

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType,
    doc='''Type.

    @type: ?
    ''')

    def _GetUsers(self):
        return tuple(IUser(self._Skype, x) for x in esplit(self._Property('USERS')))

    Users = property(_GetUsers,
    doc='''Users.

    @type: tuple of L{IUser}
    ''')


class IChatMember(Cached):
    '''Represents a member of a public chat.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CHATMEMBER', self._Id, AlterName, Args, 'ALTER CHATMEMBER %s' % AlterName)

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMEMBER', self._Id, PropName, Value, Cache)

    def CanSetRoleTo(self, Role):
        '''CanSetRoleTo.

        @param Role: Role
        @type Role: ?
        @return: ?
        @rtype: ?
        '''
        return self._Alter('CANSETROLETO', Role) == 'TRUE'

    def _GetChat(self):
        return IChat(self._Property('CHATNAME'), self._Skype)

    Chat = property(_GetChat,
    doc='''Chat.

    @type: L{IChat}
    ''')

    def _GetHandle(self):
        return self._Property('IDENTITY')

    Handle = property(_GetHandle,
    doc='''Handle.

    @type: unicode
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: ?
    ''')

    def _GetIsActive(self):
        return self._Property('IS_ACTIVE') == 'TRUE'

    IsActive = property(_GetIsActive,
    doc='''IsActive.

    @type: bool
    ''')

    def _GetRole(self):
        return self._Property('ROLE')

    def _SetRole(self, value):
        self._Alter('SETROLETO', value)

    Role = property(_GetRole, _SetRole,
    doc='''Role.

    @type: ?
    ''')
