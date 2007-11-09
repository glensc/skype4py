'''Skype client user interface control.
'''

from enums import *
from errors import *
from utils import *
import weakref


class IClient(object):
    '''Represents a Skype client. Access using L{ISkype.Client}.
    '''

    def __init__(self, Skype):
        '''Private.

        @param Skype: Skype
        @type Skype: L{ISkype}
        '''
        self._SkypeRef = weakref.ref(Skype)

    def ButtonPressed(self, Key):
        '''Sends button button pressed to client.

        @param Key: Key
        @type Key: unicode
        '''
        self._Skype._DoCommand('BTN_PRESSED %s' % Key)

    def ButtonReleased(self, Key):
        '''Sends button released event to client.

        @param Key: Key
        @type Key: unicode
        '''
        self._Skype._DoCommand('BTN_RELEASED %s' % Key)

    def CreateEvent(self, EventId, Caption, Hint):
        '''CreateEvent.

        @param EventId: EventId
        @type EventId: ?
        @param Caption: Caption
        @type Caption: ?
        @param Hint: Hint
        @type Hint: ?
        @return: ?
        @rtype: ?
        '''
        self._Skype._DoCommand('CREATE EVENT %s CAPTION %s HINT %s' % (EventId, quote(Caption), quote(Hint)))
        return IPluginEvent(EventId, self._Skype)

    def CreateMenuItem(self, MenuItemId, PluginContext, CaptionText, HintText=u'', IconPath='', Enabled=True,
                       ContactType=pluginContactTypeAll, MultipleContacts=False):
        '''CreateMenuItem.

        @param MenuItemId: MenuItemId
        @type MenuItemId: ?
        @param PluginContext: PluginContext
        @type PluginContext: unicode
        @param CaptionText: CaptionText
        @type CaptionText: unicode
        @param HintText: HintText
        @type HintText: unicode
        @param IconPath: IconPath
        @type IconPath: unicode
        @param Enabled: Enabled
        @type Enabled: ?
        @param ContactType: ContactType
        @type ContactType: ?
        @param MultipleContacts: MultipleContacts
        @type MultipleContacts: ?
        @return: ?
        @rtype: ?
        '''
        com = 'CREATE MENU_ITEM %s CONTEXT %s CAPTION %s ENABLED %s' % (MenuItemId, PluginContext, quote(CaptionText), cndexp(Enabled, 'true', 'false'))
        if HintText:
            com += ' HINT %s' % quote(HintText)
        if IconPath:
            com += ' ICON %s' % quote(IconPath)
        if MultipleContacts:
            com += ' ENABLE_MULTIPLE_CONTACTS true'
        if PluginContext == pluginContextContact:
            com += ' CONTACT_TYPE_FILTER %s' % ContactType
        self._Skype._DoCommand(com)
        return IPluginMenuItem(MenuItemId, self._Skype, CaptionText, HintText, Enabled)

    def Focus(self):
        '''Sets focus to Skype application window.
        '''
        self._Skype._DoCommand('FOCUS')

    def Minimize(self):
        '''Hides Skype application window.
        '''
        self._Skype._DoCommand('MINIMIZE')

    def OpenAddContactDialog(self, Username=''):
        '''Opens "Add a Contact" dialog.

        @param Username: Username
        @type Username: unicode
        '''
        self.OpenDialog('ADDAFRIEND', Username)

    def OpenAuthorizationDialog(self, Username):
        '''Opens authorization dialog.

        @param Username: Username
        @type Username: unicode
        '''
        self.OpenDialog('AUTHORIZATION', Username)

    def OpenBlockedUsersDialog(self):
        '''Opens blocked users dialog.
        '''
        self.OpenDialog('BLOCKEDUSERS')

    def OpenCallHistoryTab(self):
        '''Opens call history tab.
        '''
        self.OpenDialog('CALLHISTORY')

    def OpenConferenceDialog(self):
        '''Opens create conference dialog.
        '''
        self.OpenDialog('CONFERENCE')

    def OpenContactsTab(self):
        '''Opens contacts tab.
        '''
        self.OpenDialog('CONTACTS')

    def OpenDialog(self, Name, *Params):
        '''Open dialog.

        @param Name: Name
        @type Name: unicode
        @param Params: Params
        @type Params: ?
        '''
        self._Skype._DoCommand('OPEN %s %s' % (Name, ' '.join(Params)))

    def OpenDialpadTab(self):
        '''Opens dial pad tab.
        '''
        self.OpenDialog('DIALPAD')

    def OpenFileTransferDialog(self, Username, Folder):
        '''Opens file transfer dialog.

        @param Username: Username
        @type Username: unicode
        @param Folder: Folder
        @type Folder: unicode
        '''
        self.OpenDialog('FILETRANSFER', Username, 'IN %s' % Folder)

    def OpenGettingStartedWizard(self):
        '''Opens getting started wizard.
        '''
        self.OpenDialog('GETTINGSTARTED')

    def OpenImportContactsWizard(self):
        '''Opens import contacts wizard.
        '''
        self.OpenDialog('IMPORTCONTACTS')

    def OpenLiveTab(self):
        '''OpenLiveTab.
        '''
        self.OpenDialog('LIVETAB')

    def OpenMessageDialog(self, Username, Text=''):
        '''Opens "Send an IM Message" dialog.

        @param Username: Username
        @type Username: unicode
        @param Text: Text
        @type Text: unicode
        '''
        self.OpenDialog('IM', Username, Text)

    def OpenOptionsDialog(self, Page=''):
        '''Opens options dialog.

        @param Page: Page
        @type Page: ?
        '''
        self.OpenDialog('OPTIONS', Page)

    def OpenProfileDialog(self):
        '''Opens current user profile dialog.
        '''
        self.OpenDialog('PROFILE')

    def OpenSearchDialog(self):
        '''Opens search dialog.
        '''
        self.OpenDialog('SEARCH')

    def OpenSendContactsDialog(self, Username=''):
        '''Opens send contacts dialog.

        @param Username: Username
        @type Username: unicode
        '''
        self.OpenDialog('SENDCONTACTS', Username)

    def OpenSmsDialog(self, SmsId):
        '''Opens SMS window

        @param SmsId: SmsId
        @type SmsId: int
        '''
        self.OpenDialog('SMS', SmsId)

    def OpenUserInfoDialog(self, Username):
        '''Opens user information dialog.

        @param Username: Username
        @type Username: unicode
        '''
        self.OpenDialog('USERINFO', Username)

    def OpenVideoTestDialog(self):
        '''Opens video test dialog.
        '''
        self.OpenDialog('VIDEOTEST')

    def Shutdown(self):
        '''Closes Skype application.
        '''
        self._Skype._API.Shutdown()

    def Start(self, Minimized=False, Nosplash=False):
        '''Starts Skype application.

        @param Minimized: Minimized
        @type Minimized: bool
        @param Nosplash: Nosplash
        @type Nosplash: bool
        '''
        self._Skype._API.Start(Minimized, Nosplash)

    def _Get_Skype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise ISkypeError('Skype4Py internal error')

    _Skype = property(_Get_Skype)

    def _GetIsRunning(self):
        return self._Skype._API.IsRunning()

    IsRunning = property(_GetIsRunning,
    doc='''IsRunning.

    @type: bool
    ''')

    def _GetWallpaper(self):
        return self._Skype.Variable('WALLPAPER')

    def _SetWallpaper(self, value):
        self._Skype.Variable('WALLPAPER', value)

    Wallpaper = property(_GetWallpaper, _SetWallpaper,
    doc='''Wallpaper.

    @type: unicode
    ''')

    def _GetWindowState(self):
        return self._Skype.Variable('WINDOWSTATE')

    def _SetWindowState(self, value):
        self._Skype.Variable('WINDOWSTATE', value)

    WindowState = property(_GetWindowState, _SetWindowState,
    doc='''WindowState.

    @type: L{Window state<enums.wndUnknown>}
    ''')


