'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *
from enums import *
from errors import *
import time


class ICallChannel(object):
    def __init__(self, Manager, Call, Stream, Type):
        self._Manager = Manager
        self._Call = Call
        self._Stream = Stream
        self._Type = Type

    def SendTextMessage(self, Text):
        '''Sends text message over channel.'''
        if self._Type == cctReliable:
            self._Stream.Write(Text)
        elif self._Type == cctDatagram:
            self._Stream.SendDatagram(Text)
        else:
            raise ISkypeError(0, 'Cannot send using %s channel type' & repr(self._Type))

    def _GetType(self):
        return self._Type

    Type = property(_GetType)

    def _GetStream(self):
        return self._Stream

    Stream = property(_GetStream)

    def _GetManager(self):
        return self._Manager

    Manager = property(_GetManager)

    def _GetCall(self):
        return self._Call

    Call = property(_GetCall)


class ICallChannelManager(EventHandlingBase):
    '''
    @ivar OnChannels: Event handler; prototype same as L{ICallChannelManagerEvents.Channels}.

    Type: callable
    @type OnChannels: callable

    @ivar OnMessage: Event handler; prototype same as L{ICallChannelManagerEvents.Message}.

    Type: callable
    @type OnMessage: callable

    @ivar OnCreated: Event handler; prototype same as L{ICallChannelManagerEvents.Created}.

    Type: callable
    @type OnCreated: callable
    '''

    def __init__(self, Events=None):
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

    def __del__(self):
        if self._Application:
            self._Application.Delete()
            self._Application = None
            self._Skype.UnregisterEventHandler('ApplicationStreams', self._OnApplicationStreams)
            self._Skype.UnregisterEventHandler('ApplicationReceiving', self._OnApplicationReceiving)
            self._Skype.UnregisterEventHandler('ApplicationDatagram', self._OnApplicationDatagram)

    def _OnCallStatus(self, pCall, Status):
        if Status == clsRinging:
            if self._Application == None:
                self.CreateApplication()
            self._Application.Connect(pCall.PartnerHandle, True)
            for stream in self._Application.Streams:
                if stream.PartnerHandle == pCall.PartnerHandle:
                    self._Channels.append(ICallChannel(self, pCall, stream, self._ChannelType))
                    self._CallEventHandler('Channels', self, self._Channels)
                    break
        elif Status in (clsCancelled, clsFailed, clsFinished, clsRefused, clsMissed):
            for ch in self._Channels:
                if ch.Call == pCall:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self._Channels)
                    try:
                        ch.Stream.Disconnect()
                    except ISkypeError:
                        pass
                    break

    def _OnApplicationStreams(self, pApp, pStreams):
        if pApp == self._Application:
            for ch in self._Channels:
                if ch.Stream not in pStreams:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self._Channels)

    def _OnApplicationReceiving(self, pApp, pStreams):
        if pApp == self._Application:
            for ch in self._Channels:
                if ch.Stream in pStreams:
                    msg = ICallChannelMessage(ch.Stream.Read())
                    self._CallEventHandler('Message', self, ch, msg)

    def _OnApplicationDatagram(self, pApp, pStream, Text):
        if pApp == self._Application:
            for ch in self_Channels:
                if ch.Stream == pStream:
                    msg = ICallChannelMessage(Text)
                    self._CallEventHandler('Message', self, ch, msg)
                    break

    def Connect(self, pSkype):
        '''Connects to Skype.'''
        self._Skype = pSkype
        self._Skype.RegisterEventHandler('CallStatus', self._OnCallStatus)

    def Disconnect(self):
        '''Disconnects from Skype.'''
        self._Skype.UnregisterEventHandler('CallStatus', self._OnCallStatus)
        self._Skype = None

    def CreateApplication(self, ApplicationName=None):
        '''Creates application context.'''
        if ApplicationName != None:
            self.Name = ApplicationName
        self._Application = self._Skype.Application(self.Name)
        self._Skype.RegisterEventHandler('ApplicationStreams', self._OnApplicationStreams)
        self._Skype.RegisterEventHandler('ApplicationReceiving', self._OnApplicationReceiving)
        self._Skype.RegisterEventHandler('ApplicationDatagram', self._OnApplicationDatagram)
        self._Application.Create()
        self._CallEventHandler('Created')

    def _GetChannels(self):
        return tuple(self._Channels)

    Channels = property(_GetChannels)

    def _GetChannelType(self):
        return self._ChannelType

    def _SetChannelType(self, ChannelType):
        self._ChannelType = ChannelType

    ChannelType = property(_GetChannelType, _SetChannelType)

    def _GetName(self):
        return self._Name

    def _SetName(self, Name):
        self._Name = unicode(Name)

    Name = property(_GetName, _SetName)

    def _GetCreated(self):
        return bool(self._Application)

    Created = property(_GetCreated)


class ICallChannelManagerEvents(object):
    def Channels(self):
        pass
    def Message(self):
        pass
    def Created(self):
        pass


ICallChannelManager._AddEvents(ICallChannelManagerEvents)


class ICallChannelMessage(object):
    def __init__(self, Text):
        self._Text = Text

    def _GetText(self):
        return self._Text

    def _SetText(self, Text):
        self._Text = Text

    Text = property(_GetText, _SetText)
