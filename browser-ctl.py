#! /usr/bin/python

# Copyright (c) 2020 Filippo Ranza <filipporanza@gmail.com>

from argparse import ArgumentParser
import webbrowser
from subprocess import run
import re
import socket
import os
import urllib.parse

import pyperclip


def browser_name():
    handler = webbrowser.get()
    return handler.name


def open_browser(url):
    webbrowser.open_new_tab(url)
    browser = browser_name()
    if os.name == 'posix':
        run(["wmctrl", "-a", browser])


def build_query(query, site):
    tokens = query.split()
    if site:
        tokens.insert(0, site)

    return "+".join(map(urllib.parse.quote, tokens))


def is_website(line):
    url_regex = re.compile(r"http(s)?://(?P<site>[\w\.-]+)")
    if m := url_regex.match(line):
        site = m.groupdict()["site"]
        try:
            socket.gethostbyname(site)
        except socket.gaierror:
            out = False
        else:
            out = True
    else:
        out = False
    return out


def auto_query(msg="", site=""):
    if not msg:
        msg = pyperclip.paste()

    if is_website(msg):
        url = msg
    else:
        query = build_query(msg, site)
        url = f"https://www.google.com/search?client={browser_name()}&q={query}"

    open_browser(url)


def translate(text, source, target):
    if not text:
        text = pyperclip.paste()

    query = build_query(text, None)
    url = f"https://translate.google.it/?sl={source}&tl={target}&text={query}"
    open_browser(url)


def search_wikipedia(query, language):
    if not query:
        query = pyperclip.paste()

    query = build_query(query, None)
    url = f"https://{language}.wikipedia.org/w/index.php?search={query}"
    open_browser(url)


def parse_args():
    parser = ArgumentParser()
    subcommand = parser.add_subparsers(title="command", dest="command", required=True)

    query_cmd = subcommand.add_parser("query", help="search given text on google")
    query_cmd.add_argument(
        "-s",
        "--site",
        help="specify a site to add at the beginning of the query string",
    )
    query_cmd.add_argument(
        "-q",
        "--query",
        help="specify the query string to seach, if omitted read from clipboard",
    )

    translate_cmd = subcommand.add_parser("translate", help="translate given text")
    translate_cmd.add_argument(
        "-s",
        "--source",
        default="en",
        help=f"specify source language, defaults to 'en'",
    )
    translate_cmd.add_argument(
        "-t",
        "--target",
        default="it",
        help=f"specify target language, defaults to 'it'",
    )
    translate_cmd.add_argument(
        "-T",
        "--text",
        help="text to translate from source to target language, if omitted read from clipboard",
    )

    subcommand.add_parser("whatsapp", help="open a Whatsapp web page")
    subcommand.add_parser("open", help="open a Google web page")
    subcommand.add_parser("mail", help="open a Gmail web page")
    subcommand.add_parser("cal", help="open a Google Calendar web page")

    wiki_cmd = subcommand.add_parser("wiki", help="search given text (or cliboard) on wikipedia")
    wiki_cmd.add_argument('-l', '--lang', help="specify wikipedia language", default="en")
    wiki_cmd.add_argument('-q', '--query', help="text to search on wikipedia, if omitted read from clipboard")

    return parser.parse_args()


def main():
    args = parse_args()
    handlers = {
        "translate": lambda args: translate(
            text=args.text, source=args.source, target=args.target
        ),
        "query": lambda args: auto_query(msg=args.query, site=args.site),
        "whatsapp": lambda _: open_browser("http://web.whatsapp.com"),
        "open": lambda _: open_browser("https://www.google.com"),
        "mail": lambda _: open_browser("https://mail.google.com/"),
        "cal": lambda _: open_browser("https://calendar.google.com/"),
        "wiki" : lambda args : search_wikipedia(args.query, args.lang)
    }

    handler = handlers[args.command]
    handler(args)


if __name__ == "__main__":
    main()
