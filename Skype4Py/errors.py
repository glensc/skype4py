
class ISkypeAPIError(Exception):
    def __init__(self, errstr):
        Exception.__init__(self, str(errstr))


class ISkypeError(Exception):
    def __init__(self, errno, errstr):
        Exception.__init__(self, int(errno), str(errstr))

    def __str__(self):
        return '[Errno %d] %s' % (self[0], self[1])
