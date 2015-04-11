# [Django Macros Url](https://github.com/phpdude/django-macros-url/) v0.1.6 - Routing must be simple as possible

Django Macros Url makes it easy to write (and read) url patterns in your django applications by using macros.

You can combine your prefixes with macro names with underscore, for example you can use macro `:slug` and `:product_slug`. They both will be compiled to same regex pattern with their group names of course. Multiple underscores accepted too.

[![Build Status](https://travis-ci.org/phpdude/django-macros-url.svg?branch=master)](https://travis-ci.org/phpdude/django-macros-url)

### Supported macros by default

```
slug - [\w-]+
year - \d{4}
month - (0?([1-9])|10|11|12)
day - ((0|1|2)?([1-9])|[1-3]0|31)
id - \d+
pk - \d+
uuid - [a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}
```

If you want to offer more macros by default, you can fork and make pull request.

### Installation

You can install library with pypi like a charm.

```
pip install django-macros-url
```

### Usage

Django Macros Urls used same way as django standart urls. You just import this and declare your patterns with macros.

Also you can register new macro (or maybe you want to replace default macro with your like regex pattern) with `macrosurl.register(macro, pattern)` method.

Example of registration.

```python
import macrosurl

macrosurl.register('myhash', '[a-f0-9]{9}')

urlpatterns = patterns(
    'yourapp.views',
    macrosurl.url('^:myhash/$', 'myhash_main'),
    macrosurl.url('^news/:news_myhash/$', 'myhash_news'),
)
```

You free to register custom macro anywhere (i do it in main urls.py file). Macros Urls uses lazy initiazation. Macros will be compiled only on first request.

### Urls normalization

Once Macros Url finished compile regex pattern, it makes normalization of it by rules:

- Strip from left side all whitespace and ^
- Strip from right side of pattern all whitespace and $
- Add to left side ^
- Add to right side $

This makes your urls always very strong to adding any unexpected params into path.

### Examples

Macro Url example urls.py file

```python
from django.conf.urls import patterns
from macrosurl import url


urlpatterns = patterns(
    'yourapp.views',
    url('^:category_slug/$', 'category'),
    url(':category_slug/:product_slug/', 'category_product'),
    url(':category_slug/:product_slug/:variant_id', 'category_product_variant'),
    url('news/', 'news'),
    url('news/:year/:month/:day', 'news_date'),
    url('news/:slug', 'news_entry'),
    url('^order/:id$', 'order'),
)
```

Django way urls example

```python
from django.conf.urls import patterns
from macrosurl import url


urlpatterns = patterns(
    'yourapp.views',
    url('^(?P<category_slug>[\w-]+>)/$', 'category'),
    url('^(?P<category_slug>[\w-]+>)/(?P<product_slug>[\w-]+>)/$', 'category_product'),
    url('^(?P<category_slug>[\w-]+>)/(?P<product_slug>[\w-]+>)/(?P<variant_id>\d+>)$', 'category_product_variant'),
    url('^news/$', 'news'),
    url('^news/(?P<year>\d{4}>)/(?P<month>(0?([1-9])|10|11|12)>)/(?P<day>((0|1|2)?([1-9])|[1-3]0|31)>)$', 'news_date'),
    url('^news/(?P<slug>[\w-]+>)$', 'news_entry'),
    url('^order/(?P<id>\d+>)$', 'order'),
)
```

I think you understand the difference of ways :)

#### Routing must be simple! ;-)

I think real raw url regexp patterns needed in 1% case only. Prefer simple way to write (and read, this is important) fancy clean urls.

### Contributor

Alexandr Shurigin (aka [phpdude](https://github.com/phpdude/))

### Additionals

Sorry for my english level :(

You are welcome fix readme to good english by pull request! Thank you.