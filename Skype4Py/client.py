'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from enums import *
from errors import *
from utils import *
import weakref
import sys


class IClient(object):
    def __init__(self, Skype):
        self._SkypeRef = weakref.ref(Skype)

    def _GetSkype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise ISkypeError('Skype4Py internal error')

    def Start(self, Minimized=False, Nosplash=False):
        '''Starts Skype application.'''
        self._Skype._API.Start(Minimized, Nosplash)

    def Minimize(self):
        '''Hides Skype application window.'''
        self._Skype._DoCommand('MINIMIZE')

    def Shutdown(self):
        '''Closes Skype application.'''
        self._Skype._API.Shutdown()

    def OpenProfileDialog(self):
        '''Opens current user profile dialog.'''
        self.OpenDialog('PROFILE')

    def OpenUserInfoDialog(self, Username):
        '''Opens user information dialog.'''
        self.OpenDialog('USERINFO', Username)

    def OpenConferenceDialog(self):
        '''Opens create conference dialog.'''
        self.OpenDialog('CONFERENCE')

    def OpenSearchDialog(self):
        '''Opens search dialog.'''
        self.OpenDialog('SEARCH')

    def OpenOptionsDialog(self, Page=''):
        '''Opens options dialog.'''
        self.OpenDialog('OPTIONS', Page)

    def OpenCallHistoryTab(self):
        '''Opens call history tab.'''
        self.OpenDialog('CALLHISTORY')

    def OpenContactsTab(self):
        '''Opens contacts tab.'''
        self.OpenDialog('CONTACTS')

    def OpenDialpadTab(self):
        '''Opens dial pad tab.'''
        self.OpenDialog('DIALPAD')

    def OpenSendContactsDialog(self, Username=''):
        '''Opens send contacts dialog.'''
        self.OpenDialog('SENDCONTACTS', Username)

    def OpenBlockedUsersDialog(self):
        '''Opens blocked users dialog.'''
        self.OpenDialog('BLOCKEDUSERS')

    def OpenImportContactsWizard(self):
        '''Opens import contacts wizard.'''
        self.OpenDialog('IMPORTCONTACTS')

    def OpenGettingStartedWizard(self):
        '''Opens getting started wizard.'''
        self.OpenDialog('GETTINGSTARTED')

    def OpenAuthorizationDialog(self, Username):
        '''Opens authorization dialog.'''
        self.OpenDialog('AUTHORIZATION', Username)

    def OpenDialog(self, Name, *Params):
        '''Open dialog.'''
        self._Skype._DoCommand('OPEN %s %s' % (Name, ' '.join(Params)))

    def OpenVideoTestDialog(self):
        '''Opens video test dialog.'''
        self.OpenDialog('VIDEOTEST')

    def OpenAddContactDialog(self, Username=''):
        '''Opens "Add a Contact" dialog.'''
        self.OpenDialog('ADDAFRIEND', Username)

    def OpenMessageDialog(self, Username, Text=''):
        '''Opens "Send an IM Message" dialog.'''
        self.OpenDialog('IM', Username, Text)

    def OpenFileTransferDialog(self, Username, Folder):
        '''Opens file transfer dialog.'''
        self.OpenDialog('FILETRANSFER', Username, 'IN %s' % Folder)

    def Focus(self):
        '''Sets focus to Skype application window.'''
        self._Skype._DoCommand('FOCUS')

    def ButtonPressed(self, Key):
        '''Sends button button pressed to client.'''
        self._Skype._DoCommand('BTN_PRESSED %s' % Key)

    def ButtonReleased(self, Key):
        '''Sends button released event to client.'''
        self._Skype._DoCommand('BTN_RELEASED %s' % Key)

    def OpenSmsDialog(self, SmsId):
        '''Opens SMS window'''
        self.OpenDialog('SMS', SmsId)

    def CreateEvent(self, EventId, Caption, Hint):
        self._Skype._DoCommand('CREATE EVENT %s CAPTION %s HINT %s' % (EventId, quote(Caption), quote(Hint)))
        return IPluginEvent(EventId, self._Skype)

    def CreateMenuItem(self, MenuItemId, PluginContext, CaptionText, HintText=u'', IconPath='', Enabled=True,
                       ContactType=pluginContactTypeAll, MultipleContacts=False):
        com = 'CREATE MENU_ITEM %s CONTEXT %s CAPTION %s ENABLED %s' % (MenuItemId, PluginContext, quote(CaptionText), cndexp(Enabled, 'true', 'false'))
        if HintText:
            com += ' HINT %s' % quote(HintText)
        if IconPath:
            com += ' ICON %s' % quote(IconPath.decode(sys.getfilesystemencoding()))
        if MultipleContacts:
            com += ' ENABLE_MULTIPLE_CONTACTS true'
        if PluginContext == pluginContextContact:
            com += ' CONTACT_TYPE_FILTER %s' % ContactType
        self._Skype._DoCommand(com)
        return IPluginMenuItem(MenuItemId, self._Skype, CaptionText, HintText, Enabled)

    def OpenLiveTab(self):
        self.OpenDialog('LIVETAB')

    _Skype = property(_GetSkype)

    def _GetIsRunning(self):
        return self._Skype._API.IsRunning()

    IsRunning = property(_GetIsRunning)

    def _GetWallpaper(self):
        return self._Skype.Variable('WALLPAPER')

    def _SetWallpaper(self, value):
        self._Skype.Variable('WALLPAPER', value)

    Wallpaper = property(_GetWallpaper, _SetWallpaper)


class IPluginEvent(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = unicode(Id)

    def Delete(self):
        self._Skype._DoCommand('DELETE EVENT %s' % self._Id)

    def _GetId(self):
        return self._Id

    Id = property(_GetId)



class IPluginMenuItem(Cached):
    def _Init(self, Id, Skype, Caption=None, Hint=None, Enabled=None):
        self._Skype = Skype
        self._Id = unicode(Id)
        self._CacheDict = {}
        if Caption != None:
            self._CacheDict['CAPTION'] = unicode(Caption)
        if Hint != None:
            self._CacheDict['HINT'] = unicode(Hint)
        if Enabled != None:
            self._CacheDict['ENABLED'] = cndexp(Enabled, u'TRUE', u'FALSE')

    def _Property(self, PropName, Set=None):
        if Set == None:
            return self._CacheDict[PropName]
        self._Skype._Property('MENU_ITEM', self._Id, PropName, Set)
        self._CacheDict[PropName] = unicode(Set)

    def Delete(self):
        self._Skype._DoCommand('DELETE MENU_ITEM %s' % self._Id)

    def _GetId(self):
        return self._Id

    Id = property(_GetId)

    def _GetCaption(self):
        return self._Property('CAPTION')

    def _SetCaption(self, value):
        self._Property('CAPTION', value)

    Caption = property(_GetCaption, _SetCaption)

    def _GetHint(self):
        return self._Property('HINT')

    def _SetHint(self, value):
        self._Property('HINT', value)

    Hint = property(_GetHint, _SetHint)

    def _GetEnabled(self):
        return self._Property('ENABLED') == 'TRUE'

    def _SetEnabled(self, value):
        self._Property('ENABLED', cndexp(value, 'TRUE', 'FALSE'))

    Enabled = property(_GetEnabled, _SetEnabled)
