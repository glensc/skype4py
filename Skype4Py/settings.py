'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import weakref


class ISettings(object):
    def __init__(self, Skype):
        self._SkypeRef = weakref.ref(Skype)

    def _GetSkype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise Exception()

    def Avatar(self, Id='1', Set=None):
        '''Sets user avatar picture from file.'''
        if Set == None:
            raise TypeError('Argument \'Set\' is mandatory!')
        self.LoadAvatarFromFile(Set, Id)

    def RingToneStatus(self, Id='1', Set=None):
        '''Returns/sets ringtone status.'''
        if Set == None:
            return self._Skype._Property('RINGTONE', Id, 'STATUS') == 'ON'
        return self._Skype._Property('RINGTONE', Id, 'STATUS', 'ON' if Set else 'OFF')

    def RingTone(self, Id='1', Set=None):
        '''Returns/sets ringtone.'''
        return self._Skype._Property('RINGTONE', Id, '', Set)

    def ResetIdleTimer(self):
        self._Skype._DoCommand('RESETIDLETIMER')

    def LoadAvatarFromFile(self, Filename, AvatarId='1'):
        '''Loads user avatar picture from file.'''
        s = 'AVATAR %s %s' % (AvatarId, Filename)
        self._Skype._DoCommand('SET %s' % s, s)

    def SaveAvatarToFile(self, Filename, AvatarId='1'):
        '''Saves user avatar picture to file.'''
        s = 'AVATAR %s %s' % (AvatarId, Filename)
        self._Skype._DoCommand('GET %s' % s, s)

    _Skype = property(_GetSkype)

    AudioIn = property(lambda self: self._Skype.Variable('AUDIO_IN'),
                       lambda self, value: self._Skype.Variable('AUDIO_IN', value))
    AudioOut = property(lambda self: self._Skype.Variable('AUDIO_OUT'),
                        lambda self, value: self._Skype.Variable('AUDIO_OUT', value))
    Ringer = property(lambda self: self._Skype.Variable('RINGER'),
                        lambda self, value: self._Skype.Variable('RINGER', value))
    VideoIn = property(lambda self: self._Skype.Variable('VIDEO_IN'),
                       lambda self, value: self._Skype.Variable('VIDEO_IN', value))
    PCSpeaker = property(lambda self: self._Skype.Variable('PCSPEAKER') == 'ON',
                         lambda self, value: self._Skype.Variable('PCSPEAKER', 'ON' if value else 'OFF'))
    AGC = property(lambda self: self._Skype.Variable('AGC') == 'ON',
                   lambda self, value: self._Skype.Variable('AGC', 'ON' if value else 'OFF'))
    AEC = property(lambda self: self._Skype.Variable('AEC') == 'ON',
                   lambda self, value: self._Skype.Variable('AEC', 'ON' if value else 'OFF'))
    Language = property(lambda self: self._Skype.Variable('UI_LANGUAGE'),
                        lambda self, value: self._Skype.Variable('UI_LANGUAGE', value))
    AutoAway = property(lambda self: self._Skype.Variable('AUTOAWAY') == 'ON',
                        lambda self, value: self._Skype.Variable('AUTOAWAY', 'ON' if value else 'OFF'))

