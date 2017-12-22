from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
import requests

app_redirects = [
    (
        "Redirect HTTP to HTTPS",
        'http://uk.wegotpop.com/login',
        'https://uk.wegotpop.com/login',
        200,
        [
            (301, 'http://uk.wegotpop.com/apply'),
        ],
        {},
        []
    ),
    (
        "Redirect naked to login",
        'https://uk.wegotpop.com',
        'https://uk.wegotpop.com/login',
        200,
        [
            (301, 'https://uk.wegotpop.com/'),
        ],
        {},
        []
    ),
    (
        "Login works",
        'https://uk.wegotpop.com/login',
        'https://uk.wegotpop.com/login',
        200,
        [],
        {},
        []
    ),
    (
        "Redirect naked to apply for US launch",
        'https://us.wegotpop.com',
        'https://us.wegotpop.com/apply',
        200,
        [
            (302, 'https://us.wegotpop.com/')
        ],
        {},
        []
    )
]

content_redirects = [
    (
        "PRODUCTION Landing page",
        'https://www.wegotpop.com/',
        'https://www.wegotpop.com/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION Backward compatibility with POP application served at www",
        'https://www.wegotpop.com/login',
        'https://uk.wegotpop.com/login',
        200,
        [
            (301, 'https://www.wegotpop.com/login')
        ],
        {},
        []
    ),
    (
        "PRODUCTION US main page is served by the static site",
        'https://www.wegotpop.com/pages/us/',
        'https://www.wegotpop.com/pages/us/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION FAQ pages are served by the static site",
        'https://www.wegotpop.com/faq/',
        'https://www.wegotpop.com/faq/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION US casting director page is served by the static site",
        'https://www.wegotpop.com/pages/us/casting-director/',
        'https://www.wegotpop.com/pages/us/casting-director/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION US background artist page is served by the static site",
        'https://www.wegotpop.com/pages/us/background-artist/',
        'https://www.wegotpop.com/pages/us/background-artist/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION US team page is served by the static site",
        'https://www.wegotpop.com/pages/us/the-pop-team/',
        'https://www.wegotpop.com/pages/us/the-pop-team/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION US blog page is served by the UK WordPress site",
        'https://www.wegotpop.com/pages/us/blog/',
        'https://www.wegotpop.com/pages/uk/blog/',
        200,
        [
            (302, 'https://www.wegotpop.com/pages/us/blog/')
        ],
        {},
        []
    ),
    (
        "PRODUCTION US category pages are served by the UK WordPress site",
        'https://www.wegotpop.com/pages/us/category/casting/',
        'https://www.wegotpop.com/pages/uk/category/casting/',
        200,
        [
            (302, 'https://www.wegotpop.com/pages/us/category/casting/')
        ],
        {},
        []
    ),
    (
        "PRODUCTION US blog articles are served by the UK WordPress site",
        'https://www.wegotpop.com/pages/us/2017/06/02/top-10-cities-live-work-film/',
        'https://www.wegotpop.com/pages/uk/2017/06/02/top-10-cities-live-work-film/',
        200,
        [
            (302, 'https://www.wegotpop.com/pages/us/2017/06/02/top-10-cities-live-work-film/')
        ],
        {},
        []
    ),
    (
        "PRODUCTION global privacy is served by the static site",
        'https://www.wegotpop.com/pages/privacy/',
        'https://www.wegotpop.com/pages/privacy/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION global Terms of Service page is served by the static site",
        'https://www.wegotpop.com/pages/terms-of-service/',
        'https://www.wegotpop.com/pages/terms-of-service/',
        200,
        [],
        {},
        []
    ),
    (
        "PRODUCTION CSS",
        'https://www.wegotpop.com/css/main.css',
        'https://www.wegotpop.com/css/main.css',
        200,
        [],
        {'Content-Type': 'text/css'},
        []
    ),
    (
        "PRODUCTION Handle final slash",
        'https://www.wegotpop.com/pages/uk/casting-agents',
        'https://www.wegotpop.com/pages/uk/casting-agents/',
        200,
        [(302, 'https://www.wegotpop.com/pages/uk/casting-agents')],
        {},
        []
    ),
    (
        "PRODUCTION Static JS",
        'https://www.wegotpop.com/js/modals.js',
        'https://www.wegotpop.com/js/modals.js',
        200,
        [],
        {'Content-Type': 'application/javascript; charset=utf-8'},
        []
    )
]

