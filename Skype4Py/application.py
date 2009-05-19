'''APP2APP protocol.
'''

import threading

from utils import *
from user import *


class Application(Cached):
    '''Represents an application in APP2APP protocol. Use L{Skype.Application<skype.Skype.Application>} to instatinate.
    '''

    def __repr__(self):
        return '<%s with Name=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Name))

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('APPLICATION', self._Name, AlterName, Args)

    def _Init(self, Name, Skype):
        self._Name = tounicode(Name)
        self._Skype = Skype

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('APPLICATION', self._Name, PropName, Set)

    def _Connect_ApplicationStreams(self, App, Streams):
        if App == self:
            s = [x for x in Streams if x.PartnerHandle == self._Connect_Username]
            if s:
                self._Connect_Stream[0] = s[0]
                self._Connect_Event.set()

    def Connect(self, Username, WaitConnected=False):
        '''Connects application to user.

        @param Username: Name of the user to connect to.
        @type Username: str
        @param WaitConnected: If True, causes the method to wait untill the connection is established.
        @type WaitConnected: bool
        @return: If C{WaitConnected} is True, returns the stream which can be used to send the data.
        Otherwise returns None.
        @rtype: L{ApplicationStream} or None
        '''
        if WaitConnected:
            self._Connect_Event = threading.Event()
            self._Connect_Stream = [None]
            self._Connect_Username = Username
            self._Connect_ApplicationStreams(self, self.Streams)
            self._Skype.RegisterEventHandler('ApplicationStreams', self._Connect_ApplicationStreams)
            self._Alter('CONNECT', Username)
            self._Connect_Event.wait()
            self._Skype.UnregisterEventHandler('ApplicationStreams', self._Connect_ApplicationStreams)
            try:
                return self._Connect_Stream[0]
            finally:
                del self._Connect_Stream, self._Connect_Event, self._Connect_Username
        else:
            self._Alter('CONNECT', Username)

    def Create(self):
        '''Creates the APP2APP application in Skype client.
        '''
        self._Skype._DoCommand('CREATE APPLICATION %s' % self._Name)

    def Delete(self):
        '''Deletes the APP2APP application in Skype client.
        '''
        self._Skype._DoCommand('DELETE APPLICATION %s' % self._Name)

    def SendDatagram(self, Text, Streams=None):
        '''Sends datagram to application streams.

        @param Text: Text to send.
        @type Text: unicode
        @param Streams: Streams to send the datagram to or None if all currently connected streams should be used.
        @type Streams: sequence of L{ApplicationStream}
        '''
        if Streams is None:
            Streams = self.Streams
        for s in Streams:
            s.SendDatagram(Text)

    def _GetConnectableUsers(self):
        return gen(User(x, self._Skype) for x in split(self._Property('CONNECTABLE')))

    ConnectableUsers = property(_GetConnectableUsers,
    doc='''All connectable users.

    @type: tuple of L{User}
    ''')

    def _GetConnectingUsers(self):
        return gen(User(x, self._Skype) for x in split(self._Property('CONNECTING')))

    ConnectingUsers = property(_GetConnectingUsers,
    doc='''All users connecting at the moment.

    @type: tuple of L{User}
    ''')

    def _GetName(self):
        return self._Name

    Name = property(_GetName,
    doc='''Name of the application.

    @type: unicode
    ''')

    def _GetReceivedStreams(self):
        return gen(ApplicationStream(x.split('=')[0], self) for x in split(self._Property('RECEIVED')))

    ReceivedStreams = property(_GetReceivedStreams,
    doc='''All streams that received data and can be read.

    @type: tuple of L{ApplicationStream}
    ''')

    def _GetSendingStreams(self):
        return gen(ApplicationStream(x.split('=')[0], self) for x in split(self._Property('SENDING')))

    SendingStreams = property(_GetSendingStreams,
    doc='''All streams that send data and at the moment.

    @type: tuple of L{ApplicationStream}
    ''')

    def _GetStreams(self):
        return gen(ApplicationStream(x, self) for x in split(self._Property('STREAMS')))

    Streams = property(_GetStreams,
    doc='''All currently connected application streams.

    @type: tuple of L{ApplicationStream}
    ''')


class ApplicationStream(Cached):
    '''Represents an application stream in APP2APP protocol.
    '''

    def __len__(self):
        return self.DataLength

    def __repr__(self):
        return '<%s with Handle=%s, Application=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Handle), repr(self.Application))

    def _Init(self, Handle, Application):
        self._Handle = str(Handle)
        self._Application = Application

    def Disconnect(self):
        '''Disconnects the stream.
        '''
        self._Application._Alter('DISCONNECT', self._Handle)

    close = Disconnect

    def Read(self):
        '''Reads data from stream.

        @return: Read data or an empty string if none were available.
        @rtype: unicode
        '''
        return self._Application._Alter('READ', self._Handle)

    read = Read

    def SendDatagram(self, Text):
        '''Sends datagram to stream.

        @param Text: Datagram to send.
        @type Text: unicode
        '''
        self._Application._Alter('DATAGRAM', '%s %s' % (self._Handle, tounicode(Text)))

    def Write(self, Text):
        '''Writes data to stream.

        @param Text: Data to send.
        @type Text: unicode
        '''
        self._Application._Alter('WRITE', '%s %s' % (self._Handle, tounicode(Text)))

    write = Write

    def _GetApplication(self):
        return self._Application

    Application = property(_GetApplication,
    doc='''Application this stream belongs to.

    @type: L{Application}
    ''')

    def _GetApplicationName(self):
        return self._Application.Name

    ApplicationName = property(_GetApplicationName,
    doc='''Name of the application this stream belongs to. Same as C{ApplicationStream.Application.Name}.

    @type: unicode
    ''')

    def _GetDataLength_GetStreamLength(self, Type):
        for s in split(self._Application._Property(Type)):
            h, i = s.split('=')
            if h == self._Handle:
                return int(i)

    def _GetDataLength(self):
        i = self._GetDataLength_GetStreamLength('SENDING')
        if i is not None:
            return i
        i = self._GetDataLength_GetStreamLength('RECEIVED')
        if i is not None:
            return i
        return 0

    DataLength = property(_GetDataLength,
    doc='''Number of bytes awaiting in the read buffer.

    @type: int
    ''')

    def _GetHandle(self):
        return self._Handle

    Handle = property(_GetHandle,
    doc='''Stream handle in u'<Skypename>:<n>' format.

    @type: str
    ''')

    def _GetPartnerHandle(self):
        return self._Handle.split(':')[0]

    PartnerHandle = property(_GetPartnerHandle,
    doc='''Skypename of the user this stream is connected to.

    @type: str
    ''')
