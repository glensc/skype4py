'''
This faked module is used while building docs on windows
where dbus and gobject aren't available.
'''

class dbus(object):
    class mainloop(object):
        class glib(object):
            @staticmethod
            def DBusGMainLoop(*args, **kwargs):
                pass
    class service(object):
        class Object(object):
            pass
        @staticmethod
        def method(*args, **kwargs):
            return lambda *args, **kwargs: None
class gobject(object):
    @staticmethod
    def threads_init():
        pass
