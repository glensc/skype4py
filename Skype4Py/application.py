'''
Classes handling the APP2APP protocol.
'''

from utils import *
from user import *
import threading


class IApplication(Cached):
    '''Represents an application in APP2APP protocol. Use L{ISkype.Application} to instatinate.'''

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
        '''Connects application to user.

        @param Username: Name of the user to connect to.
        @type Username: unicode
        @param WaitConnected: If True, causes the method to wait untill the connection is established.
        @type WaitConnected: bool
        '''
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

    def SendDatagram(self, Text, Streams=None):
        '''Sends datagram to application streams.

        @param Text: Text to send.
        @type Text: unicode
        @param Streams: Streams to send the datagram to or None if all currently connected streams should be used.
        @type Streams: iterable of L{IApplicationStream}
        '''
        if Streams == None:
            Streams = self.Streams
        for s in Streams:
            s.SendDatagram(Text)

    def _GetName(self):
        return self._Name

    Name = property(_GetName,
    doc='''Name of the application.

    Type: unicode
    @type: unicode''')

    def _GetStreams(self):
        return tuple(IApplicationStream(x, self) for x in esplit(self._Property('STREAMS')))

    Streams = property(_GetStreams,
    doc='''All currently connected application streams.

    Type: tuple of L{IApplicationStream}
    @type: tuple of L{IApplicationStream}''')

    def _GetConnectableUsers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('CONNECTABLE')))

    ConnectableUsers = property(_GetConnectableUsers,
    doc='''All connectable users.

    Type: tuple of L{IUser}
    @type: tuple of L{IUser}''')

    def _GetConnectingUsers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('CONNECTING')))

    ConnectingUsers = property(_GetConnectingUsers,
    doc='''All users connecting at the moment.

    Type: tuple of L{IUser}
    @type: tuple of L{IUser}''')

    def _GetSendingStreams(self):
        return tuple(IApplicationStream(x.split('=')[0], self) for x in esplit(self._Property('SENDING')))

    SendingStreams = property(_GetSendingStreams,
    doc='''All streams that send data and at the moment.

    Type: tuple of L{IApplicationStream}
    @type: tuple of L{IApplicationStream}''')

    def _GetReceivedStreams(self):
        return tuple(IApplicationStream(x.split('=')[0], self) for x in esplit(self._Property('RECEIVED')))

    ReceivedStreams = property(_GetReceivedStreams,
    doc='''All streams that received data and can be read.

    Type: tuple of L{IApplicationStream}
    @type: tuple of L{IApplicationStream}''')


class IApplicationStream(Cached):
    '''Represents an application stream in APP2APP protocol.'''

    def _Init(self, Handle, Application):
        self._Handle = Handle
        self._Application = Application

    def Read(self):
        '''Reads data from stream.

        @returns: Read data or an empty string if none were available.
        @rtype: unicode
        '''
        return self._Application._Alter('READ', self._Handle)

    def Write(self, Text):
        '''Writes data to stream.

        @param Text: Data to send.
        @type Text: unicode
        '''
        self._Application._Alter('WRITE', '%s %s' % (self._Handle, Text))

    def SendDatagram(self, Text):
        '''Sends datagram to stream.

        @param Text: Datagram to send.
        @type Text: unicode
        '''
        self._Application._Alter('DATAGRAM', '%s %s' % (self._Handle, Text))

    def Disconnect(self):
        '''Disconnects from stream.'''
        self._Application._Alter('DISCONNECT', self._Handle)

    def __len__(self):
        return self.DataLength

    def _GetApplication(self):
        return self._Application

    Application = property(_GetApplication,
    doc='''Application this stream belongs to.

    Type: L{IApplication}
    @type: L{IApplication}''')

    def _GetApplicationName(self):
        return self._Application.Name

    ApplicationName = property(_GetApplicationName,
    doc='''Name of the application this stream belongs to.

    Type: unicode
    @type: unicode''')

    def _GetHandle(self):
        return self._Handle

    Handle = property(_GetHandle,
    doc='''Stream handle in u'<Skypename>:<n>' format.

    Type: unicode
    @type: unicode''')

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

    DataLength = property(_GetDataLength,
    doc='''Number of bytes awaiting in the read buffer.

    Type: int
    @type: int''')

    def _GetPartnerHandle(self):
        return self._Handle.split(':')[0]

    PartnerHandle = property(_GetPartnerHandle,
    doc='''Skypename of the user this stream is connected to.

    Type: unicode
    @type: unicode''')

    read = Read
    write = Write
    close = Disconnect
    
