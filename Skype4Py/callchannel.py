'''Data channels for calls.
'''
__docformat__ = 'restructuredtext en'


import time

from utils import *
from enums import *
from errors import SkypeError


class CallChannel(object):
    '''Represents a call channel.
    '''

    def __init__(self, Manager, Call, Stream, Type):
        '''Initializes the object.
        
        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
          Call : `Call`
            The call object.
          Stream : `ApplicationStream`
            The APP2APP stream object.
          Type : `enums`.cct*
            The call channel type.
        '''
        self._Manager = Manager
        self._Call = Call
        self._Stream = Stream
        self._Type = str(Type)

    def __repr__(self):
        return '<%s with Manager=%s, Call=%s, Stream=%s>' % (object.__repr__(self)[1:-1], repr(self.Manager), repr(self.Call), repr(self.Stream))

    def SendTextMessage(self, Text):
        '''Sends a text message over channel.

        :Parameters:
          Text : unicode
            Text to send.
        '''
        if self._Type == cctReliable:
            self._Stream.Write(Text)
        elif self._Type == cctDatagram:
            self._Stream.SendDatagram(Text)
        else:
            raise SkypeError(0, 'Cannot send using %s channel type' & repr(self._Type))

    def _GetCall(self):
        return self._Call

    Call = property(_GetCall,
    doc='''The call object associated with this channel.

    :type: `Call`
    ''')

    def _GetManager(self):
        return self._Manager

    Manager = property(_GetManager,
    doc='''The call channel manager object.

    :type: `CallChannelManager`
    ''')

    def _GetStream(self):
        return self._Stream

    Stream = property(_GetStream,
    doc='''Underlying APP2APP stream object.

    @type: `ApplicationStream`
    ''')

    def _GetType(self):
        return self._Type

    Type = property(_GetType,
    doc='''Type of this channel.

    :type: `enums`.cct*
    ''')


