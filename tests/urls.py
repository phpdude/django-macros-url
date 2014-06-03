import uuid

from django.conf import settings
from django.conf.urls import include
from django.utils import unittest

from macrosurl import MacroUrlPattern, url


class TestRegexCompilation(unittest.TestCase):
    def test_nomacro(self):
        self.assertEqual(MacroUrlPattern('^$').compiled, '^$')
        self.assertEqual(MacroUrlPattern('^news/all/$').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/all/$').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/all/$').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/:news/$').compiled, '^news/:news/$')

    def test_normalize_url(self):
        self.assertEqual(MacroUrlPattern('').compiled, '^$')
        self.assertEqual(MacroUrlPattern('news/all/').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/all/$').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/all/').compiled, '^news/all/$')

    def test_strip_whitespace(self):
        self.assertEqual(MacroUrlPattern('').compiled, '^$')
        self.assertEqual(MacroUrlPattern(' news/all/').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern('^news/all/$ ').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern(' ^news/all/ ').compiled, '^news/all/$')
        self.assertEqual(MacroUrlPattern(' ^news/all/ \n').compiled, '^news/all/$')

    def test_id(self):
        self.assertEqual(MacroUrlPattern('page/:id').compiled, '^page/(?P<id>\d+)$')
        self.assertEqual(MacroUrlPattern('product/:product_id').compiled, '^product/(?P<product_id>\d+)$')
        self.assertEqual(MacroUrlPattern('product/:id/:product_id').compiled,
                         '^product/(?P<id>\d+)/(?P<product_id>\d+)$')
        self.assertEqual(MacroUrlPattern('product/:id/:product_id/:news_id').compiled,
                         '^product/(?P<id>\d+)/(?P<product_id>\d+)/(?P<news_id>\d+)$')

    def test_slug(self):
        self.assertEqual(MacroUrlPattern('page/:slug').compiled, '^page/(?P<slug>[\w-]+)$')
        self.assertEqual(MacroUrlPattern('page/:category_slug/:slug').compiled,
                         '^page/(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)$')

    def test_year(self):
        self.assertEqual(MacroUrlPattern('news/:year').compiled, '^news/(?P<year>\d{4})$')

    def test_year_month(self):
        self.assertEqual(MacroUrlPattern('news/:year/:month').compiled,
                         '^news/(?P<year>\d{4})/(?P<month>(0?([1-9])|10|11|12))$')

    def test_year_month_day(self):
        self.assertEqual(MacroUrlPattern('news/:year/:month/:day/').compiled,
                         '^news/(?P<year>\d{4})/(?P<month>(0?([1-9])|10|11|12))/(?P<day>((0|1|2)?([1-9])|[1-3]0|31))/$')

    def test_date(self):
        self.assertEqual(MacroUrlPattern('news/:date/').compiled,
                         '^news/(?P<date>\d{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31))/$')

    def test_uid(self):
        self.assertEqual(MacroUrlPattern('invoice/:uuid').compiled,
                         '^invoice/(?P<uuid>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})$')

    def test_strongurl(self):
        self.assertEqual(MacroUrlPattern('orders/:date/:uuid/products/:slug/:variant_id').compiled,
                         '^orders/(?P<date>\\d{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31))/(?P<uuid>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/products/(?P<slug>[\\w-]+)/(?P<variant_id>\\d+)$')

    # noinspection PyProtectedMember
    def test_includes_end(self):
        self.assertEqual(str(url('users/:slug', include('tests'))._regex), '^users/(?P<slug>[\\w-]+)')
        self.assertEqual(str(url('users/:slug', include('tests', namespace='1'))._regex), '^users/(?P<slug>[\\w-]+)')
        self.assertEqual(str(url('users/:slug', 'tests')._regex), '^users/(?P<slug>[\\w-]+)$')


class TestRegexUrlResolving(unittest.TestCase):
    def setUp(self):
        if not settings.configured:
            settings.configure(USE_I18N=False)

    def test_id(self):
        self.assertIsNone(url('product/:id', 'view').resolve('product/test'))
        self.assertIsNotNone(url('product/:id', 'view').resolve('product/10'))
        self.assertEqual(url('product/:id', 'view').resolve('product/10').kwargs['id'], '10')
        self.assertEqual(url('product/:product_id', 'view').resolve('product/10').kwargs['product_id'], '10')

    def test_slug(self):
        self.assertIsNone(url('product/:slug', 'view').resolve('product/test/ouch'))
        self.assertIsNotNone(url('product/:slug', 'view').resolve('product/test'))
        self.assertIsNotNone(url('product/:slug/:other_slug', 'view').resolve('product/test/other'))

    def test_year(self):
        self.assertIsNone(url('news/:year', 'view').resolve('news/last'))
        for y in range(1970, 2025):
            self.assertIsNotNone(url('news/:year', 'view').resolve('news/%s' % y))
        self.assertIsNone(url('news/:year/last', 'view').resolve('news/2014/other'))
        self.assertIsNotNone(url('news/:year/last', 'view').resolve('news/2014/last'))

    def test_year_month(self):
        self.assertIsNone(url('news/:year/:month', 'view').resolve('news/2014/last'))
        self.assertIsNone(url('news/:year/:month', 'view').resolve('news/2014/2012'))
        for y in range(1970, 2025):
            for m in range(1, 12):
                self.assertIsNotNone(url('news/:year/:month', 'view').resolve('news/%s/%s' % (y, m)))

        self.assertIsNotNone(url('news/:year/:month/last', 'view').resolve('news/2014/12/last'))

    def test_year_month_day(self):
        self.assertIsNone(url('news/:year/:month/:day', 'view').resolve('news/2014/12/last'))
        self.assertIsNone(url('news/:year/:month/:day', 'view').resolve('news/2014/2012/31'))
        for y in range(2000, 2020):
            for m in range(1, 12):
                for d in range(1, 31):
                    self.assertIsNotNone(url('news/:year/:month/:day', 'view').resolve('news/%s/%s/%s' % (y, m, d)))

    def test_date(self):
        self.assertIsNone(url('news/:date', 'view').resolve('news/2014/12/12'))
        for y in range(2000, 2020):
            for m in range(1, 12):
                for d in range(1, 31):
                    self.assertIsNotNone(url('news/:date', 'view').resolve('news/%s-%s-%s' % (y, m, d)))

    def test_uuid(self):
        self.assertIsNone(url("invoice/:uuid", 'view').resolve('invoice/123123-123123-1231231-1231312-3-1312312-'))
        for i in range(1, 1000):
            self.assertIsNotNone(url("invoice/:uuid", 'view').resolve('invoice/%s' % uuid.uuid4()))
