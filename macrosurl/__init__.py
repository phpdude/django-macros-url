import re

from django.conf.urls import url as baseurl

VERSION = (0, 1, 0)

_macros_library = {
    'id': r'\d+',
    'slug': r'[\w-]+',
    'year': r'\d{4}',
    'month': r'(0?([1-9])|10|11|12)',
    'day': r'((0|1|2)?([1-9])|[1-3]0|31)',
    'date': r'\d{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31)',
    'uuid': r'[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}'
}


def get_version(*args, **kwargs):
    return ".".join(map(str, VERSION))


def register(macros, pattern):
    _macros_library[macros] = pattern


def regex_group(macro, pattern):
    return '(?P<%s>%s)' % (macro, pattern)


def normalize_pattern(url):
    return '^%s$' % url.lstrip("^ \n").rstrip("$ \n")


class MacroUrlPattern(object):
    def __init__(self, pattern):
        self.pattern = pattern


    def compile(self):
        pattern = self.pattern
        macros = re.findall('(:([a-z_\d]+))', pattern)
        for match, macro in macros:
            if macro in _macros_library:
                pattern = pattern.replace(match, regex_group(macro, _macros_library[macro]))
            else:
                for _macro in _macros_library:
                    if macro.endswith("_%s" % _macro):
                        pattern = pattern.replace(match, regex_group(macro, _macros_library[_macro]))
                        continue

        return normalize_pattern(pattern)

    @property
    def compiled(self):
        if not hasattr(self, '_compiled'):
            setattr(self, '_compiled', self.compile())

        return getattr(self, '_compiled')

    def __str__(self):
        return self.compiled

    def __unicode__(self):
        return self.__str__()


def url(regex, view, kwargs=None, name=None, prefix=''):
    return baseurl(MacroUrlPattern(regex), view, kwargs=kwargs, name=name, prefix=prefix)