class CallChannelManager(EventHandlingBase):
    '''Instantiate this class to create a call channel manager. A call channel manager will
    automatically create a data channel (based on the APP2APP protocol) for voice calls.

    1. Usage.

       You should access this class using the alias at the package level:
       
       .. python::

           import Skype4Py

           skype = Skype4Py.Skype()

           ccm = Skype4Py.CallChannelManager()
           ccm.Connect(skype)

       Read the constructor (`CallChannelManager.__init__`) documentation for a list of
       accepted arguments.

    2. Events.

       This class provides events.

       The events names and their arguments lists can be found in the
       `CallChannelManagerEvents` class in this module.

       The use of events is explained in `EventHandlingBase` class which
       is a superclass of this class.
    '''

    def __del__(self):
        if self._Application:
            self._Application.Delete()
            self._Application = None
            self._Skype.UnregisterEventHandler('ApplicationStreams', self._OnApplicationStreams)
            self._Skype.UnregisterEventHandler('ApplicationReceiving', self._OnApplicationReceiving)
            self._Skype.UnregisterEventHandler('ApplicationDatagram', self._OnApplicationDatagram)

    def __init__(self, Events=None):
        '''Initializes the object.
        
        :Parameters:
          Events
            An optional object with event handlers. See `EventHandlingBase` for more
            information on events.
        '''
        EventHandlingBase.__init__(self)
        if Events:
            self._SetEventHandlerObj(Events)

        self._Skype = None
        self._CallStatusEventHandler = None
        self._ApplicationStreamsEventHandler = None
        self._ApplicationReceivingEventHandler = None
        self._ApplicationDatagramEventHandler = None
        self._Application = None
        self._Name = u'CallChannelManager'
        self._ChannelType = cctReliable
        self._Channels = []

    def _OnApplicationDatagram(self, App, Stream, Text):
        if App == self._Application:
            for ch in self_Channels:
                if ch.Stream == Stream:
                    msg = CallChannelMessage(Text)
                    self._CallEventHandler('Message', self, ch, msg)
                    break

    def _OnApplicationReceiving(self, App, Streams):
        if App == self._Application:
            for ch in self._Channels:
                if ch.Stream in Streams:
                    msg = CallChannelMessage(ch.Stream.Read())
                    self._CallEventHandler('Message', self, ch, msg)

    def _OnApplicationStreams(self, App, Streams):
        if App == self._Application:
            for ch in self._Channels:
                if ch.Stream not in Streams:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self.Channels)

    def _OnCallStatus(self, Call, Status):
        if Status == clsRinging:
            if self._Application is None:
                self.CreateApplication()
            self._Application.Connect(Call.PartnerHandle, True)
            for stream in self._Application.Streams:
                if stream.PartnerHandle == Call.PartnerHandle:
                    self._Channels.append(CallChannel(self, Call, stream, self._ChannelType))
                    self._CallEventHandler('Channels', self, self.Channels)
                    break
        elif Status in (clsCancelled, clsFailed, clsFinished, clsRefused, clsMissed):
            for ch in self._Channels:
                if ch.Call == Call:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self.Channels)
                    try:
                        ch.Stream.Disconnect()
                    except SkypeError:
                        pass
                    break

    def Connect(self, Skype):
        '''Connects this call channel manager instance to Skype. This is the first thing you should
        do after creating this object.

        :Parameters:
          Skype : `Skype`
            The Skype object.

        :see: `Disconnect`
        '''
        self._Skype = Skype
        self._Skype.RegisterEventHandler('CallStatus', self._OnCallStatus)

    def CreateApplication(self, ApplicationName=None):
        '''Creates an APP2APP application context. The application is automatically created using
        `application.Application.Create` method.
        
        :Parameters:
          ApplicationName : unicode
            Application name. The default name is ``u'CallChannelManager'``.
        '''
        if ApplicationName is not None:
            self.Name = tounicode(ApplicationName)
        self._Application = self._Skype.Application(self.Name)
        self._Skype.RegisterEventHandler('ApplicationStreams', self._OnApplicationStreams)
        self._Skype.RegisterEventHandler('ApplicationReceiving', self._OnApplicationReceiving)
        self._Skype.RegisterEventHandler('ApplicationDatagram', self._OnApplicationDatagram)
        self._Application.Create()
        self._CallEventHandler('Created', self)

    def Disconnect(self):
        '''Disconnects from the Skype instance.
        
        :see: `Connect`
        '''
        self._Skype.UnregisterEventHandler('CallStatus', self._OnCallStatus)
        self._Skype = None

    def _GetChannels(self):
        return list(self._Channels)

    Channels = property(_GetChannels,
    doc='''All call data channels.

    :type: list of `CallChannel`
    ''')

    def _GetChannelType(self):
        return self._ChannelType

    def _SetChannelType(self, Value):
        self._ChannelType = str(Value)

    ChannelType = property(_GetChannelType, _SetChannelType,
    doc='''Queries/sets the default channel type.

    :type: `enums`.cct*
    ''')

    def _GetCreated(self):
        return bool(self._Application)

    Created = property(_GetCreated,
    doc='''Returns True if the application context has been created.

    :type: bool
    ''')

    def _GetName(self):
        return self._Name

    def _SetName(self, Value):
        self._Name = tounicode(Value)

    Name = property(_GetName, _SetName,
    doc='''Queries/sets the application context name.

    :type: unicode
    ''')


class CallChannelManagerEvents(object):
    '''Events defined in `CallChannelManager`.

    See `EventHandlingBase` for more information on events.
    '''

    def Channels(self, Manager, Channels):
        '''This event is triggered when list of call channels changes.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
          Channels : tuple of `CallChannel`
            Updated list of call channels.
        '''

    def Created(self, Manager):
        '''This event is triggered when the application context has successfully been created.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
        '''

    def Message(self, Manager, Channel, Message):
        '''This event is triggered when a call channel message has been received.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
          Channel : `CallChannel`
            The call channel object receiving the message.
          Message : `CallChannelMessage`
            The received message.
        '''


CallChannelManager._AddEvents(CallChannelManagerEvents)


class CallChannelMessage(object):
    '''Represents a call channel message.
    '''

    def __init__(self, Text):
        '''Initializes the object.

        :Parameters:
          Text : unicode
            The message text.
        '''
        self._Text = tounicode(Text)

    def _GetText(self):
        return self._Text

    def _SetText(self, Value):
        self._Text = tounicode(Value)

    Text = property(_GetText, _SetText,
    doc='''Queries/sets the message text.

    :type: unicode
    ''')
