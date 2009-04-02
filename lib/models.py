import re, datetime
import os.path as op


DATE_RE = re.compile(r'(.*?)(\d+)[/-](\d+)[/-](\d+)[/-](.*)$')

class Post(object):
    @staticmethod
    def check(entry):
        if DATE_RE.search(entry.path):
            return True
        return False

    def __init__(self):
        base, Y, M, D, slug = DATE_RE.search(self.path).groups()
        self.settings.date = datetime.date(int(Y), int(M), int(D))
        self.settings.base = base
        self.settings.slug = slug.rsplit('.', 1)[0] # drop extension

    def __str__(self):
        return self.slug

    def get_url(self):
        date = self.date.strftime('%Y/%m/%d')
        url = op.join(self.base, date, self.slug)
        return url


class Page(object):
    @staticmethod
    def check(entry):
        return True

    def __init__(self):
        base, slug = op.split(self.path)
        self.settings.base = base
        self.settings.slug = slug.rsplit('.', 1)[0] # drop extension

    def __str__(self):
        return self.slug

    def get_url(self):
        url = op.join(self.base, self.slug)
        return url


TYPE_LIST = [Post, Page]
