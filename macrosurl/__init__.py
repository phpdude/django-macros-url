import re

VERSION = (0, 2, 2)

_macros_library = {
    'id': r'\d+',
    'pk': r'\d+',
    'page': r'\d+',
    'slug': r'[\w-]+',
    'year': r'\d{4}',
    'month': r'(0?([1-9])|10|11|12)',
    'day': r'((0|1|2)?([1-9])|[1-3]0|31)',
    'date': r'\d{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31)',
    'uuid': r'[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}',
}


def get_version(*args, **kwargs):
    return ".".join(map(str, VERSION))


def register(macros, pattern):
    _macros_library[macros] = pattern


def regex_group(macro, pattern):
    return '(?P<%s>%s)' % (macro, pattern)


def normalize_pattern(url, end_dollar=True):
    pattern = '^%s$'
    if not end_dollar:
        pattern = '^%s'

    return pattern % url.lstrip("^ \n").rstrip("$ \n")


class MacroUrlPattern(object):
    def __init__(self, pattern, end_dollar=True):
        self.pattern = pattern
        self.end_dollar = end_dollar

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

        return normalize_pattern(pattern, self.end_dollar)

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
    from django.conf.urls import url as baseurl

    # Handle include()'s in views.
    end_dollar = True
    if isinstance(view, tuple) and len(view) == 3:
        end_dollar = False

    # Auto-calling as_view on CBVs objects. Now you can omit as_view() in your views by default.
    if isinstance(view, type):
        if hasattr(view, 'as_view') and hasattr(view.as_view, '__call__'):
            view = view.as_view()

    return baseurl(MacroUrlPattern(regex, end_dollar=end_dollar), view, kwargs=kwargs, name=name, prefix=prefix)
