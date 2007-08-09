'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from user import *
import time


class IApplication(Cached):
    def _Init(self, Name, Skype):
        self._Name = unicode(Name)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('APPLICATION', self._Name, PropName, Set)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('APPLICATION', self._Name, AlterName, Args)

    def Create(self):
        self._Skype._DoCommand('CREATE APPLICATION %s' % self._Name)

    def Delete(self):
        self._Skype._DoCommand('DELETE APPLICATION %s' % self._Name)

    def Connect(self, Username, WaitConnected=False):
        self._Alter('CONNECT', Username)
        User = IUser(Username, self._Skype)
        if WaitConnected:
            while User in self.ConnectingUsers:
                time.sleep(0.01)
            for i in xrange(10):
                if Username not in map(lambda x: x.PartnerHandle, self.Streams):
                    time.sleep(0.01)

    def SendDatagram(self, Text, pStreams=None):
        if pStreams == None:
            pStreams = self.Streams
        for s in pStreams:
            s.SendDatagram(Text)

    Name = property(lambda self: self._Name)
    Streams = property(lambda self: map(lambda x: IApplicationStream(x, self), esplit(self._Property('STREAMS'))))
    ConnectableUsers = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('CONNECTABLE'))))
    ConnectingUsers = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(self._Property('CONNECTING'))))
    SendingStreams = property(lambda self: map(lambda x: IApplicationStream(x.split('=')[0], self), esplit(self._Property('SENDING'))))
    ReceivedStreams = property(lambda self: map(lambda x: IApplicationStream(x.split('=')[0], self), esplit(self._Property('RECEIVED'))))


class IApplicationStream(Cached):
    def _Init(self, Handle, Application):
        self._Handle = Handle
        self._Application = Application

    def Read(self):
        return self._Application._Alter('READ', self._Handle)

    def Write(self, Text):
        self._Application._Alter('WRITE', '%s %s' % (self._Handle, Text))

    def SendDatagram(self, Text):
        self._Application._Alter('DATAGRAM', '%s %s' % (self._Handle, Text))

    def Disconnect(self):
        self._Application._Alter('DISCONNECT', self._Handle)

    def _GetDataLength(self):
        def GetStreamLength(Type):
            for s in esplit(self._Application._Property(Type)):
                h, i = s.split('=')
                if h == self._Handle:
                    return int(i)
        i = GetStreamLength('SENDING')
        if i != None:
            return i
        i = GetStreamLength('RECEIVED')
        if i != None:
            return i
        return 0

    def __len__(self):
        return self.DataLength

    ApplicationName = property(lambda self: self._Application.Name)
    Handle = property(lambda self: self._Handle)
    DataLength = property(_GetDataLength)
    PartnerHandle = property(lambda self: self._Handle.split(':')[0])

    read = Read
    write = Write
    close = Disconnect
