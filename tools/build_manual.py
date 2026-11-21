#!/usr/bin/env python3
#######################################################################
#   RRRRRR    OOOOOO   SSSSSS  EEEEEEEE TTTTTTTT TTTTTTTT    AA       #
#   RR   RR  OO    OO SS       EE          TT       TT      AAAA      #
#   RR   RR  OO    OO SS       EE          TT       TT     AA  AA     #
#   RRRRRR   OO    OO  SSSSSS  EEEEEE      TT       TT    AA    AA    #
#   RR   RR  OO    OO       SS EE          TT       TT    AAAAAAAA    #
#   RR   RR  OO    OO       SS EE          TT       TT    AA    AA    #
#   RR    RR  OOOOOO   SSSSSS  EEEEEEEE    TT       TT    AA    AA    #
#                                                                     #
#                         Rosetta                                     #
#######################################################################
#
# File:
#   tools/build_manual.py (RosettaSupportManual repo)
#
# Purpose:
#   Refreshes the parts of the Support Manual (Rosetta_Support_Manual/)
#   that are made from the pages themselves. Run it after editing,
#   adding or renaming a page:
#
#       python3 tools/build_manual.py
#
#   It writes:
#     - search-index.js: every page's title, headings and text, for the
#       search box in the header (rosetta-docs.js). A script file, not
#       JSON, so it also works when a page is opened from disk.
#     - each page's Previous / Next links (between <!--pager--> and
#       <!--/pager-->), in the order of the contents page (index.html).
#       Pages the contents page doesn't link get none.
#   Running it twice changes nothing the second time. Standard library
#   only. The same as the Rosetta repo's docs/build_manuals.py (User
#   Manual and Gcode Library), without their software-version line.
#
# Version
#   1.0 - 21 November 2026
#
# Copyright (c) 2026 Colvin Tools and Brainwave Embedded.
#
# The MIT/X Consortium License applies.
#######################################################################

import html
import json
import os
import re
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER, NAME = "Rosetta_Support_Manual", "Support Manual"


class Page(HTMLParser):
    '''Title, headings (id, text) and plain text of a page's
    <div class="content"> (plus its <h1>), and its links in order.'''

    SKIP = {"script", "style", "nav", "math"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.heads, self.text, self.links = "", [], [], []
        self._in_h1 = 0
        self._content = False
        self._depth = 0
        self._skip = 0
        self._head = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and "content" in (a.get("class") or "").split():
            self._content, self._depth = True, 0
        if self._content and tag == "div":
            self._depth += 1
        if tag in self.SKIP:
            self._skip += 1
        if tag == "h1" and not self._content and not self.title:
            self._in_h1 = 1
        if self._content and tag in ("h1", "h2", "h3") and a.get("id"):
            self._head = [a["id"], ""]
        if self._content and tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        if tag == "h1" and self._in_h1:
            self._in_h1 = 0
        if self._head and tag in ("h1", "h2", "h3"):
            self.heads.append((self._head[0], " ".join(self._head[1].split())))
            self._head = None
        if self._content and tag == "div":
            self._depth -= 1
            if self._depth == 0:
                self._content = False

    def handle_data(self, data):
        if self._in_h1:
            self.title += data
        if self._content and not self._skip:
            self.text.append(data)
            if self._head:
                self._head[1] += data


def parse(path):
    p = Page()
    p.feed(open(path, encoding="utf-8").read())
    p.title = " ".join(p.title.split())
    return p


def main():
    base = os.path.join(REPO, FOLDER)
    pages = {f: parse(os.path.join(base, f)) for f in sorted(os.listdir(base)) if f.endswith(".html")}

    entries = [{"u": f, "m": NAME, "t": p.title, "h": p.heads, "x": " ".join(" ".join(p.text).split())}
               for f, p in pages.items()]
    js = ("// Made by tools/build_manual.py - don't edit; run it again instead.\n"
          "window.ROSETTA_SEARCH = " + json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(os.path.join(base, "search-index.js"), "w", encoding="utf-8").write(js)

    order = []
    for href in pages["index.html"].links:
        if "/" in href or href.startswith(("http", "mailto", "#")):
            continue
        name = href.split("#")[0]
        if name.endswith(".html") and name != "index.html" and name in pages and name not in order:
            order.append(name)

    for f in pages:
        path = os.path.join(base, f)
        text = open(path, encoding="utf-8").read()
        pager = ""
        if f in order:
            i = order.index(f)
            links = []
            if i > 0:
                links.append('<a class="pager-prev" href="%s"><span>Previous</span>%s</a>'
                             % (order[i - 1], html.escape(pages[order[i - 1]].title)))
            links.append('<a class="pager-contents" href="index.html"><span>%s</span>Contents</a>' % NAME)
            if i < len(order) - 1:
                links.append('<a class="pager-next" href="%s"><span>Next</span>%s</a>'
                             % (order[i + 1], html.escape(pages[order[i + 1]].title)))
            pager = '<nav class="pager" aria-label="Previous and next page">%s</nav>' % "".join(links)
        new = text
        if "<!--pager-->" not in new:
            new = new.replace("</main>", "<!--pager--><!--/pager-->\n</main>", 1)
        new = re.sub(r"<!--pager-->.*?<!--/pager-->", lambda m: "<!--pager-->" + pager + "<!--/pager-->", new, flags=re.S)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
    print("%s: %d pages, %d in contents order, search index %d KB" % (FOLDER, len(pages), len(order), len(js) // 1024))


if __name__ == "__main__":
    main()
