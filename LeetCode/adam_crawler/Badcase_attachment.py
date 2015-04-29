import urllib2
import time
from functools import wraps
def retry(ExceptionToCheck, tries = 3, delay = 2, backoff = 1,logger = None):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries,mdelay = 3,delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck,e:
                    print "%s,retry in %s seconds!" % (str(e),mdelay)
                    time.sleep(delay)
                    mtries -= 1
                    mdelay = mdelay * backoff
                    lastException = e
            raise lastException
        return f_retry
    return deco_retry






