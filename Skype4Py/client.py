'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from enums import *
from plugin import *


class IClient(object):
    def __init__(self, Skype):
        self._Skype = Skype

    def Start(self, Minimized=False, Nosplash=False):
        self._Skype._API.Start(Minimized, Nosplash)

    def Minimize(self):
        self._Skype._DoCommand('MINIMIZE')

    def Shutdown(self):
        self._Skype._API.Shutdown()

    def OpenProfileDialog(self):
        self._Skype._DoCommand('OPEN PROFILE')

    def OpenUserInfoDialog(self, Username):
        self._Skype._DoCommand('OPEN USERINFO %s' % Username)

    def OpenConferenceDialog(self):
        self._Skype._DoCommand('OPEN CONFERENCE')

    def OpenSearchDialog(self):
        self._Skype._DoCommand('OPEN SEARCH')

    def OpenOptionsDialog(self, Page):
        self._Skype._DoCommand('OPEN OPTIONS')

    def OpenCallHistoryTab(self):
        self._Skype._DoCommand('OPEN CALLHISTORY')

    def OpenContactsTab(self):
        self._Skype._DoCommand('OPEN CONTACTS')

    def OpenDialpadTab(self):
        self._Skype._DoCommand('OPEN DIALPAD')

    def OpenSendContactsDialog(self, Username=''):
        self._Skype._DoCommand('OPEN SENDCONTACTS %s' % Username)

    def OpenBlockedUsersDialog(self):
        self._Skype._DoCommand('OPEN BLOCKEDUSERS')

    def OpenImportContactsWizard(self):
        self._Skype._DoCommand('OPEN IMPORTCONTACTS')

    def OpenGettingStartedWizard(self):
        self._Skype._DoCommand('OPEN GETTINGSTARTED')

    def OpenAuthorizationDialog(self, Username):
        self._Skype._DoCommand('OPEN AUTHORIZATION %s' % Username)

    def OpenDialog(self, Name, Param1='', Param2=''):
        pass

    def OpenVideoTestDialog(self):
        self._Skype._DoCommand('OPEN VIDEOTEST')

    def OpenAddContactDialog(self, Username=''):
        self._Skype._DoCommand('OPEN ADDAFRIEND %s' % Username)

    def OpenMessageDialog(self, Username, Text=''):
        self._Skype._DoCommand('OPEN IM %s %s' % (Username, Text))

    def OpenFileTransferDialog(self, Username, Folder):
        self._Skype._DoCommand('OPEN FILETRANSFER %s IN %s' % (Username, Folder))

    def Focus(self):
        self._Skype._DoCommand('FOCUS')

    def ButtonPressed(self, Key):
        self._Skype._DoCommand('BTN_PRESSED %s' % Key)

    def ButtonReleased(self, Key):
        self._Skype._DoCommand('BTN_RELEASED %s' % Key)

    def OpenSmsDialog(self, SmsId):
        self._Skype._DoCommand('OPEN SMS %s' % SmsId)

    def CreateEvent(self, EventId, Caption, Hint):
        self._Skype._DoCommand('CREATE EVENT %s CAPTION %s HINT %s' % (EventId, quote(Caption), quote(Hint)))
        return IPluginEvent(EventId, self._Skype)

    def CreateMenuItem(self, MenuItemId, PluginContext, CaptionText, HintText='', IconPath='', Enabled=True,
                       ContactType=TPluginContactType.All, MultipleContacts=False):
        com = 'CREATE MENU_ITEM %s CONTEXT %s CAPTION %s' % (MenuItemId, str(PluginContext), quote(CaptionText))
        if HintText:
            com += ' HINT %s' % quote(HintText)
        if IconPath:
            com += ' ICON %s' % quote(IconPath)
        com += ' ENABLED %s ENABLE_MULTIPLE_CONTACTS %s' % ('TRUE' if Enabled else 'FALSE', 'TRUE' if MultipleContacts else 'FALSE')
        self._Skype._DoCommand(com)
        return IPluginMenuItem(MenuItemId, self._Skype, CaptionText, HintText, Enabled)

    IsRunning = property(lambda self: self._Skype._API.IsRunning())
    Wallpaper = property(lambda self: self._Skype.Variable('WALLPAPER'),
                         lambda self, value: self._Skype.Variable('WALLPAPER', value))
