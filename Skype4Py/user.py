'''Users and groups.
'''

from utils import *
from enums import *


class IUser(Cached):
    '''Represents a Skype user.
    '''

    def __repr__(self):
        return '<%s with Handle=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Handle))

    def _Init(self, Handle, Skype):
        self._Skype = Skype
        self._Handle = str(Handle)

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Skype._Property('USER', self.Handle, PropName, Set, Cache)

    def SaveAvatarToFile(self, Filename, AvatarId=1):
        '''Saves user avatar to a file.

        @param Filename: Destination path.
        @type Filename: str
        @param AvatarId: Avatar Id.
        @type AvatarId: int
        '''
        s = 'USER %s AVATAR %s %s' % (self.Handle, AvatarId, path2unicode(Filename))
        self._Skype._DoCommand('GET %s' % s, s)

    def SetBuddyStatusPendingAuthorization(self, Text=u''):
        '''Sets the BuddyStaus property to L{budPendingAuthorization<enums.budPendingAuthorization>}
        additionaly specifying the authorization text.
        
        @param Text: The authorization text.
        @type Text: unicode
        @see: L{BuddyStatus}
        '''
        self._Property('BUDDYSTATUS', '%d %s' % (budPendingAuthorization, tounicode(Text)), Cache=False)

    def _GetAbout(self):
        return self._Property('ABOUT')

    About = property(_GetAbout,
    doc='''About text of the user.

    @type: unicode
    ''')

    def _GetAliases(self):
        return tuple([str(x) for x in esplit(self._Property('ALIASES'))])

    Aliases = property(_GetAliases,
    doc='''Aliases of the user.

    @type: tuple of str
    ''')

    def _GetBirthday(self):
        value = self._Property('BIRTHDAY')
        if len(value) == 8:
            from datetime import date
            from time import strptime
            return date(*strptime(value, '%Y%m%d')[:3])

    Birthday = property(_GetBirthday,
    doc='''Birthday of the user.

    @type: datetime.date
    ''')

    def _GetBuddyStatus(self):
        return int(self._Property('BUDDYSTATUS'))

    def _SetBuddyStatus(self, value):
        self._Property('BUDDYSTATUS', int(value), Cache=False)

    BuddyStatus = property(_GetBuddyStatus, _SetBuddyStatus,
    doc='''Buddy status of the user.

    @type: L{Buddy status<enums.budUnknown>}
    ''')

    def _GetCanLeaveVoicemail(self):
        return (self._Property('CAN_LEAVE_VM') == 'TRUE')

    CanLeaveVoicemail = property(_GetCanLeaveVoicemail,
    doc='''Tells if it is possible to send voicemail to the user.

    @type: bool
    ''')

    def _GetCity(self):
        return self._Property('CITY')

    City = property(_GetCity,
    doc='''City of the user.

    @type: unicode
    ''')

    def _GetCountry(self):
        value = self._Property('COUNTRY')
        if value:
            if self._Skype.Protocol >= 4:
                value = chop(value)[-1]
        return value

    Country = property(_GetCountry,
    doc='''Country of the user.

    @type: unicode
    ''')

    def _GetCountryCode(self):
        if self._Skype.Protocol < 4:
            return ''
        value = self._Property('COUNTRY')
        if value:
            value = chop(value)[0]
        return str(value)

    CountryCode = property(_GetCountryCode,
    doc='''ISO country code of the user.

    @type: str
    ''')

    def _GetDisplayName(self):
        return self._Property('DISPLAYNAME')

    def _SetDisplayName(self, value):
        self._Property('DISPLAYNAME', value)

    DisplayName = property(_GetDisplayName, _SetDisplayName,
    doc='''Display name of the user.

    @type: unicode
    ''')

    def _GetHandle(self):
        return self._Handle

    Handle = property(_GetHandle,
    doc='''Skypename of the user.

    @type: unicode
    ''')

    def _GetFullName(self):
        return self._Property('FULLNAME')

    FullName = property(_GetFullName,
    doc='''Full name of the user.

    @type: unicode
    ''')

    def _GetHasCallEquipment(self):
        return self._Property('HASCALLEQUIPMENT') == 'TRUE'

    HasCallEquipment = property(_GetHasCallEquipment,
    doc='''Tells if the user has call equipment.

    @type: bool
    ''')

    def _GetHomepage(self):
        return str(self._Property('HOMEPAGE'))

    Homepage = property(_GetHomepage,
    doc='''Homepage URL of the user.

    @type: str
    ''')

    def _GetIsAuthorized(self):
        return (self._Property('ISAUTHORIZED') == 'TRUE')

    def _SetIsAuthorized(self, value):
        self._Property('ISAUTHORIZED', cndexp(value, 'TRUE', 'FALSE'))

    IsAuthorized = property(_GetIsAuthorized, _SetIsAuthorized,
    doc='''Tells if the user is authorized to contact us.

    @type: bool
    ''')

    def _GetIsBlocked(self):
        return (self._Property('ISBLOCKED') == 'TRUE')

    def _SetIsBlocked(self, value):
        self._Property('ISBLOCKED', cndexp(value, 'TRUE', 'FALSE'))

    IsBlocked = property(_GetIsBlocked, _SetIsBlocked,
    doc='''Tells whether this user is blocked or not.

    @type: bool
    ''')

    def _GetIsCallForwardActive(self):
        return (self._Property('IS_CF_ACTIVE') == 'TRUE')

    IsCallForwardActive = property(_GetIsCallForwardActive,
    doc='''Tells whether the user has Call Forwarding activated or not.

    @type: bool
    ''')

    def _GetIsSkypeOutContact(self):
        return (self.OnlineStatus == olsSkypeOut)

    IsSkypeOutContact = property(_GetIsSkypeOutContact,
    doc='''Tells whether a user is a SkypeOut contact.

    @type: bool
    ''')

    def _GetIsVideoCapable(self):
        return (self._Property('IS_VIDEO_CAPABLE') == 'TRUE')

    IsVideoCapable = property(_GetIsVideoCapable,
    doc='''Tells if the user has video capability.

    @type: bool
    ''')

    def _GetIsVoicemailCapable(self):
        return (self._Property('IS_VOICEMAIL_CAPABLE') == 'TRUE')

    IsVoicemailCapable = property(_GetIsVoicemailCapable,
    doc='''Tells if the user has voicemail capability.

    @type: bool
    ''')

    def _GetLanguage(self):
        value = self._Property('LANGUAGE')
        if value:
            if self._Skype.Protocol >= 4:
                value = chop(value)[-1]
        return value

    Language = property(_GetLanguage,
    doc='''The language of the user.

    @type: unicode
    ''')

    def _GetLanguageCode(self):
        if self._Skype.Protocol < 4:
            return u''
        value = self._Property('LANGUAGE')
        if value:
            value = chop(value)[0]
        return str(value)

    LanguageCode = property(_GetLanguageCode,
    doc='''The ISO language code of the user.

    @type: str
    ''')

    def _GetLastOnline(self):
        return float(self._Property('LASTONLINETIMESTAMP'))

    LastOnline = property(_GetLastOnline,
    doc='''The time when a user was last online as a timestamp.

    @type: float
    @see: L{LastOnlineDatetime}
    ''')

    def _GetLastOnlineDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.LastOnline)

    LastOnlineDatetime = property(_GetLastOnlineDatetime,
    doc='''The time when a user was last online as a datetime.

    @type: datetime.datetime
    @see: L{LastOnline}
    ''')

    def _GetMoodText(self):
        return self._Property('MOOD_TEXT')

    MoodText = property(_GetMoodText,
    doc='''Mood text of the user.

    @type: unicode
    ''')

    def _GetNumberOfAuthBuddies(self):
        return int(self._Property('NROF_AUTHED_BUDDIES'))

    NumberOfAuthBuddies = property(_GetNumberOfAuthBuddies,
    doc='''Number of authenticated buddies in user's contact list.

    @type: int
    ''')

    def _GetOnlineStatus(self):
        return str(self._Property('ONLINESTATUS'))

    OnlineStatus = property(_GetOnlineStatus,
    doc='''Online status of the user.

    @type: L{Online status<enums.olsUnknown>}
    ''')

    def _GetPhoneHome(self):
        return self._Property('PHONE_HOME')

    PhoneHome = property(_GetPhoneHome,
    doc='''Home telephone number of the user.

    @type: unicode
    ''')

    def _GetPhoneMobile(self):
        return self._Property('PHONE_MOBILE')

    PhoneMobile = property(_GetPhoneMobile,
    doc='''Mobile telephone number of the user.

    @type: unicode
    ''')

    def _GetPhoneOffice(self):
        return self._Property('PHONE_OFFICE')

    PhoneOffice = property(_GetPhoneOffice,
    doc='''Office telephone number of the user.

    @type: unicode
    ''')

    def _GetProvince(self):
        return self._Property('PROVINCE')

    Province = property(_GetProvince,
    doc='''Province of the user.

    @type: unicode
    ''')

    def _GetReceivedAuthRequest(self):
        return self._Property('RECEIVEDAUTHREQUEST')

    ReceivedAuthRequest = property(_GetReceivedAuthRequest,
    doc='''Text message for authorization request. Available only when user asks for authorization.

    @type: unicode
    ''')

    def _GetRichMoodText(self):
        return self._Property('RICH_MOOD_TEXT')

    RichMoodText = property(_GetRichMoodText,
    doc='''Advanced version of L{MoodText}.

    @type: unicode
    @see: U{https://developer.skype.com/Docs/ApiDoc/SET_PROFILE_RICH_MOOD_TEXT}
    ''')

    def _GetSex(self):
        return str(self._Property('SEX'))

    Sex = property(_GetSex,
    doc='''Sex of the user.

    @type: L{User sex<enums.usexUnknown>}
    ''')

    def _GetSpeedDial(self):
        return self._Property('SPEEDDIAL')

    def _SetSpeedDial(self, value):
        self._Property('SPEEDDIAL', value)

    SpeedDial = property(_GetSpeedDial, _SetSpeedDial,
    doc='''Speed-dial code assigned to the user.

    @type: unicode
    ''')

    def _GetTimezone(self):
        return int(self._Property('TIMEZONE'))

    Timezone = property(_GetTimezone,
    doc='''Timezone of the user in minutes from GMT.

    @type: int
    ''')


