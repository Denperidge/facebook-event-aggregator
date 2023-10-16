from src.facebook_event_aggregator.utils.url_converter import facebook_locale_to_www, facebook_www_to_locale

class TestUrlConverter():
    www_url = "https://www.facebook.com/test"
    locale_url = "https://en-gb.facebook.com/test"


    def test_www_to_locale(self):
        assert facebook_www_to_locale(self.www_url, "en-gb") == self.locale_url

    def test_locale_to_www(self):
        assert facebook_locale_to_www(self.locale_url, "en-gb") == self.www_url
    