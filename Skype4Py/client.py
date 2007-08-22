'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from enums import *
from plugin import *
from errors import *
import weakref


class IClient(object):
    def __init__(self, Skype):
        self._SkypeRef = weakref.ref(Skype)

    def _GetSkype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise ISkypeError('Skype4Py internal error')

    def Start(self, Minimized=False, Nosplash=False):
        self._Skype._API.Start(Minimized, Nosplash)

    def Minimize(self):
        self._Skype._DoCommand('MINIMIZE')

    def Shutdown(self):
        self._Skype._API.Shutdown()

    def OpenProfileDialog(self):
        self.OpenDialog('PROFILE')

    def OpenUserInfoDialog(self, Username):
        self.OpenDialog('USERINFO', Username)

    def OpenConferenceDialog(self):
        self.OpenDialog('CONFERENCE')

    def OpenSearchDialog(self):
        self.OpenDialog('SEARCH')

    def OpenOptionsDialog(self, Page=''):
        self.OpenDialog('OPTIONS', Page)

    def OpenCallHistoryTab(self):
        self.OpenDialog('CALLHISTORY')

    def OpenContactsTab(self):
        self.OpenDialog('CONTACTS')

    def OpenDialpadTab(self):
        self.OpenDialog('DIALPAD')

    def OpenSendContactsDialog(self, Username=''):
        self.OpenDialog('SENDCONTACTS', Username)

    def OpenBlockedUsersDialog(self):
        self.OpenDialog('BLOCKEDUSERS')

    def OpenImportContactsWizard(self):
        self.OpenDialog('IMPORTCONTACTS')

    def OpenGettingStartedWizard(self):
        self.OpenDialog('GETTINGSTARTED')

    def OpenAuthorizationDialog(self, Username):
        self.OpenDialog('AUTHORIZATION', Username)

    def OpenDialog(self, Name, Param1='', Param2=''):
        self._Skype._DoCommand('OPEN %s %s %s' % (Name, Param1, Param2))

    def OpenVideoTestDialog(self):
        self.OpenDialog('VIDEOTEST')

    def OpenAddContactDialog(self, Username=''):
        self.OpenDialog('ADDAFRIEND', Username)

    def OpenMessageDialog(self, Username, Text=''):
        self.OpenDialog('IM', Username, Text)

    def OpenFileTransferDialog(self, Username, Folder):
        self.OpenDialog('FILETRANSFER', Username, 'IN %s' % Folder)

    def Focus(self):
        self._Skype._DoCommand('FOCUS')

    def ButtonPressed(self, Key):
        self._Skype._DoCommand('BTN_PRESSED %s' % Key)

    def ButtonReleased(self, Key):
        self._Skype._DoCommand('BTN_RELEASED %s' % Key)

    def OpenSmsDialog(self, SmsId):
        self.OpenDialog('SMS', SmsId)

    def CreateEvent(self, EventId, Caption, Hint):
        self._Skype._DoCommand('CREATE EVENT %s CAPTION %s HINT %s' % (EventId, quote(Caption), quote(Hint)))
        return IPluginEvent(EventId, self._Skype)

    def CreateMenuItem(self, MenuItemId, PluginContext, CaptionText, HintText='', IconPath='', Enabled=True,
                       ContactType=pluginContactTypeAll, MultipleContacts=False):
        com = 'CREATE MENU_ITEM %s CONTEXT %s CAPTION %s' % (MenuItemId, str(PluginContext), quote(CaptionText))
        if HintText:
            com += ' HINT %s' % quote(HintText)
        if IconPath:
            com += ' ICON %s' % quote(IconPath)
        com += ' ENABLED %s ENABLE_MULTIPLE_CONTACTS %s' % ('TRUE' if Enabled else 'FALSE', 'TRUE' if MultipleContacts else 'FALSE')
        self._Skype._DoCommand(com)
        return IPluginMenuItem(MenuItemId, self._Skype, CaptionText, HintText, Enabled)

    def OpenLiveTab(self):
        self.OpenDialog('LIVETAB')

    _Skype = property(_GetSkype)

    IsRunning = property(lambda self: self._Skype._API.IsRunning())
    Wallpaper = property(lambda self: self._Skype.Variable('WALLPAPER'),
                         lambda self, value: self._Skype.Variable('WALLPAPER', value))