class IGroup(Cached):
    '''Represents a group of Skype users.
    '''

    def __repr__(self):
        return '<%s with Id=%s>' % (Cached.__repr__(self)[1:-1], repr(self.Id))

    def _Alter(self, AlterName, Args=None):
        return self._Skype._Alter('GROUP', self._Id, AlterName, Args)

    def _Init(self, Id, Skype):
        self._Skype = Skype
        self._Id = int(Id)

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Skype._Property('GROUP', self._Id, PropName, Value, Cache)

    def Accept(self):
        '''Accepts an invitation to join a shared contact group.
        '''
        self._Alter('ACCEPT')

    def AddUser(self, Username):
        '''Adds new a user to the group.

        @param Username: Skypename of the new user.
        @type Username: str
        '''
        self._Alter('ADDUSER', Username)

    def Decline(self):
        '''Declines an invitation to join a shared contact group.
        '''
        self._Alter('DECLINE')

    def RemoveUser(self, Username):
        '''Removes a user from the group.

        @param Username: Skypename of the user.
        @type Username: str
        '''
        self._Alter('REMOVEUSER', Username)

    def Share(self, MessageText=''):
        '''Shares a contact group.

        @param MessageText: Message text for group members.
        @type MessageText: unicode
        '''
        self._Alter('SHARE', MessageText)

    def _GetCustomGroupId(self):
        return str(self._Property('CUSTOM_GROUP_ID'))

    CustomGroupId = property(_GetCustomGroupId,
    doc='''Persistent group ID. The custom group ID is a persistent value that does not change.

    @type: str
    ''')

    def _GetDisplayName(self):
        return self._Property('DISPLAYNAME')

    def _SetDisplayName(self, value):
        self._Property('DISPLAYNAME', value)

    DisplayName = property(_GetDisplayName, _SetDisplayName,
    doc='''Display name of the group.

    @type: unicode
    ''')

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc='''Group Id.

    @type: int
    ''')

    def _GetIsExpanded(self):
        return self._Property('EXPANDED') == 'TRUE'

    IsExpanded = property(_GetIsExpanded,
    doc='''Tells if the group is expanded in the client.

    @type: bool
    ''')

    def _GetIsVisible(self):
        return self._Property('VISIBLE') == 'TRUE'

    IsVisible = property(_GetIsVisible,
    doc='''Tells if the group is visible in the client.

    @type: bool
    ''')

    def _GetOnlineUsers(self):
        return tuple([x for x in self.Users if x.OnlineStatus == olsOnline])

    OnlineUsers = property(_GetOnlineUsers,
    doc='''Users of the group that are online

    @type: tuple of L{IUser}
    ''')

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc='''Group type.

    @type: L{Group type<enums.grpUnknown>}
    ''')

    def _GetUsers(self):
        return tuple([IUser(x, self._Skype) for x in esplit(self._Property('USERS', Cache=False), ', ')])

    Users = property(_GetUsers,
    doc='''Users in this group.

    @type: tuple of L{IUser}
    ''')
