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

    def Avatar(self, Id='1', newVal=''):
        self._Skype._Property('AVATAR', Id, newVal)

    def RingToneStatus(self, Id='1', Value=None):
        if Value == None:
            return self._Skype._Property('RINGTONE', Id, 'STATUS') == 'ON'
        return self._Skype._Property('RINGTONE', Id, 'STATUS', 'ON' if Value else 'OFF')

    def RingTone(self, Id='1', Value=None):
        return self._Skype._Property('RINGTONE', Id, '', Value)

    def ResetIdleTimer(self):
        self._Skype._DoCommand('RESETIDLETIMER')

    def LoadAvatarFromFile(self, Filename, AvatarId='1'):
        self._Skype._Property('AVATAR', Id, '', Filename)

    def SaveAvatarToFile(self, Filename, AvatarId='1'):
        self._Skype._Property('AVATAR', Id, Filename)

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

    # TODO
    #AutoAway
