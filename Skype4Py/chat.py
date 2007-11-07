'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from user import *
from enums import *
from errors import *


class IChat(Cached):
    def _Init(self, Name, Skype):
        self._Skype = Skype
        self._Name = Name

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHAT', self._Name, PropName, Value, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CHAT', self._Name, AlterName, Args, 'ALTER CHAT %s' % AlterName)

    def OpenWindow(self):
        '''Opens chat window.'''
        self._Skype._DoCommand('OPEN CHAT %s' % self._Name)

    def SendMessage(self, MessageText):
        '''Sends chat message.'''
        msgs1 = self.RecentMessages
        self._Skype._DoCommand('CHATMESSAGE %s %s' % (self._Name, MessageText))
        msgs2 = self.RecentMessages
        for m in msgs2:
            if m not in msgs1:
                return m

    def Leave(self):
        '''Leaves the chat.'''
        self._Alter('LEAVE')

    def AddMembers(self, pMembers):
        '''Adds new members to the chat.'''
        self._Alter('ADDMEMBERS', ', '.join([x.Handle for x in pMembers]))

    def Bookmark(self):
        '''Bookmarks the chat.'''
        self._Alter('BOOKMARK')

    def Unbookmark(self):
        '''Bookmarks the chat.'''
        self._Alter('UNBOOKMARK')

    def AcceptAdd(self):
        self._Alter('ACCEPTADD')

    def ClearRecentMessages(self):
        self._Alter('CLEARRECENTMESSAGES')

    def Disband(self):
        self._Alter('DISBAND')

    def Join(self):
        self._Alter('JOIN')

    def Kick(self, Handle):
        self._Alter('KICK', Handle)

    def KickBan(self, Handle):
        self._Alter('KICKBAN', Handle)

    def EnterPassword(self, Password):
        self._Alter('ENTERPASSWORD', Password)

    def SetPassword(self, Password, Hint=''):
        self._Alter('SETPASSWORD', '%s %s' % (Password, Hint))

    def _GetName(self):
        return self._Name

    Name = property(_GetName)

    def _GetBookmarked(self):
        return self._Property('BOOKMARKED') == 'TRUE'

    Bookmarked = property(_GetBookmarked)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime)

    def _GetAdder(self):
        return IUser(self._Property('ADDER'), self._Skype)

    Adder = property(_GetAdder)

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus)

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

    Topic = property(_GetTopic, _SetTopic)

    def _GetFriendlyName(self):
        return self._Property('FRIENDLYNAME')

    FriendlyName = property(_GetFriendlyName)

    def _GetPosters(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('POSTERS')))

    Posters = property(_GetPosters)

    def _GetMembers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('MEMBERS')))

    Members = property(_GetMembers)

    def _GetActiveMembers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('ACTIVEMEMBERS', Cache=False)))

    ActiveMembers = property(_GetActiveMembers)

    def _GetMessages(self):
        return tuple(IChatMessage(x ,self._Skype) for x in esplit(self._Property('CHATMESSAGES', Cache=False), ', '))

    Messages = property(_GetMessages)

    def _GetRecentMessages(self):
        return tuple(IChatMessage(x, self._Skype) for x in esplit(self._Property('RECENTCHATMESSAGES', Cache=False), ', '))

    RecentMessages = property(_GetRecentMessages)

    def _GetActivityTimestamp(self):
        return float(self._Property('ACTIVITY_TIMESTAMP'))

    ActivityTimestamp = property(_GetActivityTimestamp)

    def _GetActivityDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.ActivityTimestamp)

    ActivityDatetime = property(_GetActivityDatetime)

    def _GetApplicants(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('APPLICANTS')))

    Applicants = property(_GetApplicants)

    def _GetBlob(self):
        return self._Property('BLOB')

    Blob = property(_GetBlob)

    def _GetDescription(self):
        return self._Property('DESCRIPTION')

    def _SetDescription(self, value):
        self._Property('DESCRIPTION', value)

    Description = property(_GetDescription, _SetDescription)

    def _GetDialogPartner(self):
        return self._Property('DIALOG_PARTNER')

    DialogPartner = property(_GetDialogPartner)

    def _GetGuideLines(self):
        return self._Property('GUIDELINES')

    def _SetGuideLines(self, value):
        self._Alter('SETGUIDELINES', value)

    GuideLines = property(_GetGuideLines, _SetGuideLines)

    def _GetMemberObjects(self):
        return tuple(IChatMember(x, self._Skype) for x in esplit(self._Property('MEMBEROBJECTS'), ', '))

    MemberObjects = property(_GetMemberObjects)

    def _GetMyRole(self):
        return self._Property('MYROLE')

    MyRole = property(_GetMyRole)

    def _GetMyStatus(self):
        return self._Property('MYSTATUS')

    MyStatus = property(_GetMyStatus)

    def _GetOptions(self):
        return int(self._Property('OPTIONS'))

    def _SetOptions(self, value):
        self._Alter('SETOPTIONS', value)

    Options = property(_GetOptions, _SetOptions)

    def _GetPasswordHint(self):
        return self._Property('PASSWORDHINT')

    PasswordHint = property(_GetPasswordHint)

    def _GetTopicXML(self):
        return self._Property('TOPICXML')

    def _SetTopicXML(self, value):
        self._Property('TOPICXML', value)

    TopicXML = property(_GetTopicXML, _SetTopicXML)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _SetAlertString(self, value):
        self._Alter('SETALERTSTRING', quote('=%s' % value))

    AlertString = property(fset=_SetAlertString)


