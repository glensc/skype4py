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


class ICallChannelManagerEvents(object):
    def Channels(self, pManager, pChannels):
        pass

    def Message(self, pManager, pChannel, pMessage):
        pass

    def Created(self):
        pass


class ICallChannel(object):
    def __init__(self, Manager, Call, Stream, Type):
        self._Manager = Manager
        self._Call = Call
        self._Stream = Stream
        self._Type = Type

    def SendTextMessage(self, Text):
        if self._Type == TCallChannelType.cctReliable:
            self._Stream.Write(Text)
        elif self._Type == TCallChannelType.cctDatagram:
            self._Stream.SendDatagram(Text)
        else:
            raise SkypeError(0, 'Cannot send using %s channel type' & repr(self._Type))

    Type = property(lambda self: self._Type)
    Stream = property(lambda self: self._Stream)
    Manager = property(lambda self: self._Manager)
    Call = property(lambda self: self._Call)


ICallChannelManagerEventHandling = EventHandling(dir(ICallChannelManagerEvents))


class ICallChannelManager(ICallChannelManagerEventHandling):
    def __init__(self, Events=ICallChannelManagerEvents):
        ICallChannelManagerEventHandling.__init__(self)
        self._RegisterEventsClass(Events)

        self._Skype = None
        self._CallStatusEventHandler = None
        self._ApplicationStreamsEventHandler = None
        self._ApplicationReceivingEventHandler = None
        self._ApplicationDatagramEventHandler = None
        self._Application = None
        self._Name = u'CallChannelManager'
        self._ChannelType = TCallChannelType.cctReliable
        self._Channels = []

    def __del__(self):
        if self._Application:
            self._Application.Delete()
            self._Application = None
            self._Skype._UnregisterEventHandler('ApplicationStreams', self._ApplicationStreamsEventHandler)
            self._Skype._UnregisterEventHandler('ApplicationReceiving', self._ApplicationReceivingEventHandler)
            self._Skype._UnregisterEventHandler('ApplicationDatagram', self._ApplicationDatagramEventHandler)

    def _OnCallStatus(self, pCall, Status):
        if Status == TCallStatus.clsRinging:
            streams = self._Application.Streams
            self._Application.Connect(pCall.PartnerHandle, True)
            for stream in self._Application.Streams:
                if stream.PartnerHandle == pCall.PartnerHandle:
                    self._Channels.append(ICallChannel(self, pCall, stream, self._ChannelType))
                    self._CallEventHandler('Channels', self, self._Channels)
                    break
        elif Status in [TCallStatus.clsCancelled, TCallStatus.clsFailed, TCallStatus.clsFinished, TCallStatus.clsRefused, TCallStatus.clsMissed]:
            for ch in self._Channels:
                if ch.Call == pCall:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self._Channels)
                    break

    def _OnApplicationStreams(self, pApp, pStreams):
        if pApp == self._Application:
            for ch in self._Channels:
                if ch.Stream not in pStreams:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self._Channels)

    def _OnApplicationReceiving(self, pApp, pStreams):
        print 'receiving handler', pApp, pStreams
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
        self._Skype = pSkype
        self._CallStatusEventHandler = self._Skype._RegisterEventHandler('CallStatus', None, self._OnCallStatus)

    def Disconnect(self):
        self._Skype._UnregisterEventHandler('CallStatus', self._CallStatusEventHandler)
        self._Skype = None

    def CreateApplication(self, ApplicationName=''):
        if ApplicationName:
            self.Name = ApplicationName
        self._Application = self._Skype.Application(self.Name)
        self._Application.Create()
        self._ApplicationStreamsEventHandler = self._Skype._RegisterEventHandler('ApplicationStreams', None, self._OnApplicationStreams)
        self._ApplicationReceivingEventHandler = self._Skype._RegisterEventHandler('ApplicationReceiving', None, self._OnApplicationReceiving)
        self._ApplicationDatagramEventHandler = self._Skype._RegisterEventHandler('ApplicationDatagram', None, self._OnApplicationDatagram)
        self._CallEventHandler('Created')

    def _SetChannelType(self, ChannelType):
        self._ChannelType = TCallChannelType(ChannelType)

    def _SetName(self, Name):
        self._Name = Name

    Channels = property(lambda self: self._Channels)
    ChannelType = property(lambda self: self._ChannelType, _SetChannelType)
    Name = property(lambda self: self._Name, _SetName)
    Created = property(lambda self: bool(self._Application))


class ICallChannelMessage(object):
    def __init__(self, Text):
        self._Text = Text

    def _SetText(self, Text):
        self._Text = Text

    Text = property(lambda self: self._Text, _SetText)
