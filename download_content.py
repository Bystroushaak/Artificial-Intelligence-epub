#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
import urllib2  # for HTTPError
import mimetypes


import httpkie
import dhtmlparser


import epub


# Variables ===================================================================
DOWNER = httpkie.Downloader()
BASE_URL = "http://www.cs.ubc.ca/~poole/aibook/html/"
IMAGES = "images"
COVER_FN = "book_cover.xhtml"

CONTENT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<HTML xmlns="http://www.w3.org/1999/xhtml">
<body>
%s
</body>
</HTML>"""
URL_CACHE = set()


# Functions & objects =========================================================
class Content(object):
    def __init__(self, url, filename=None):
        self.skip_this = False
        self.subcontents = []

        # parse url
        if "#" in url:
            url = url.split("#")[0]

        if "http" not in url:
            url = os.path.join(BASE_URL, url)
            # url = os.path.normpath(url)

        self.url = url

        # parse filename
        if not filename:
            filename = os.path.basename(url)
        self.filename = filename

        # check cache
        global URL_CACHE
        if url in URL_CACHE:
            self.skip_this = True
            # print "\tSkipping", self.url
            return
        else:
            URL_CACHE.add(url)

        print url

        try:
            self.content = self.get_content()
        except urllib2.HTTPError:
            self.skip_this = True
            print "\tSkipping", self.url

    def get_content(self):
        return DOWNER.download(self.url)

    def get_mimetype(self):
        return mimetypes.guess_type(self.url)[0]

    def get_sub_contents(self):
        return []


class Image(Content):
    def __init__(self, url, filename=None):
        super(Image, self).__init__(url, filename)
        
        if not filename:
            filename = url.split("/")

            if len(filename) > 2:
                self.filename = "_".join(filename[-2:])

    @property
    def filename(self):
        return os.path.join(IMAGES, self.__dict__["filename"])

    @filename.setter
    def filename(self, fn):
        self.__dict__["filename"] = fn


class Text(Content):
    def __init__(self, url, filename=None, recurse=False):
        self.recurse = recurse
        super(Text, self).__init__(url, filename)


    def _parse_sub_contents(self, dom):
        for image in dom.find("img"):
            self.subcontents.append(
                Image(image.params["src"])
            )
            image.params["src"] = self.subcontents[-1].filename

        if not self.recurse:
            return

        for link in dom.find("a"):
            if "href" not in link.params:
                continue

            link = link.params["href"]

            if "://" in link or link.startswith("www"):
                continue

            self.subcontents.append(
                Text(link)
            )
            # add also subcontents of subcontents
            self.subcontents.extend(
                self.subcontents[-1].get_sub_contents()
            )

    def get_content(self):
        content = super(Text, self).get_content()

        dom = dhtmlparser.parseString(content)
        main = dom.find("div", {"id": "main"})

        self.title = dom.find("title")[0].getContent()
        self.title = self.title.split("--")[-1].strip()

        if not main:
            return content

        self._parse_sub_contents(main[0])

        return CONTENT_TEMPLATE % str(main[0])

    def get_sub_contents(self):
        # skip items that were already in URL_CACHE
        return filter(lambda x: not x.skip_this, self.subcontents)


class TOC(Text):
    def _parse_sub_contents(self, dom):
        for link in dom.match("li", "a"):
            self.subcontents.append(
                Text(link.params["href"], recurse=True)
            )


# Main program ================================================================
if __name__ == '__main__':
    if not os.path.exists(IMAGES):
        os.mkdir(IMAGES)

    toc = TOC("http://www.cs.ubc.ca/~poole/aibook/html/ArtInt.html")
    cover = Image("http://enbooks.cn/images/btbimages/182/9780521519007.jpg")
    package = [
        toc,
        cover,
    ]

    chapters = toc.get_sub_contents()

    images = []
    for chapter in chapters:
        package.extend(chapter.get_sub_contents())

    package.extend(chapters)

    # save everything to disk
    print "Saving to disk.."
    for item in package:
        with open(item.filename, "wb") as f:
            f.write(item.content)

    # create cover for book
    cover_xml = epub.gen_cover(cover.filename)
    with open(COVER_FN, "w") as f:
        f.write(cover_xml)

    # create toc.ncx
    
