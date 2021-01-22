#! /usr/bin/python

import argparse
import requests
import urllib
import webbrowser


def query_wikipedia(lang, query, count):
    params = {"action": "opensearch", "search": query, "limit": count}
    url = f"https://{lang}.wikipedia.org/w/api.php"
    response = requests.get(url, params=params)
    if response.status_code != 200:
        msg = f"wikipedia: {lang}\nQuery: {query}\nCount: {count}\nStatus code: {response.status_code}"
        raise RuntimeError(msg)
    content = response.json()
    return content[3]


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Search, in order, if given String is availble on Italian Wikipedia, English Wikipedia or Google (as last resort)"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="Specify the maximum number of wikipedia urls to open, 1 by default",
        default=1,
    )
    parser.add_argument(
        "query",
        help="String to search on Italian wikipedia , English wikipedia or google (as last resort)",
    )
    return parser.parse_args()


def open_all_pages(urls):
    for url in urls:
        webbrowser.open(url)


def main():
    args = parse_cli_args()
    languages = ["it", "en"]
    for lang in languages:
        urls = query_wikipedia(lang, args.query, args.count)
        if urls:
            open_all_pages(urls)
            break
    else:
        quote_query = urllib.parse.quote(args.query)
        google = f"https://www.google.com/search?q={quote_query}"
        webbrowser.open(google)


if __name__ == "__main__":
    main()
