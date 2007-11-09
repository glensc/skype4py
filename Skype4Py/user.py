'''Users and groups.
'''

from utils import *
from enums import *


class IUser(Cached):
    '''Represents a Skype user.
    '''

    def _Init(self, Handle, Skype):
        self._Skype = Skype
        self.Handle = unicode(Handle)

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('USER', self.Handle, PropName, Set, Cache)

    def SaveAvatarToFile(self, Filename, AvatarId=1):
        '''SaveAvatarToFile.

        @param Filename: Filename
        @type Filename: unicode
        @param AvatarId: AvatarId
        @type AvatarId: int
        '''
        s = 'USER %s AVATAR %s %s' % (self.Handle, AvatarId, Filename)
        self._Skype._DoCommand('GET %s' % s, s)

    def _GetAbout(self):
        return self._Property('ABOUT')

    About = property(_GetAbout,
    doc='''About.

    @type: unicode
    ''')

    def _GetAliases(self):
        return self._Property('ALIASES').split()

    Aliases = property(_GetAliases,
    doc='''Aliases.

    @type: ?
    ''')

    def _GetBirthday(self):
        value = self._Property('BIRTHDAY')
        if len(value) == 8:
            from datetime import date
            from time import strptime
            return date(*strptime(value, '%Y%m%d')[:3])

    Birthday = property(_GetBirthday,
    doc='''Birthday.

    @type: datetime.date
    ''')

    def _GetBuddyStatus(self):
        return int(self._Property('BUDDYSTATUS'))

    def _SetBuddyStatus(self, value):
        self._Property('BUDDYSTATUS', int(value))

    BuddyStatus = property(_GetBuddyStatus, _SetBuddyStatus,
    doc='''BuddyStatus.

    @type: ?
    ''')

    def _GetCanLeaveVoicemail(self):
        return self._Property('CAN_LEAVE_VM') == 'TRUE'

    CanLeaveVoicemail = property(_GetCanLeaveVoicemail,
    doc='''CanLeaveVoicemail.

    @type: ?
    ''')

    def _GetCity(self):
        return self._Property('CITY')

    City = property(_GetCity,
    doc='''City.

    @type: unicode
    ''')

    def _GetCountry(self):
        value = self._Property('COUNTRY')
        if value:
            if self._Skype.Protocol >= 4:
                value = chop(value)[-1]
        return value

    Country = property(_GetCountry,
    doc='''Country.

    @type: unicode
    ''')

    def _GetCountryCode(self):
        if self._Skype.Protocol < 4:
            return u''
        value = self._Property('COUNTRY')
        if value:
            value = chop(value)[0]
        return value

    CountryCode = property(_GetCountryCode,
    doc='''CountryCode.

    @type: ?
    ''')

    def _GetDisplayName(self):
        return self._Property('DISPLAYNAME')

    def _SetDisplayName(self, value):
        self._Property('DISPLAYNAME', value)

    DisplayName = property(_GetDisplayName, _SetDisplayName,
    doc='''DisplayName.

    @type: unicode
    ''')

    def _GetFullName(self):
        return self._Property('FULLNAME')

    FullName = property(_GetFullName,
    doc='''FullName.

    @type: unicode
    ''')

    def _GetHasCallEquipment(self):
        return self._Property('HASCALLEQUIPMENT') == 'TRUE'

    HasCallEquipment = property(_GetHasCallEquipment,
    doc='''HasCallEquipment.

    @type: bool
    ''')

    def _GetHomepage(self):
        return self._Property('HOMEPAGE')

    Homepage = property(_GetHomepage,
    doc='''Homepage.

    @type: unicode
    ''')

    def _GetIsAuthorized(self):
        return self._Property('ISAUTHORIZED') == 'TRUE'

    def _SetIsAuthorized(self, value):
        self._Property('ISAUTHORIZED', cndexp(value, 'TRUE', 'FALSE'))

    IsAuthorized = property(_GetIsAuthorized, _SetIsAuthorized,
    doc='''IsAuthorized.

    @type: bool
    ''')

    def _GetIsBlocked(self):
        return self._Property('ISBLOCKED') == 'TRUE'

    def _SetIsBlocked(self, value):
        self._Property('ISBLOCKED', cndexp(value, 'TRUE', 'FALSE'))

    IsBlocked = property(_GetIsBlocked, _SetIsBlocked,
    doc='''IsBlocked.

    @type: bool
    ''')

    def _GetIsCallForwardActive(self):
        return self._Property('IS_CF_ACTIVE') == 'TRUE'

    IsCallForwardActive = property(_GetIsCallForwardActive,
    doc='''IsCallForwardActive.

    @type: bool
    ''')

    def _GetIsSkypeOutContact(self):
        return self.OnlineStatus == olsSkypeOut

    IsSkypeOutContact = property(_GetIsSkypeOutContact,
    doc='''IsSkypeOutContact.

    @type: bool
    ''')

    def _GetIsVideoCapable(self):
        return self._Property('IS_VIDEO_CAPABLE') == 'TRUE'

    IsVideoCapable = property(_GetIsVideoCapable,
    doc='''IsVideoCapable.

    @type: bool
    ''')

    def _GetIsVoicemailCapable(self):
        return self._Property('IS_VOICEMAIL_CAPABLE') == 'TRUE'

    IsVoicemailCapable = property(_GetIsVoicemailCapable,
    doc='''IsVoicemailCapable.

    @type: bool
    ''')

    def _GetLanguage(self):
        value = self._Property('LANGUAGE')
        if value:
            if self._Skype.Protocol >= 4:
                value = chop(value)[-1]
        return value

    Language = property(_GetLanguage,
    doc='''Language.

    @type: ?
    ''')

    def _GetLanguageCode(self):
        if self._Skype.Protocol < 4:
            return u''
        value = self._Property('LANGUAGE')
        if value:
            value = chop(value)[0]
        return value

    LanguageCode = property(_GetLanguageCode,
    doc='''LanguageCode.

    @type: ?
    ''')

    def _GetLastOnline(self):
        return float(self._Property('LASTONLINETIMESTAMP'))

    LastOnline = property(_GetLastOnline,
    doc='''LastOnline.

    @type: ?
    ''')

    def _GetLastOnlineDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.LastOnline)

    LastOnlineDatetime = property(_GetLastOnlineDatetime,
    doc='''LastOnlineDatetime.

    @type: datetime.datetime
    ''')

    def _GetMoodText(self):
        return self._Property('MOOD_TEXT')

    MoodText = property(_GetMoodText,
    doc='''MoodText.

    @type: unicode
    ''')

    def _GetNumberOfAuthBuddies(self):
        return int(self._Property('NROF_AUTHED_BUDDIES'))

    NumberOfAuthBuddies = property(_GetNumberOfAuthBuddies,
    doc='''NumberOfAuthBuddies.

    @type: ?
    ''')

    def _GetOnlineStatus(self):
        return self._Property('ONLINESTATUS')

    OnlineStatus = property(_GetOnlineStatus,
    doc='''OnlineStatus.

    @type: ?
    ''')

    def _GetPhoneHome(self):
        return self._Property('PHONE_HOME')

    PhoneHome = property(_GetPhoneHome,
    doc='''PhoneHome.

    @type: unicode
    ''')

    def _GetPhoneMobile(self):
        return self._Property('PHONE_MOBILE')

    PhoneMobile = property(_GetPhoneMobile,
    doc='''PhoneMobile.

    @type: unicode
    ''')

    def _GetPhoneOffice(self):
        return self._Property('PHONE_OFFICE')

    PhoneOffice = property(_GetPhoneOffice,
    doc='''PhoneOffice.

    @type: unicode
    ''')

    def _GetProvince(self):
        return self._Property('PROVINCE')

    Province = property(_GetProvince,
    doc='''Province.

    @type: unicode
    ''')

    def _GetReceivedAuthRequest(self):
        return self._Property('RECEIVEDAUTHREQUEST')

    ReceivedAuthRequest = property(_GetReceivedAuthRequest,
    doc='''ReceivedAuthRequest.

    @type: ?
    ''')

    def _GetRichMoodText(self):
        return self._Property('RICH_MOOD_TEXT')

    RichMoodText = property(_GetRichMoodText,
    doc='''RichMoodText.

    @type: unicode
    ''')

    def _GetSex(self):
        return self._Property('SEX')

    Sex = property(_GetSex,
    doc='''Sex.

    @type: ?
    ''')

    def _GetSpeedDial(self):
        return self._Property('SPEEDDIAL')

    def _SetSpeedDial(self, value):
        self._Property('SPEEDDIAL', value)

    SpeedDial = property(_GetSpeedDial, _SetSpeedDial,
    doc='''SpeedDial.

    @type: ?
    ''')

    def _GetTimezone(self):
        return int(self._Property('TIMEZONE'))

    Timezone = property(_GetTimezone,
    doc='''Timezone.

    @type: ?
    ''')


