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

    _Skype = property(_GetSkype)

    def _GetFullName(self):
        return self._Property('FULLNAME')

    def _SetFullName(self, value):
        self._Property('FULLNAME', value)

    FullName = property(_GetFullName, _SetFullName)

    def _GetBirthday(self):
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

    Birthday = property(_GetBirthday, _SetBirthday)

    def _GetSex(self):
        return self._Property('SEX')

    def _SetSex(self, value):
        self._Property('SEX', value)

    Sex = property(_GetSex, _SetSex)

    def _GetLanguages(self):
        return self._Property('LANGUAGES')

    def _SetLanguages(self, value):
        self._Property('LANGUAGES', value)

    Languages = property(_GetLanguages, _SetLanguages)

    def _GetCountry(self):
        return chop(self._Property('COUNTRY'))[0]

    def _SetCountry(self, value):
        self._Property('COUNTRY', value)

    Country = property(_GetCountry, _SetCountry)

    def _GetProvince(self):
        return self._Property('PROVINCE')

    def _SetProvince(self, value):
        self._Property('PROVINCE', value)

    Province = property(_GetProvince, _SetProvince)

    def _GetCity(self):
        return self._Property('CITY')

    def _SetCity(self, value):
        self._Property('CITY', value)

    City = property(_GetCity, _SetCity)

    def _GetPhoneHome(self):
        return self._Property('PHONE_HOME')

    def _SetPhoneHome(self, value):
        self._Property('PHONE_HOME', value)

    PhoneHome = property(_GetPhoneHome, _SetPhoneHome)

    def _GetPhoneOffice(self):
        return self._Property('PHONE_OFFICE')

    def _SetPhoneOffice(self, value):
        self._Property('PHONE_OFFICE', value)

    PhoneOffice = property(_GetPhoneOffice, _SetPhoneOffice)

    def _GetPhoneMobile(self):
        return self._Property('PHONE_MOBILE')

    def _SetPhoneMobile(self, value):
        self._Property('PHONE_MOBILE', value)

    PhoneMobile = property(_GetPhoneMobile, _SetPhoneMobile)

    def _GetHomepage(self):
        return self._Property('HOMEPAGE')

    def _SetHomepage(self, value):
        self._Property('HOMEPAGE', value)

    Homepage = property(_GetHomepage, _SetHomepage)

    def _GetAbout(self):
        return self._Property('ABOUT')

    def _SetAbout(self, value):
        self._Property('ABOUT', value)

    About = property(_GetAbout, _SetAbout)

    def _GetMoodText(self):
        return self._Property('MOOD_TEXT')

    def _SetMoodText(self, value):
        self._Property('MOOD_TEXT', value)

    MoodText = property(_GetMoodText, _SetMoodText)

    def _GetRichMoodText(self):
        return self._Property('RICH_MOOD_TEXT')

    def _SetRichMoodText(self, value):
        self._Property('RICH_MOOD_TEXT', value)

    RichMoodText = property(_GetRichMoodText, _SetRichMoodText)

    def _GetTimezone(self):
        return int(self._Property('TIMEZONE'))

    def _SetTimezone(self, value):
        self._Property('TIMEZONE', value)

    Timezone = property(_GetTimezone, _SetTimezone)

    def _GetCallNoAnswerTimeout(self):
        return int(self._Property('CALL_NOANSWER_TIMEOUT'))

    def _SetCallNoAnswerTimeout(self, value):
        self._Property('CALL_NOANSWER_TIMEOUT', value)

    CallNoAnswerTimeout = property(_GetCallNoAnswerTimeout, _SetCallNoAnswerTimeout)

    def _GetCallApplyCF(self):
        return self._Property('CALL_APPLY_CF') == 'TRUE'

    def _SetCallApplyCF(self, value):
        self._Property('CALL_APPLY_CF', cndexp(value, 'TRUE', 'FALSE'))

    CallApplyCF = property(_GetCallApplyCF, _SetCallApplyCF)

    def _GetCallSendToVM(self):
        return self._Property('CALL_SEND_TO_VM') == 'TRUE'

    def _SetCallSendToVM(self, value):
        self._Property('CALL_SEND_TO_VM', cndexp(value, 'TRUE', 'FALSE'))

    CallSendToVM = property(_GetCallSendToVM, _SetCallSendToVM)

    def _GetCallForwardRules(self):
        return self._Property('CALL_FORWARD_RULES')

    def _SetCallForwardRules(self, value):
        self._Property('CALL_FORWARD_RULES', value)

    CallForwardRules = property(_GetCallForwardRules, _SetCallForwardRules)

    def _GetBalance(self):
        return int(self._Property('PSTN_BALANCE'))

    Balance = property(_GetBalance)

    def _GetBalanceCurrency(self):
        return self._Property('PSTN_BALANCE_CURRENCY')

    BalanceCurrency = property(_GetBalanceCurrency)

    def _GetBalanceValue(self):
        return float(self._Property('PSTN_BALANCE')) / 100

    BalanceValue = property(_GetBalanceValue)

    def _GetBalanceToText(self):
        return (u'%s %.2f' % (self.BalanceCurrency, self.BalanceValue)).strip()

    BalanceToText = property(_GetBalanceToText)

    def _GetIPCountry(self):
        return self._Property('IPCOUNTRY')

    IPCountry = property(_GetIPCountry)

    def _GetValidatedSmsNumbers(self):
        return self._Property('SMS_VALIDATED_NUMBERS')

    ValidatedSmsNumbers = property(_GetValidatedSmsNumbers)
