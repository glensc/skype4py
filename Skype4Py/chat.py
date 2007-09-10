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
        self._Alter('ADDMEMBERS', ', '.join(map(lambda x: x.Handle, pMembers)))

    def Bookmark(self):
        '''Bookmarks the chat.'''
        self._Alter('BOOKMARK')

    def Unbookmark(self):
        '''Bookmarks the chat.'''
        self._Alter('UNBOOKMARK')

    def _GetTopic(self):
        try:
            topicxml = self._Property('TOPICXML')
            if topicxml:
                return topicxml
        except ISkypeError:
            pass
        return self._Property('TOPIC')

    def _SetTopic(self, Topic):
        try:
            self._Alter('SETTOPICXML', Topic)
        except ISkypeError:
            self._Alter('SETTOPIC', Topic)

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

    Name = property(lambda self: self._Name)
    Bookmarked = property(lambda self: self._Property('BOOKMARKED') == 'TRUE')
    Timestamp = property(lambda self: float(self._Property('TIMESTAMP')))
    Adder = property(lambda self: IUser(self._Property('ADDER'), self._Skype))
    Status = property(lambda self: self._Property('STATUS'))
    Topic = property(_GetTopic, _SetTopic)
    FriendlyName = property(lambda self: self._Property('FRIENDLYNAME'))
    Posters = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('POSTERS'))))
    Members = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('MEMBERS'))))
    ActiveMembers = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('ACTIVEMEMBERS', Cache=False))))
    Messages = property(lambda self: map(lambda x: IChatMessage(x ,self._Skype), esplit(self._Property('CHATMESSAGES', Cache=False), ', ')))
    RecentMessages = property(lambda self: map(lambda x: IChatMessage(x, self._Skype), esplit(self._Property('RECENTCHATMESSAGES', Cache=False), ', ')))
    ActivityTimestamp = property(lambda self: float(self._Property('ACTIVITY_TIMESTAMP')))
    Applicants = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('APPLICANTS'))))
    Blob = property(lambda self: self._Property('BLOB'))
    Description = property(lambda self: self._Property('DESCRIPTION'),
                           lambda self, value: self._Property('DESCRIPTION', value))
    DialogPartner = property(lambda self: self._Property('DIALOG_PARTNER'))
    GuideLines = property(lambda self: self._Property('GUIDELINES'),
                          lambda self, value: self._Alter('SETGUIDELINES', value))
    MemberObjects = property(lambda self: map(lambda x: IChatMember(x, self._Skype), esplit(self._Property('MEMBEROBJECTS'), ', ')))
    MyRole = property(lambda self: self._Property('MYROLE'))
    MyStatus = property(lambda self: self._Property('MYSTATUS'))
    Options = property(lambda self: int(self._Property('OPTIONS')),
                       lambda self, value: self._Alter('SETOPTIONS', value))
    PasswordHint = property(lambda self: self._Property('PASSWORDHINT'))
    TopicXML = property(lambda self: self._Property('TOPICXML'),
                        lambda self, value: self._Property('TOPICXML', value))
    Type = property(lambda self: self._Property('TYPE'))
    AlertString = property(fset=lambda self, value: self._Alter('SETALERTSTRING', quote('=%s' % value)))


class IChatMessage(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMESSAGE', self._Id, PropName, Value, Cache)

    def _SetSeen(self, value):
        if value:
            self._Property('SEEN', '')
        else:
            raise ISkypeError(0, 'Seen can only be set to True')

    Id = property(lambda self: self._Id)
    Timestamp = property(lambda self: float(self._Property('TIMESTAMP')))
    FromHandle = property(lambda self: self._Property('FROM_HANDLE'))
    FromDisplayName = property(lambda self: self._Property('FROM_DISPNAME'))
    Type = property(lambda self: self._Property('TYPE'))
    Status = property(lambda self: self._Property('STATUS'))
    LeaveReason = property(lambda self: self._Property('LEAVEREASON'))
    Body = property(lambda self: self._Property('BODY'),
                    lambda self, value: self._Property('BODY', value))
    ChatName = property(lambda self: self._Property('CHATNAME'))
    Users = property(lambda self: map(lambda x: IUser(self._Skype, x), esplit(self._Property('USERS'))))
    Seen = property(fset=_SetSeen)
    Chat = property(lambda self: IChat(self.ChatName, self._Skype))
    Sender = property(lambda self: IUser(self.FromHandle, self._Skype))


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

    Id = property(lambda self: self._Id)
    Handle = property(lambda self: self._Property('IDENTITY'))
    Role = property(lambda self: self._Property('ROLE'),
                    lambda self, value: self._Alter('SETROLETO', value))
    IsActive = property(lambda self: self._Property('IS_ACTIVE') == 'TRUE')
    Chat = property(lambda self: IChat(self._Property('CHATNAME'), self._Skype))
