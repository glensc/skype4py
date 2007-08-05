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

    def _Alter(self, AlterName, Args=None, Reply=None):
        return self._Skype._Alter('CHAT', self._Name, AlterName, Args, Reply)

    def OpenWindow(self):
        self._Skype._DoCommand('OPEN CHAT %s' % self._Name)

    def SendMessage(self, MessageText):
        msgs1 = self.RecentMessages
        self._Skype._DoCommand('CHATMESSAGE %s %s' % (self._Name, MessageText))
        msgs2 = self.RecentMessages
        for m in msgs2:
            if m not in msgs1:
                return m

    def Leave(self):
        self._Alter('LEAVE')

    def AddMembers(self, pMembers):
        self._Alter('ADDMEMBERS', ', '.join(map(lambda x: x.Handle, pMembers)))

    def Bookmark(self):
        self._Alter('BOOKMARK', Reply='ALTER CHAT BOOKMARK')

    def Unbookmark(self):
        self._Alter('UNBOOKMARK', Reply='ALTER CHAT UNBOOKMARK')

    def _GetTopic(self):
        try:
            topicxml = self._Property('TOPICXML')
            if topicxml:
                return topicxml
        except SkypeError:
            pass
        return self._Property('TOPIC')

    def _SetTopic(self, Topic):
        try:
            self._Alter('SETTOPICXML', Topic, 'ALTER CHAT SETTOPICXML')
        except SkypeError:
            self._Alter('SETTOPIC', Topic, 'ALTER CHAT SETTOPIC')

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



class IChatMessage(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('CHATMESSAGE', self._Id, PropName, Value, Cache)

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
    Seen = property(lambda self: self._Property('SEEN') == 'TRUE', \
                    lambda self, value: self._Property('SEEN', 'TRUE' if value else 'FALSE'))
    Chat = property(lambda self: IChat(self.ChatName, self._Skype))
    Sender = property(lambda self: IUser(self.FromHandle, self._Skype))