class IGroup(Cached):
    '''Represents a group of Skype users.
    '''

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('GROUP', self._Id, AlterName, Args)

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('GROUP', self._Id, PropName, Value, Cache)

    def Accept(self):
        '''Accepts a shared group.
        '''
        self._Alter('ACCEPT')

    def AddUser(self, Username):
        '''Adds new a user or PSTN number to group.

        @param Username: Username
        @type Username: unicode
        '''
        self._Alter('ADDUSER', Username)

    def Decline(self):
        '''Decline a shared group.
        '''
        self._Alter('DECLINE')

    def RemoveUser(self, Username):
        '''Removes a user or PSTN number from group.

        @param Username: Username
        @type Username: unicode
        '''
        self._Alter('REMOVEUSER', Username)

    def Share(self, MessageText=''):
        '''Shares a group.

        @param MessageText: MessageText
        @type MessageText: unicode
        '''
        self._Alter('SHARE', MessageText)

    def _GetCustomGroupId(self):
        return self._Property('CUSTOM_GROUP_ID')

    CustomGroupId = property(_GetCustomGroupId,
    doc='''CustomGroupId.

    @type: ?
    ''')

    def _GetDisplayName(self):
        return self._Property('DISPLAYNAME')

    def _SetDisplayName(self, value):
        self._Property('DISPLAYNAME', value)

    DisplayName = property(_GetDisplayName, _SetDisplayName,
    doc='''DisplayName.

    @type: unicode
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Id.

    @type: ?
    ''')

    def _GetIsExpanded(self):
        return self._Property('EXPANDED') == 'TRUE'

    IsExpanded = property(_GetIsExpanded,
    doc='''IsExpanded.

    @type: bool
    ''')

    def _GetIsVisible(self):
        return self._Property('VISIBLE') == 'TRUE'

    IsVisible = property(_GetIsVisible,
    doc='''IsVisible.

    @type: bool
    ''')

    def _GetOnlineUsers(self):
        return tuple(x for x in self.Users if x.OnlineStatus == olsOnline)

    OnlineUsers = property(_GetOnlineUsers,
    doc='''OnlineUsers.

    @type: tuple of L{IUser}
    ''')

    def _GetType(self):
        return self._Property('TYPE')

    Type = property(_GetType,
    doc='''Type.

    @type: ?
    ''')

    def _GetUsers(self):
        return tuple(IUser(x, self._Skype) for x in esplit(self._Property('USERS', Cache=False), ', '))

    Users = property(_GetUsers,
    doc='''Users.

    @type: tuple of L{IUser}
    ''')