content_staging_redirects = [
    (
        "STAGING Landing page",
        'https://www-staging.wegotpop.com/',
        'https://www-staging.wegotpop.com/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING global privacy is served by the static site",
        'https://www-staging.wegotpop.com/pages/privacy/',
        'https://www-staging.wegotpop.com/pages/privacy/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING global Terms of Service page is served by the static site",
        'https://www-staging.wegotpop.com/pages/terms-of-service/',
        'https://www-staging.wegotpop.com/pages/terms-of-service/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING US main page is served by the static site",
        'https://www-staging.wegotpop.com/pages/us/',
        'https://www-staging.wegotpop.com/pages/us/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING UK main page is served by the static site",
        'https://www-staging.wegotpop.com/pages/uk/',
        'https://www-staging.wegotpop.com/pages/uk/',
        200,
        [],
        {},
        []
    ),    (
        "STAGING FAQ pages are served by the static site",
        'https://www-staging.wegotpop.com/faq/',
        'https://www-staging.wegotpop.com/faq/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING US casting director page is served by the static site",
        'https://www-staging.wegotpop.com/pages/us/casting-director/',
        'https://www-staging.wegotpop.com/pages/us/casting-director/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING US background artist page is served by the static site",
        'https://www-staging.wegotpop.com/pages/us/background-artist/',
        'https://www-staging.wegotpop.com/pages/us/background-artist/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING US team page is served by the static site",
        'https://www-staging.wegotpop.com/pages/us/the-pop-team/',
        'https://www-staging.wegotpop.com/pages/us/the-pop-team/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING UK crew portal application page is served by the static site",
        'https://www-staging.wegotpop.com/pages/uk/crew-portal/application/',
        'https://www-staging.wegotpop.com/pages/uk/crew-portal/application/',
        200,
        [],
        {},
        []
    ),
    (
        "STAGING US blog page is served by the static site",
        'https://www-staging.wegotpop.com/pages/us/blog/',
        'https://www-staging.wegotpop.com/pages/uk/blog/',
        200,
        [
            (302, 'https://www-staging.wegotpop.com/pages/us/blog/')
        ],
        {},
        []
    ),
    (
        "STAGING US category pages are served by the static site",
        'https://www-staging.wegotpop.com/pages/us/category/casting/',
        'https://www-staging.wegotpop.com/pages/uk/category/casting/',
        200,
        [
            (302, 'https://www-staging.wegotpop.com/pages/us/category/casting/')
        ],
        {},
        []
    ),
    (
        "STAGING US blog articles are served by the static site",
        'https://www-staging.wegotpop.com/pages/us/2017/06/02/top-10-cities-live-work-film/',
        'https://www-staging.wegotpop.com/pages/uk/2017/06/02/top-10-cities-live-work-film/',
        200,
        [
            (302, 'https://www-staging.wegotpop.com/pages/us/2017/06/02/top-10-cities-live-work-film/')
        ],
        {},
        []
    ),
    (
        "STAGING CSS",
        'https://www-staging.wegotpop.com/css/main.css',
        'https://www-staging.wegotpop.com/css/main.css',
        200,
        [],
        {'Content-Type': 'text/css'},
        []
    ),
    (
        "STAGING Handle final slash",
        'https://www-staging.wegotpop.com/pages/uk/casting-agents',
        'https://www-staging.wegotpop.com/pages/uk/casting-agents/',
        200,
        [(302, 'https://www-staging.wegotpop.com/pages/uk/casting-agents')],
        {},
        []
    ),
    (
        "STAGING Static JS",
        'https://www-staging.wegotpop.com/js/modals.js',
        'https://www-staging.wegotpop.com/js/modals.js',
        200,
        [],
        {'Content-Type': 'application/javascript; charset=utf-8'},
        []
    )
]

definitions = app_redirects + content_redirects + content_staging_redirects

ids = [i[0] for i in definitions]
redirects = [i[1:] for i in definitions]


@pytest.mark.parametrize(
    "src_url, dst_url, code, history, headers, strings",
    redirects,
    ids=ids
)
def test_urls(src_url, dst_url, code, history, headers, strings):
    response = requests.get(src_url)

    assert response.url == dst_url
    assert response.status_code == code
    assert [(r.status_code, r.url) for r in response.history] == history
    for x in headers.items():
        assert x in response.headers.items()
    for s in strings:
        assert s.encode('utf-8') in response.content
