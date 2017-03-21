import requests

main_url = 'http://jobboerse.arbeitsagentur.de'


def get_page(url, jsession=None):
    headers = {'user-agent': 'offers_monitor/0.0.1'}
    cookies = {}

    if jsession is not None:
        cookies = {'jsessionid': jsession}

    if url is None:
        url = main_url

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == requests.codes.ok:
        #if jsession is None:
        #    jsession = get_jsession(response)

        return {'success': True, 'jsession': jsession, 'page': response.text}

    return {'success': False, 'jsession': jsession, 'page': response.text}


def get_jsession(response):
    if 'jsessionid' in response.cookies.get_dict():
        return response.cookies.get_dict()['jsessionid']

    for rr in response.history:
        print(rr)
        print(rr.cookies.get_dict())
        if 'jsessionid' in rr.cookies.get_dict():
            return rr.cookies.get_dict()['jsessionid']

    return None