class IPluginEvent(Cached):
    '''Represents an event displayed in Skype client.
    '''

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = unicode(Id)

    def Delete(self):
        '''Delete.
        '''
        self._Skype._DoCommand('DELETE EVENT %s' % self._Id)

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: unicode
    ''')


class IPluginMenuItem(Cached):
    '''Represents a menu item displayed in Skype client.
    '''

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
        '''Delete.
        '''
        self._Skype._DoCommand('DELETE MENU_ITEM %s' % self._Id)

    def _GetCaption(self):
        return self._Property('CAPTION')

    def _SetCaption(self, value):
        self._Property('CAPTION', value)

    Caption = property(_GetCaption, _SetCaption,
    doc='''Caption.

    @type: unicode
    ''')

    def _GetEnabled(self):
        return self._Property('ENABLED') == 'TRUE'

    def _SetEnabled(self, value):
        self._Property('ENABLED', cndexp(value, 'TRUE', 'FALSE'))

    Enabled = property(_GetEnabled, _SetEnabled,
    doc='''Enabled.

    @type: bool
    ''')

    def _GetHint(self):
        return self._Property('HINT')

    def _SetHint(self, value):
        self._Property('HINT', value)

    Hint = property(_GetHint, _SetHint,
    doc='''Hint.

    @type: unicode
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: unicode
    ''')
