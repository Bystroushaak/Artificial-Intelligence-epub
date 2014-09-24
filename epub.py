#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import uuid


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


# Functions & objects =========================================================
def gen_cover(path, uid=None):
    if not uid:
        uid = str(uuid.uuid4())

    return COVER_TEMPLATE % (uid, path)



# Main program ================================================================
if __name__ == '__main__':
    pass
