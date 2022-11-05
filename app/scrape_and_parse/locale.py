from os import getenv

# To help get consistent results from scraping, a locale can be specified in .env
# This defaults to en-gb if none is provided
def facebook_www_to_locale(url):
    locale = getenv("fb_locale", "en-gb")
    return url.replace("www.facebook", "{}.facebook".format(locale))

# And this function does the opposite, by removing the locale specification
# So that Facebook will detemine the language from the the end users' preference
def facebook_locale_to_www(url):
    locale = getenv("fb_locale", "en-gb")
    return url.replace("{}.facebook".format(locale), "www.facebook")
