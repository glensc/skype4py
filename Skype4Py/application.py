'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from user import *
import threading


class IApplication(Cached):
    def _Init(self, Name, Skype):
        self._Name = unicode(Name)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('APPLICATION', self._Name, PropName, Set)

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('APPLICATION', self._Name, AlterName, Args)

    def Create(self):
        '''Creates application.'''
        self._Skype._DoCommand('CREATE APPLICATION %s' % self._Name)

    def Delete(self):
        '''Deletes application.'''
        self._Skype._DoCommand('DELETE APPLICATION %s' % self._Name)

    def Connect(self, Username, WaitConnected=False):
        '''Connects application to user.'''
        if WaitConnected:
            event = threading.Event()
            stream = [None]
            def app_streams(App, Streams):
                if App == self:
                    s = [x for x in Streams if x.PartnerHandle == Username]
                    if s:
                        stream[0] = s[0]
                        event.set()
            app_streams(self, self.Streams)
            self._Skype.RegisterEventHandler('ApplicationStreams', app_streams)
            self._Alter('CONNECT', Username)
            event.wait()
            self._Skype.UnregisterEventHandler('ApplicationStreams', app_streams)
            return stream[0]
        else:
            self._Alter('CONNECT', Username)

    def SendDatagram(self, Text, pStreams=None):
        '''Sends datagram to application streams.'''
        if pStreams == None:
            pStreams = self.Streams
        for s in pStreams:
            s.SendDatagram(Text)

    Name = property(lambda self: self._Name)
    Streams = property(lambda self: tuple(IApplicationStream(x, self) for x in esplit(self._Property('STREAMS'))))
    ConnectableUsers = property(lambda self: tuple(IUser(x, self._Skype) for x in esplit(self._Property('CONNECTABLE'))))
    ConnectingUsers = property(lambda self: tuple(IUser(x, self._Skype) for x in esplit(self._Property('CONNECTING'))))
    SendingStreams = property(lambda self: tuple(IApplicationStream(x.split('=')[0], self) for x in esplit(self._Property('SENDING'))))
    ReceivedStreams = property(lambda self: tuple(IApplicationStream(x.split('=')[0], self) for x in esplit(self._Property('RECEIVED'))))


class IApplicationStream(Cached):
    def _Init(self, Handle, Application):
        self._Handle = Handle
        self._Application = Application

    def Read(self):
        '''Reads stream.'''
        return self._Application._Alter('READ', self._Handle)

    def Write(self, Text):
        '''Writes stream.'''
        self._Application._Alter('WRITE', '%s %s' % (self._Handle, Text))

    def SendDatagram(self, Text):
        '''Send datagram on stream.'''
        self._Application._Alter('DATAGRAM', '%s %s' % (self._Handle, Text))

    def Disconnect(self):
        '''Disconnect stream.'''
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
