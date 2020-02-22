# !/usr/bin/python
# -*- coding: utf-8 -*-
"""myds - A Data Science Package (https://github.com/augustomatheuss/myds)

Module urls from myds for URL extraction.

Copyright 2020 Augusto Damasceno

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Augusto Damasceno (augustodamasceno@protonmail.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2020 Augusto Damasceno"
__license__ = "2-Clause BSD License"


import requests
from bs4 import BeautifulSoup
import validators


def url2bs(url: str):
    """
    HTTP GET response text with the url to a BeautifulSoup object parsed with lxml.
    :param url: URL.
    :return: BeautifulSoup object.
    """
    try:
        response = requests.get(url)
        result = BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException as e:
        print('Error in HTTP GET from the url:\n\t' + url + '\nERROR MESSAGE:')
        print(e)
        result = None

    return result


def all_urls(soup: BeautifulSoup):
    """
    Get a list with all URLs in a BeautifulSoup object.
    :param soup: BeautifulSoup object.
    :return: List with all URLs.
    """
    all_urls_result_set = soup.findAll('a')
    all_urls_list = []
    for result_set in all_urls_result_set:
        url = result_set.get('href')
        if url is not None:
            all_urls_list.append(url)

    return all_urls_list


def local_urls(soup: BeautifulSoup):
    """
    Get a list with all local URLs in a BeautifulSoup object.
    :param soup: BeautifulSoup object.
    :return: List with all local URLs.
    """
    url_result_set = soup.findAll('a')
    local = []
    for result_set in url_result_set:
        url = result_set.get('href')
        if url is not None and url.startswith('/'):
            local.append(url)

    return local


def not_local_urls(soup: BeautifulSoup):
    """
    Get a list with all not local URLs in a BeautifulSoup object.
    :param soup: BeautifulSoup object.
    :return: List with all not local URLs.
    """
    url_result_set = soup.findAll('a')
    local = []
    for result_set in url_result_set:
        url = result_set.get('href')
        if url is not None and (not url.startswith('/') or url.startswith('.')):
            local.append(url)

    return local


def next_level(urls_list, base_url):
    """
    For all URLs in a list:
        * HTTP GET response text with the url to a BeautifulSoup object parsed with lxml.
        * Get a list with all URLs in the BeautifulSoup object.
    :param urls_list: List of URLs
    :param base_url: Base URL where the URLs came from.
    :return: List of dictionaries. Each dictionary is {URL: list-of-related-URLs}.
    """
    levels = []
    for url in urls_list:
        if url.startswith('/') or url.startswith('.'):
            slashs = base_url.count('/')
            split = base_url.rsplit('/', slashs-2)
            internal = url2bs(split[0] + url)
            if internal is not None:
                levels.append({split[0] + url: all_urls(internal)})
        else:
            external = url2bs(url)
            if external is not None:
                levels.append({url: all_urls(external)})

    return levels


if __name__ == "__main__":
    """ If the module is called as script, receive one or more URLs as args and prints the results for:
        * all_urls
        * local_urls
        * new_level
    """
    import sys

    for arg in range(1, len(sys.argv)):
        if validators.url(sys.argv[arg]):
            soup = url2bs(sys.argv[arg])
            if soup is not None:
                print('\nAll urls in {}'.format(sys.argv[arg]))
                a = 1
                all_urls_list = all_urls(soup)
                for u in all_urls_list:
                    print(str(a)+": " + u)
                    a += 1
                print('\nAll local urls in {}'.format(sys.argv[arg]))
                local = 1
                for u in local_urls(soup):
                    print(str(local) + ": " + u)
                    local += 1
                for u in next_level(all_urls_list, sys.argv[arg]):
                    key, value = list(u.items())[0]
                    print('\nNext level urls for ' + sys.argv[arg] + '\n\t from url ' + key)
                    n = 1
                    for un in value:
                        print(str(n)+": "+un)
                        n += 1
