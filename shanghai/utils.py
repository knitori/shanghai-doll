
import regex


# more or less the regex used in HexChat IRC client
patterns = dict(
    scheme=r'(?:https?://)',
    user=r'(?:[\w\-]+@)',
    domain=r'[\pL\pN\pS][-\pL\pN\pS]*(?:\.[-\pL\pN\pS]+)*',
    tld=r'\.[\pL][-\pL\pN]*[\pL]',
    port=r'(?:\:\d+)',
    lpar=r'\(',
    rpar=r'\)',
    noparens=r'[^\(\) \t\n\r]*',
    endpath=r'(?<![\.,\?!\]])',
)

patterns['path'] = r'(?:(?:{lpar}{noparens}{rpar})|(?:{noparens}))*'\
    .format(**patterns)

URL_PATTERN = r'(?P<url>{scheme}?{user}?(?:{domain}{tld}){port}?' \
              r'(?:/{path}{endpath})?)' \
              .format(**patterns)

url_pattern = regex.compile(URL_PATTERN, regex.IGNORECASE)


def find_urls(text):
    return url_pattern.findall(text)
