#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import uuid
from string import Template


# Variables ===================================================================
# <link href="wileysd_template_v1.2.css" rel="stylesheet" type="text/css"/>
COVER_TEMPLATE = """<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Cover</title>
<meta content="urn:uuid:%s" name="Adept.expected.resource"/>
</head>
<body>
<a id="cover"/>
<img alt="cover" src="%s" style="text-align: center;"/>
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


# Functions & objects =========================================================
def _filename_to_int(fn):
    splitted = fn.replace(".", "_").split("_")

    digits = filter(lambda x: x.isdigit(), splitted)

    if not digits:
        return 0

    return int(digits[0])


def gen_cover(path, uid=None):
    if not uid:
        uid = str(uuid.uuid4())

    return COVER_TEMPLATE % (uid, path)


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


# Main program ================================================================
if __name__ == '__main__':
    pass
