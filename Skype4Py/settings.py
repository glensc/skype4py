'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import weakref
import sys
from utils import *


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
        return self._Skype._Property('RINGTONE', Id, 'STATUS', cndexp(Set, 'ON', 'OFF'))

    def RingTone(self, Id='1', Set=None):
        '''Returns/sets ringtone.'''
        return self._Skype._Property('RINGTONE', Id, '', Set)

    def ResetIdleTimer(self):
        self._Skype._DoCommand('RESETIDLETIMER')

    def LoadAvatarFromFile(self, Filename, AvatarId='1'):
        '''Loads user avatar picture from file.'''
        s = 'AVATAR %s %s' % (AvatarId, Filename.decode(sys.getfilesystemencoding()))
        self._Skype._DoCommand('SET %s' % s, s)

    def SaveAvatarToFile(self, Filename, AvatarId='1'):
        '''Saves user avatar picture to file.'''
        s = 'AVATAR %s %s' % (AvatarId, Filename.decode(sys.getfilesystemencoding()))
        self._Skype._DoCommand('GET %s' % s, s)

    _Skype = property(_GetSkype)

    def _GetAudioIn(self):
        return self._Skype.Variable('AUDIO_IN')

    def _SetAudioIn(self, value):
        self._Skype.Variable('AUDIO_IN', value)

    AudioIn = property(_GetAudioIn, _SetAudioIn)

    def _GetAudioOut(self):
        return self._Skype.Variable('AUDIO_OUT')

    def _SetAudioOut(self, value):
        self._Skype.Variable('AUDIO_OUT', value)

    AudioOut = property(_GetAudioOut, _SetAudioOut)

    def _GetRinger(self):
        return self._Skype.Variable('RINGER')

    def _SetRinger(self, value):
        self._Skype.Variable('RINGER', value)

    Ringer = property(_GetRinger, _SetRinger)

    def _GetVideoIn(self):
        return self._Skype.Variable('VIDEO_IN')

    def _SetVideoIn(self, value):
        self._Skype.Variable('VIDEO_IN', value)

    VideoIn = property(_GetVideoIn, _SetVideoIn)

    def _GetPCSpeaker(self):
        return self._Skype.Variable('PCSPEAKER') == 'ON'

    def _SetPCSpeaker(self, value):
        self._Skype.Variable('PCSPEAKER', 'ON' if value else 'OFF')

    PCSpeaker = property(_GetPCSpeaker, _SetPCSpeaker)

    def _GetAGC(self):
        return self._Skype.Variable('AGC') == 'ON'

    def _SetAGC(self, value):
        self._Skype.Variable('AGC', 'ON' if value else 'OFF')

    AGC = property(_GetAGC, _SetAGC)

    def _GetAEC(self):
        return self._Skype.Variable('AEC') == 'ON'

    def _SetAEC(self, value):
        self._Skype.Variable('AEC', 'ON' if value else 'OFF')

    AEC = property(_GetAEC, _SetAEC)

    def _GetLanguage(self):
        return self._Skype.Variable('UI_LANGUAGE')

    def _SetLanguage(self, value):
        self._Skype.Variable('UI_LANGUAGE', value)

    Language = property(_GetLanguage, _SetLanguage)

    def _GetAutoAway(self):
        return self._Skype.Variable('AUTOAWAY') == 'ON'

    def _SetAutoAway(self, value):
        self._Skype.Variable('AUTOAWAY', 'ON' if value else 'OFF')

    AutoAway = property(_GetAutoAway, _SetAutoAway)