class IChatMessage(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMESSAGE', self._Id, PropName, Value, Cache)

    def SetAsSeen(self):
        self._Property('SEEN', '')

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime)

    def _GetFromHandle(self):
        return self._Property('FROM_HANDLE')

    FromHandle = property(_GetFromHandle)

    def _GetFromDisplayName(self):
        return self._Property('FROM_DISPNAME')

    FromDisplayName = property(_GetFromDisplayName)

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType)

    def _GetStatus(self):
        return self._Property('STATUS')

    Status = property(_GetStatus)

    def _GetLeaveReason(self):
        return self._Property('LEAVEREASON')

    LeaveReason = property(_GetLeaveReason)

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, value):
        self._Property('BODY', value)

    Body = property(_GetBody, _SetBody)

    def _GetChatName(self):
        return self._Property('CHATNAME')

    ChatName = property(_GetChatName)

    def _GetUsers(self):
        return tuple(IUser(self._Skype, x) for x in esplit(self._Property('USERS')))

    Users = property(_GetUsers)

    def _SetSeen(self, value):
        from warnings import warn
        warn('IChat.Seen = x: Use IChat.SetAsSeen instead.', DeprecationWarning, stacklevel=2)
        if value:
            self.SetAsSeen()
        else:
            raise ISkypeError(0, 'Seen can only be set to True')

    Seen = property(fset=_SetSeen)

    def _GetChat(self):
        return IChat(self.ChatName, self._Skype)

    Chat = property(_GetChat)

    def _GetSender(self):
        return IUser(self.FromHandle, self._Skype)

    Sender = property(_GetSender)


class IChatMember(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMEMBER', self._Id, PropName, Value, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('CHATMEMBER', self._Id, AlterName, Args, 'ALTER CHATMEMBER %s' % AlterName)

    def CanSetRoleTo(self, Role):
        return self._Alter('CANSETROLETO', Role) == 'TRUE'

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetHandle(self):
        return self._Property('IDENTITY')

    Handle = property(_GetHandle)

    def _GetRole(self):
        return self._Property('ROLE')

    def _SetRole(self, value):
        self._Alter('SETROLETO', value)

    Role = property(_GetRole, _SetRole)

    def _GetIsActive(self):
        return self._Property('IS_ACTIVE') == 'TRUE'

    IsActive = property(_GetIsActive)

    def _GetChat(self):
        return IChat(self._Property('CHATNAME'), self._Skype)

    Chat = property(_GetChat)
