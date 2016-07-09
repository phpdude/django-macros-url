# [Django Macros URL](https://github.com/phpdude/django-macros-url/) v0.2.0 - Routing must be simple as possible

Django Macros URL makes it easy to write (and read) URL patterns in your Django applications by using macros.

You can combine your prefixes with macro names with an underscore, for example, you can use a macro `:slug` 
and `:product_slug`. They both will be compiled to same regex pattern with their group names of course. 
Multiple underscores accepted too.

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

If you want to offer more macros by default, you can fork and make a pull request.

### Installation

You can install the library with PyPI.

```
pip install django-macros-url
```

### Usage

Django Macros URLs used the same way as Django standard URLs. You just import this and declare your 
patterns with macros.

Also, you can register new macro (or maybe you want to replace default macro with your like regex
pattern) with `macrosurl.register(macro, pattern)` method.

An example of registration.

```python
import macrosurl

macrosurl.register('myhash', '[a-f0-9]{9}')

urlpatterns = patterns(
    'yourapp.views',
    macrosurl.url('^:myhash/$', 'myhash_main'),
    macrosurl.url('^news/:news_myhash/$', 'myhash_news'),
)
```

Feel free to register custom macro anywhere (i do it in main urls.py file). Macros URLs uses lazy 
initialization. Macros will be compiled only on the first request.

### URL normalization

Once Macros URL completed compile regex pattern, it makes normalization of it by rules:

- Strip from left side all whitespace and ^
- Strip from right side of pattern all whitespace and $
- Add to left side ^
- Add to right side $

This makes your URLs always very strong to adding any unexpected params into a path.

### Auto-calling as_view() on CBV objects.

Library check type of view and if a view is type object with defined 'as_view' function, call this. This allows 
you omit ".as_view()" calls in your urls.py files. But you can call this manual with params if you need.

This feature helps you to keep your urls.py files clean as possible. I hope you like this feature!

### Examples

Macros URL example urls.py file

```python
from django.conf.urls import patterns
from macrosurl import url
from project.portal.views import IndexView

urlpatterns = patterns(
    'yourapp.views',
    url('^:category_slug/$', 'category'),
    url(':category_slug/:product_slug/', 'category_product'),
    url(':category_slug/:product_slug/:variant_id', 'category_product_variant'),
    url('news/', 'news'),
    url('news/:year/:month/:day', 'news_date'),
    url('news/:slug', 'news_entry'),
    url('^order/:id$', 'order'),
    url('^$', IndexView),
)
```

Standard Django urls example

```python
from django.conf.urls import patterns
from macrosurl import url
from project.portal.views import IndexView


urlpatterns = patterns(
    'yourapp.views',
    url('^(?P<category_slug>[\w-]+>)/$', 'category'),
    url('^(?P<category_slug>[\w-]+>)/(?P<product_slug>[\w-]+>)/$', 'category_product'),
    url('^(?P<category_slug>[\w-]+>)/(?P<product_slug>[\w-]+>)/(?P<variant_id>\d+>)$', 'category_product_variant'),
    url('^news/$', 'news'),
    url('^news/(?P<year>\d{4}>)/(?P<month>(0?([1-9])|10|11|12)>)/(?P<day>((0|1|2)?([1-9])|[1-3]0|31)>)$', 'news_date'),
    url('^news/(?P<slug>[\w-]+>)$', 'news_entry'),
    url('^order/(?P<id>\d+>)$', 'order'),
    url('^$', IndexView.as_view()),
)
```

I think you understand the difference of ways :)

#### Routing must be simple! ;-)

I think raw URL regexp patterns needed in 1% case only. I prefer simple way to write (and read, this is 
important) fancy clean URLs.

### Contributor

[Alexandr Shurigin](https://github.com/phpdude/)

You are welcome to contribute by PR.