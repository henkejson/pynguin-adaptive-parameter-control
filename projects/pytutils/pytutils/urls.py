try:
    import urlparse
    from urllib import urlencode
except ImportError:  # py3k
    import urllib.parse as urlparse
    urlencode = urlparse.urlencode


def update_query_params(url, params, doseq=True):
    """
    Update and/or insert query parameters in a URL.

    >>> update_query_params('http://example.com?foo=bar&biz=baz', dict(foo='stuff'))
    'http://example.com?...foo=stuff...'

    :param url: URL
    :type url: str
    :param kwargs: Query parameters
    :type kwargs: dict
    :return: Modified URL
    :rtype: str
    """
    scheme, netloc, path, query_string, fragment = urlparse.urlsplit(url)

    query_params = urlparse.parse_qs(query_string)
    query_params.update(**params)

    new_query_string = urlencode(query_params, doseq=doseq)

    new_url = urlparse.urlunsplit([scheme, netloc, path, new_query_string, fragment])
    return new_url
