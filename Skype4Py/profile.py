'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from enums import *
from utils import *
import time
import weakref


class IProfile(object):
    def __init__(self, Skype):
        self._SkypeRef = weakref.ref(Skype)

    def _GetSkype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise Exception()

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('PROFILE', '', PropName, Set)

    def getBirthday(self):
        value = self._Property('BIRTHDAY')
        if len(value) == 8:
            return time.mktime((int(value[:4]), int(value[4:6]), int(value[6:]), 0, 0, 0, -1, -1, -1))
        else:
            return None

    def _SetBirthday(self, value):
        if value:
            self._Property('BIRTHDAY', time.strftime('%Y%m%d', time.localtime(value)))
        else:
            self._Property('BIRTHDAY', 0)

    _Skype = property(_GetSkype)

    FullName = property(lambda self: self._Property('FULLNAME'), lambda self, value: self._Property('FULLNAME', value))
    Birthday = property(getBirthday, _SetBirthday)
    Sex = property(lambda self: self._Property('SEX'), lambda self, value: self._Property('SEX', value))
    Languages = property(lambda self: self._Property('LANGUAGES'), lambda self, value: self._Property('LANGUAGES', value))
    Country = property(lambda self: chop(self._Property('COUNTRY'))[0], lambda self, value: self._Property('COUNTRY', value))
    Province = property(lambda self: self._Property('PROVINCE'), lambda self, value: self._Property('PROVINCE', value))
    City = property(lambda self: self._Property('CITY'), lambda self, value: self._Property('CITY', value))
    PhoneHome = property(lambda self: self._Property('PHONE_HOME'), lambda self, value: self._Property('PHONE_HOME', value))
    PhoneOffice = property(lambda self: self._Property('PHONE_OFFICE'), lambda self, value: self._Property('PHONE_OFFICE', value))
    PhoneMobile = property(lambda self: self._Property('PHONE_MOBILE'), lambda self, value: self._Property('PHONE_MOBILE', value))
    Homepage = property(lambda self: self._Property('HOMEPAGE'), lambda self, value: self._Property('HOMEPAGE', value))
    About = property(lambda self: self._Property('ABOUT'), lambda self, value: self._Property('ABOUT', value))
    MoodText = property(lambda self: self._Property('MOOD_TEXT'), lambda self, value: self._Property('MOOD_TEXT', value))
    RichMoodText = property(lambda self: self._Property('RICH_MOOD_TEXT'), lambda self, value: self._Property('RICH_MOOD_TEXT', value))
    Timezone = property(lambda self: int(self._Property('TIMEZONE')), lambda self, value: self._Property('TIMEZONE', value))
    CallNoAnswerTimeout = property(lambda self: int(self._Property('CALL_NOANSWER_TIMEOUT')), lambda self, value: self._Property('CALL_NOANSWER_TIMEOUT', value))
    CallApplyCF = property(lambda self: self._Property('CALL_APPLY_CF') == 'TRUE', lambda self, value: self._Property('CALL_APPLY_CF', 'TRUE' if value else 'FALSE'))
    CallSendToVM = property(lambda self: self._Property('CALL_SEND_TO_VM') == 'TRUE', lambda self, value: self._Property('CALL_SEND_TO_VM', 'TRUE' if value else 'FALSE'))
    CallForwardRules = property(lambda self: self._Property('CALL_FORWARD_RULES'), lambda self, value: self._Property('CALL_FORWARD_RULES', value))
    Balance = property(lambda self: int(self._Property('PSTN_BALANCE')))
    BalanceCurrency = property(lambda self: self._Property('PSTN_BALANCE_CURRENCY'))
    BalanceToText = property(lambda self: u'%s %.2f' % (self.BalanceCurrency, self.Balance / 100))
    IPCountry = property(lambda self: self._Property('IPCOUNTRY'))
    ValidatedSmsNumbers = property(lambda self: self._Property('SMS_VALIDATED_NUMBERS'))
