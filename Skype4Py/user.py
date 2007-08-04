
from utils import *
from enums import *


class IUser(Cached):
    def _Init(self, Handle, Skype):
        self._Skype = Skype
        self.Handle = unicode(Handle)

    def _Property(self, PropName, Value=None):
        return self._Skype._Property('USER', self.Handle, PropName, Value)

    def _GetBirthday(self):
        value = self._Property('BIRTHDAY')
        if len(value) == 8:
            return time.mktime((int(value[:4]), int(value[4:6]), int(value[6:]), 0, 0, 0, -1, -1, -1))
        else:
            return None

    def _GetCountry(self):
        value = self._Property('COUNTRY')
        if self._Skype.Protocol >= 4:
            value = chop(value)[1]
        return value

    def _GetCountryCode(self):
        if self._Skype.API.Protocol < 4:
            return ''
        value = self._Property('COUNTRY')
        return chop(value)[0]

    def _GetLanguage(self):
        value = self._Property('LANGUAGE')
        if self._Skype.API.Protocol >= 4:
            value = chop(value)[1]
        return value

    def _GetLanguageCode(self):
        if self._Skype.API.Protocol < 4:
            return ''
        value = self._Property('LANGUAGE')
        return chop(value)[0]

    FullName = property(lambda self: self._Property('FULLNAME'))
    Birthday = property(_GetBirthday)
    Sex = property(lambda self: TUserSex(self._Property('SEX')))
    Country = property(_GetCountry)
    Province = property(lambda self: self._Property('PROVINCE'))
    City = property(lambda self: self._Property('CITY'))
    PhoneHome = property(lambda self: self._Property('PHONE_HOME'))
    PhoneOffice = property(lambda self: self._Property('PHONE_OFFICE'))
    PhoneMobile = property(lambda self: self._Property('PHONE_MOBILE'))
    Homepage = property(lambda self: self._Property('HOMEPAGE'))
    About = property(lambda self: self._Property('ABOUT'))
    HasCallEquipment = property(lambda self: self._Property('HASCALLEQUIPMENT') == 'TRUE')
    BuddyStatus = property(lambda self: TBuddyStatus(int(self._Property('BUDDYSTATUS'))),
                           lambda self, value: self._Property('BUDDYSTATUS', int(value)))
    IsAuthorized = property(lambda self: self._Property('ISAUTHORIZED') == 'TRUE', \
                            lambda self, value: self._Property('ISAUTHORIZED', 'TRUE' if value else 'FALSE'))
    IsBlocked = property(lambda self: self._Property('ISBLOCKED') == 'TRUE',
                         lambda self, value: self._Property('ISBLOCKED', 'TRUE' if value else 'FALSE'))
    DisplayName = property(lambda self: self._Property('DISPLAYNAME'),
                           lambda self, value: self._Property('DISPLAYNAME', value))
    OnlineStatus = property(lambda self: TOnlineStatus(self._Property('ONLINESTATUS')))
    LastOnline = property(lambda self: float(self._Property('LASTONLINETIMESTAMP')))
    CountryCode = property(_GetCountryCode)
    ReceivedAuthRequest = property(lambda self: self._Property('RECEIVEDAUTHREQUEST'))
    SpeedDial = property(lambda self: self._Property('SPEEDDIAL'),
                         lambda self, value: self._Property('SPEEDDIAL', value))
    CanLeaveVoicemail = property(lambda self: self._Property('CAN_LEAVE_VM') == 'TRUE')
    MoodText = property(lambda self: self._Property('MOOD_TEXT'))
    Aliases = property(lambda self: self._Property('ALIASES').split())
    Timezone = property(lambda self: int(self._Property('TIMEZONE')))
    IsCallForwardActive = property(lambda self: self._Property('IS_CF_ACTIVE') == 'TRUE')
    Language = property(_GetLanguage)
    LanguageCode = property(_GetLanguageCode)
    IsVideoCapable = property(lambda self: self._Property('IS_VIDEO_CAPABLE') == 'TRUE')
    IsSkypeOutContact = property() # property(lambda self: self._Property('') == 'TRUE')
    NumberOfAuthBuddies = property(lambda self: int(self._Property('NROF_AUTHED_BUDDIES')))
    RichMoodText = property(lambda self: self._Property('RICH_MOOD_TEXT'))


class IGroup(Cached):
    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('GROUP', self._Id, PropName, Value, Cache)

    def _Alter(self, AlterName, Args=None):
        return self._Skype.Alter('GROUP', self._Id, AlterName, Args)

    def AddUser(self, Username):
        self._Alter('ADDUSER', Username)

    def RemoveUser(self, Username):
        self._Alter('REMOVEUSER', Username)

    def Share(self, MessageText=''):
        self._Alter('SHARE', MessageText)

    def Accept(self):
        self._Alter('ACCEPT')

    def Decline(self):
        self._Alter('DECLINE')

    def _GetOnlineUsers(self):
        online = []
        for u in self.Users:
            if u.OnlineStatus == TOnlineStatus.olsOnline:
                online.append(u)
        return u

    Id = property(lambda self: self._Id)
    Type = property(lambda self: TGroupType(self._Property('TYPE')))
    CustomGroupId = property(lambda self: self._Property('CUSTOM_GROUP_ID'))
    DisplayName = property(lambda self: self._Property('DISPLAYNAME'), lambda self, value: self._Property('DISPLAYNAME', value))
    Users = property(lambda self: map(lambda x: IUser(x, self._Skype), esplit(users, ', ')))
    OnlineUsers = property(_GetOnlineUsers)
    IsVisible = property(lambda self: self._Property('VISIBLE') == 'TRUE')
    IsExpanded = property(lambda self: self._Property('EXPANDED') == 'TRUE')
