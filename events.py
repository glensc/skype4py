
from errors import *


class ISkypeEvents(object):
    def Command(self, Command):
        print '<CmdSend> ' + Command.Command

    def Reply(self, Command):
        print '<CmdRece> ' + Command.Reply

    def Error_(self, pCommand, Number, Description):
        raise ISkypeError(int(Number), Description)

    def AttachmentStatus(self, Status):
        if Status == 'REFUSED':
            raise ISkypeAPIError('Skype connection refused')

    def ConnectionStatus(self, Status):
        pass

    def UserStatus(self, Status):
        pass

    def OnlineStatus(self, pUser, Status):
        pass

    def CallStatus(self, pCall, Status):
        pass

    def CallHistory(self):
        pass

    def Mute(self, Mute):
        pass

    def MessageStatus(self, pMessage, Status):
        pass

    def MessageHistory(self, Username):
        pass

    def AutoAway(self, Automatic):
        pass

    def CallDtmfReceived(self, pCall, Code):
        pass

    def VoicemailStatus(self, pMail, Status):
        pass

    def ApplicationConnecting(self, pApp, pUsers):
        pass

    def ApplicationStreams(self, pApp, pStreams):
        pass

    def ApplicationDatagram(self, pApp, pStream, Text):
        pass

    def ApplicationSending(self, pApp, pStreams):
        pass

    def ApplicationReceiving(self, pApp, pStreams):
        pass

    def ContactsFocused(self, Username):
        pass

    def GroupVisible(self, pGroup, Visible):
        pass

    def GroupExpanded(self, pGroup, Expanded):
        pass

    def GroupUsers(self, pGroup, pUsers):
        pass

    def GroupDeleted(self, GroupId):
        pass

    def UserMood(self, pUser, MoodText):
        pass

    def SmsMessageStatusChanged(self, pMessage, Status):
        pass

    def SmsTargetStatusChanged(self, pTarget, Status):
        pass

    def CallInputStatusChanged(self, pCall, Status):
        pass

    def AsyncSearchUsersFinished(self, Cookie, pUsers):
        pass

    def CallSeenStatusChanged(self, pCall, Status):
        pass

    def PluginEventClicked(self, pEvent):
        pass

    def PluginMenuItemClicked(self, pMenuItem, pUsers, PluginContext, ContextId):
        pass

    def WallpaperChanged(self, Path):
        pass

    def FileTransferStatusChanged(self, pTransfer, Status):
        pass

    def Channels(self, pManager, pChannels):
        pass

    def Message(self, pManager, pChannel, pMessage):
        pass

    def Created(self):
        pass
