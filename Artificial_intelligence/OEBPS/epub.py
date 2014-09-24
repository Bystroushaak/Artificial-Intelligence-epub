#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import uuid
import os.path
import mimetypes
from string import Template


# Variables ===================================================================
COVER_TEMPLATE = """<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Cover</title>
<meta content="urn:uuid:$uid" name="Adept.expected.resource"/>
</head>
<body>
<a id="cover"/>
<img alt="cover" src="$path" style="height: 100%;"/>
</body>
</html>"""

TOC_TEMPLATE = """<?xml version="1.0"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="$title" content=""/>
</head>
<docTitle>
<text>$title</text>
</docTitle>
<navMap>
$content
</navMap>
</ncx>
"""

NAV_POINT_TEMPLATE = """
<navPoint id="navpoint-$cnt" playOrder="$cnt">
<navLabel>
<text>$title</text>
</navLabel>
<content src="$filename"/>
</navPoint>
"""

CONTENT_TEMPLATE = """<?xml version="1.0"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:title>--TITLE--</dc:title>
<dc:creator>--AUTHOR--</dc:creator>
<dc:publisher>--PUBLISHER--</dc:publisher>
<dc:format/>
<dc:date>--DATE-AS-"YYYY-MM-DD"--</dc:date>
<dc:subject/>
<dc:description/>
<dc:rights/>
<dc:language>en</dc:language>
<dc:identifier id="BookId" opf:scheme="ISBN">--ISBN--</dc:identifier>
<meta content="cover" name="cover"/>
</metadata>

<manifest>
<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
$manifest
</manifest>

<spine toc="ncx">
$spine
</spine>

<guide>
<reference href="$covername" title="Cover" type="cover"/>
<reference href="$tocname" title="Table of Contents" type="toc"/>
</guide>
</package>
"""

ITEM_TEMPLATE = '<item href="$path" id="$id" media-type="$mime"/>'
ITEMREF_TEMPLATE = '<itemref idref="$id" linear="yes"/>\n'


# Functions & objects =========================================================
def _get_id(fn):
    return os.path.basename(
        fn.replace(".", "_")
    )

def _filename_to_int(fn):
    splitted = fn.replace(".", "_").replace("-", "_").split("_")

    digits = filter(lambda x: x.isdigit(), splitted)

    if not digits:
        return 0

    return int(digits[0])


def gen_cover(path, uid=None):
    if not uid:
        uid = str(uuid.uuid4())

    return Template(COVER_TEMPLATE).substitute(uid=uid, path=path)


def gen_toc_ncx(title, chapters):
    content = ""

    chapters = sorted(chapters, key=lambda x: _filename_to_int(x.filename))
    for cnt, chapter in enumerate(chapters):
        if chapter.title == "":
            continue

        content += Template(NAV_POINT_TEMPLATE).substitute(
            title=chapter.title,
            filename=chapter.filename,
            cnt=cnt
        )

    return Template(TOC_TEMPLATE).substitute(title=title, content=content)


def gen_content_opf(chapters, cover, toc, img_dir):
    blacklist = set([
        "toc.ncx",
        "epub.pyc"
    ])

    files = filter(
        lambda x: os.path.isfile(x) and x not in blacklist,
        os.listdir(".")
    )
    images = map(lambda x: os.path.join(img_dir, x), os.listdir(img_dir))
    images = filter(lambda x: os.path.isfile(x), images)

    # create manifest with links to all files
    manifest = map(
        lambda fn: Template(ITEM_TEMPLATE).substitute(
            path=fn,
            mime=mimetypes.guess_type(fn)[0],
            id=_get_id(fn)
        ),
        images + files
    )
    manifest = "\n".join(manifest)

    # text/html is not appropriate for XHTML/OPS, use application/xhtml+xml
    # instead (don't ask..)
    manifest = manifest.replace("text/html", "application/xhtml+xml")

    # create spine
    chapters = sorted(chapters, key=lambda x: _filename_to_int(x.filename))

    spine = ""
    for chapter in chapters:
        spine += Template(ITEMREF_TEMPLATE).substitute(
            id=_get_id(chapter.filename),
        )

    return Template(CONTENT_TEMPLATE).substitute(
        manifest=manifest,
        spine=spine,
        covername=cover.filename,
        tocname=toc.filename
    )
