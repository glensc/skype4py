'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from utils import *


class IPluginEvent(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = unicode(Id)

    def Delete(self):
        self._Skype._DoCommand('DELETE EVENT %s' % self._Id)

    Id = property(lambda self: self._Id)


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
            self._CacheDict['ENABLED'] = u'TRUE' if Enabled else u'FALSE'

    def _Property(self, PropName, Set=None):
        if Set == None:
            return self._CacheDict[PropName]
        self._Skype._Property('MENU_ITEM', self._Id, PropName, Set)
        self._CacheDict[PropName] = unicode(Set)

    def Delete(self):
        self._Skype._DoCommand('DELETE MENU_ITEM %s' % self._Id)

    Id = property(lambda self: self._Id)
    Caption = property(lambda self: self._Property('CAPTION'), lambda self, value: self._Property('CAPTION', value))
    Hint = property(lambda self: self._Property('HINT'), lambda self, value: self._Property('HINT', value))
    Enabled = property(lambda self: self._Property('ENABLED') == 'TRUE',
                       lambda self, value: self._Property('ENABLED', 'TRUE' if value else 'FALSE'))
